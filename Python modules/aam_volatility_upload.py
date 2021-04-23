"""
Date                    : 2017-02-16
Purpose                 : Automate AAM Volume Surfaces updates
Department and Desk     : AAM
Requester               : Suvarn Naidoo
Developer               : Ondrej Bahounek

Info:
Root directory: y:\jhb\FALanding\Prod\AAM
Template file: y:\jhb\FALanding\Prod\AAM\template\structure_template.csv
Weekly files: y:\jhb\FALanding\Prod\AAM\current_week\volsurface.csv
    - comma delimited csv file

1) weekly files uploaded by AAM team (AAMCape) every week by Wednesday's C.O.B.
2) Upload task runs every Thursday morning
3-a) email successful result to the AAM team
3-b) email erroneous result to both AAM and BTB teams

1) read structure_template first into dict
    1.1) contains info about all benchmarks that need to be updated
2) read volume surfaces file that contain benchmark points
    2.1) if benchmark was in the template, but doesn't exist - create one
    2.2) update points in FA if bond is present in structure_template
    2.3) uploaded volatility is multiplied by 0.01
3) use Volatility Manager for check

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2017-02-23      4297948         Ondrej Bahounek         Initial implementation.
2020-01-09      FAPE-181        Iryna Shcherbina        Use RTB as the email sender.
"""

import acm
import csv
import at_ael_variables
from at_email import EmailHelper
from at_logging import getLogger

import os
from collections import namedtuple, defaultdict
import UserDict


LOGGER = getLogger()


class MissingFileException(IOError):
    def __str__(self):
        return "Missing File: '%s'" % self.message


VolPoint = namedtuple("VolPoint", ["exp_day", "strike", "volatility"])


class Template(UserDict.IterableUserDict):

    UPDATED_VAL = -6666

    _required_params = [
        "BOND",
        "Name"
        ]

    _prop_params = [
        "StructureType",
        "Framework",
        "BondVolatilityType",
        "AbsUnderlyingMaturity",
        "StrikeType",
        "Currency",
        "VolatilityValueType",
        "InterpolationMethod",
        "RiskType",
        "ExpiryInterpolationMethod"
        ]

    def __init__(self, template_dict):
        all_required_params = set(self._required_params + self._prop_params)
        if all_required_params != set(template_dict.keys()):
            raise ValueError("Template columns are different from the required ones.")
        self.data = template_dict
        self.vol_data = []

    def get_name(self):
        return self['BOND']

    def add_point(self, vol_point):
        self.vol_data.append(vol_point)

    def get_vol_data(self):
        return self.vol_data

    def get_points_dict(self):
        """ Return dictionary of dictionaries:

            ['exp_day']['strike'] => volatility
        """
        the_dict = defaultdict(dict)
        for volpoint in self.vol_data:
            the_dict[volpoint.exp_day][volpoint.strike] = volpoint.volatility
        return the_dict

    def get_input_raw(self, points_dict=None):
        """ Print data in the same visual format as they are expected in the file.

        first row: BOND, <<STRIKES>> sorted
        all other rows (4 in total): EXPIRY_DAY, <<VOLATILITIES>> sorted
        """

        if not points_dict:
            points_dict = self.get_points_dict()

        strikes = sorted(float(k) for k in list(points_dict.values())[0])
        expiry_dates = sorted(points_dict.keys())
        rows = [[self.get_name()] + strikes]

        for expiry in expiry_dates:
            points = []
            for strike in strikes:
                points.append(points_dict[expiry][strike])
            rows.append([expiry] + points)
        return rows

    def _add_point(self, vol_struct_name, expiry, strike, volatility):
        vp = acm.FVolatilityPoint()
        vp.Structure(acm.FVolatilityStructure[vol_struct_name])
        vp.Call(True)
        vp.ExpiryDay(expiry)
        vp.Strike(strike)
        vp.Volatility(volatility)
        vp.ExpiryPeriod("0d")
        vp.ExpiryPeriod_count(0)
        vp.ExpiryPeriod_unit("Days")
        vp.UnderlyingMaturityPeriod("0d")
        vp.UnderlyingMaturityPeriod_count(0)
        vp.UnderlyingMaturityPeriod_unit("Days")
        vp.Commit()
        return vp

    def update_structure(self):
        if not self.vol_data:
            raise RuntimeError("Missing data to upload.")

        LOGGER.info("Updating: '%s'" % self['Name'])
        cls = acm.FBenchmarkVolatilityStructure
        volobj = cls.Select01('name="%s"' % self['Name'], None)
        if not volobj:
            volobj = cls()
            volobj.Name(self['Name'])
            LOGGER.info("Creating a new structure...")

        for prop_name in self._prop_params:
            LOGGER.info("%s: '%s'" % (prop_name, self[prop_name]))
            volobj.SetProperty(prop_name, self[prop_name])

        volobj.Commit()

        points_dict = self.get_points_dict()

        acm.BeginTransaction()
        try:
            # Delete and update old points
            vol_points_oids = [vp.Oid() for vp in volobj.Points()]
            for point_oid in vol_points_oids:
                point = acm.FVolatilityPoint[point_oid]
                strike = point.Strike()
                expiry = point.ExpiryDay()
                if points_dict.get(expiry) and points_dict[expiry].get(strike):
                    point.Volatility(points_dict[expiry][strike] * 0.01)
                    point.Commit()
                    points_dict[expiry][strike] = self.UPDATED_VAL
                else:
                    volobj.RemovePoint(point)

            # I'm using this approach which enables rerunning and backdating.
            # Preferable approach would be using FVolatilityStructure.InsertPoint,
            # but it won't insert an expired/historical point. This might still be fine,
            # because every week there will be new data, but I have chosen the below way
            # for now before the whole process is consolidated.
            for expiry, dk1 in list(points_dict.items()):
                for strike, volatility in list(dk1.items()):
                    if volatility != self.UPDATED_VAL:
                        self._add_point(volobj.Name(), expiry, strike, volatility * 0.01)

            volobj.Commit()

            acm.CommitTransaction()

        except:
            acm.AbortTransaction()
            raise

        if volobj.Points().Size() != len(self.get_vol_data()):
            raise RuntimeError(
                "Result point size %s differs from the input size %s."
                % (volobj.Points().Size(), len(self.get_vol_data())))

        LOGGER.info("'%s' updated. (#points: %d)" % (volobj.Name(), volobj.Points().Size()))

    def read_from_db(self):
        acm.PollDbEvents()
        points_dict = defaultdict(dict)
        vol_obj = acm.FVolatilityStructure[self['Name']]
        for point in vol_obj.Points():
            points_dict[point.ExpiryDay()][point.Strike()] = point.Volatility() * 100

        return points_dict


ael_variables = at_ael_variables.AelVariableHandler()
ael_variables.add("root_dir",
                  label="Root directory",
                  cls="string",
                  default=r"y:\jhb\FALanding\Prod\AAM",
                  mandatory=True,
                  alt=("Root directory of files. \n"
                       "Child directories must by named by dates."))
ael_variables.add("file_vol_data",
                  label="Vol Data file",
                  cls="string",
                  default=r"volsurface.csv",
                  mandatory=True,
                  alt="Volatility data filename.")
ael_variables.add("file_template",
                  label="Template file",
                  cls="string",
                  default=r"template\structure_template.csv",
                  mandatory=True,
                  alt=("A path to a template file. \n"
                       "Can be set relatively to a root directory, or absolutely."))

# EMAIL TAB
ael_variables.add("send_mail",
                  label="Send Mails?_Email",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt="Should errors be sent via email?")
ael_variables.add("email_recipients",
                  label="Recipients_Email",
                  default="",
                  multiple=True,
                  mandatory=False,
                  alt="Email recipients. Use comma seperated email addresses \
                       if you want to send report to multiple users.")
ael_variables.add("cc_recipients",
                  label="CC Recipients_Email",
                  default="ondrej.bahounek@barclays.com",
                  multiple=True,
                  mandatory=False,
                  alt="CC email recipients. Use comma seperated email addresses \
                       if you want to send report to multiple users.")


def get_template_fname(ael_dict):
    template_path = ael_dict['file_template']
    if os.path.exists(template_path):
        return template_path

    full_path = os.path.join(ael_dict['root_dir'], template_path)
    if not os.path.exists(full_path):
        raise MissingFileException(full_path)

    return full_path


def get_vol_data_fname(ael_dict):
    full_path = os.path.join(ael_dict['root_dir'], ael_dict['file_vol_data'])
    if not os.path.exists(full_path):
        raise MissingFileException(full_path)

    return full_path


def read_template(template_file):
    templates = []
    with open(template_file, "rb") as infile:
        dicreader = csv.DictReader(infile)
        for row in dicreader:
            templ = Template(row)
            templates.append(templ)
    return templates


def read_vol_data_file(fname, templates):
    loaded_templates = []
    with open(fname, "rb") as infile:
        LOGGER.info("Reading '%s'..." % fname)
        reader = csv.reader(infile, delimiter=",")
        for row in reader:
            if not row[0]:
                strike_list = current_template = None
                continue

            templ = [t for t in templates if t.get_name() == row[0]]
            if templ:
                current_template = templ[0]
                strike_list = row[1:len(row)]
                loaded_templates.append(current_template)
                continue

            if not current_template:
                continue

            exp_day = acm.Time.DateFromTime(row[0])
            for index, vol in enumerate(row[1:len(row)]):
                strike = float(strike_list[index])
                volatility = float(vol)
                vol_point = VolPoint(exp_day, strike, volatility)
                current_template.add_point(vol_point)

    return loaded_templates


def to_text(raw_data):
    res_text = ""
    for row in raw_data:
        line = ",".join(map(str, row)) + "\n"
        res_text += line
    return res_text


def to_html(raw_data):
    res_text = '<table width="100%" border="1">'
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, raw_data[0])) + "</tr>"
    for row in raw_data[1:]:
        line = "<tr>" + "<td><b>%s</b></td>" % row[0] + "".join(map("<td>{0}</td>".format, row[1:])) + "</tr>"
        res_text += line
    return res_text + "</table>"


def send_mail(subject, body, recipients_list, cc_recipients):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    email_helper = EmailHelper(
        body,
        '{} - {}'.format(subject, environment),
        recipients_list,
        mail_cc=cc_recipients,
    )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.error("Error while sending e-mail: %s" % exc)


def send_email_OK(data_text, recipients, cc_recipients):
    if not (recipients or cc_recipients):
        return
    subj = "AAM volatility upload successful"
    body = (
        "Hello AAM team, <br /><br />"
        "These volatility structures were updated: <br />"
        "{}".format(data_text))
    send_mail(subj, body, recipients, cc_recipients)


def send_email_FAIL(data_text, recipients, cc_recipients):
    if not (recipients or cc_recipients):
        return
    subj = "AAM volatility upload FAILED"
    body = (
        "Hello AAM team, <br /><br />There was an error: <br />"
        "<b>{}</b>"
        "<br /><br /><br />"
        "Python module: <b>{}</b>"
        "<br /><br />"
        "Please, contact <b>'{}'</b> and <b>'{}'</b> teams".format(
            data_text, __name__,
            "CIB Africa Prime and Equities Dev",
            "ABCap-IT-RTB-AM-Front-Arena"))
    send_mail(subj, body, recipients, cc_recipients)


def ael_main(ael_dict):
    email_recipients = list(ael_dict["email_recipients"])
    cc_recipients = list(ael_dict["cc_recipients"])

    try:
        template_fname = get_template_fname(ael_dict)
        vol_data_fname = get_vol_data_fname(ael_dict)
        templates = read_template(template_fname)
        used_templates = read_vol_data_file(vol_data_fname, templates)

        html_text = ""
        for t in used_templates:
            t.update_structure()
            points_dict = t.read_from_db()
            raw_data = t.get_input_raw(points_dict)
            html_text += to_html(raw_data)
            html_text += "<br />"
            LOGGER.info("*" * 50)

        if ael_dict["send_mail"]:
            send_email_OK(html_text, email_recipients, cc_recipients)

        LOGGER.info("Completed successfully.")

    except Exception as exc:
        if ael_dict["send_mail"]:
            send_email_FAIL(str(exc), email_recipients, cc_recipients)
        LOGGER.exception("Upload failed.")
        raise
