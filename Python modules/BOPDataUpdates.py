"""
This module is supposed to clean and fix the parties addresses.

It contains to processes:
    1. The process that fixes the addresses based on the provided information
    2. The process that performs a rollback, based on the provided log files

1. The process that fixes addresses uses the following files:
    a. A csv file with the wrong and correct countries,
    b. A csv file with countries and capitals,
    c. A csv file with Countries, cities, streets, suburbs and zip codes,
This process generates 6 csv files:
    a. Checking - 3 files that contain the information about the changes that will be performed
    b. Fixing - 3 files that contain the log of the performed changes (even those that failed) (these should be used for rollback)

2. The process that performs the rollback uses the following files
    a. A csv with the party name, old country and new country,
    b. A csv with the party name, old city and new city,
    c. A csv with the party name, old zip code and new zip code.
This process generates 3 csv files:
    a. rb_fixing - 3 files that contain the log of the performed changes (even those that failed)

"""
import ael
from collections import defaultdict
import csv
from datetime import datetime
import os

from at_ael_variables import AelVariableHandler


# these should be similar to attribute names from party
E_COUNTRY = 'country'
E_CITY = 'city'
E_ZIPCODE = 'zipcode'
E_ADDRESS2 = 'address2'

ATTRIBUTES = [E_COUNTRY, E_CITY, E_ZIPCODE, E_ADDRESS2]

def _get_parties():
    ael.poll()
    return ael.Party.select()

class LogInfo(object):

    E_LOG_TYPE_FIXING = 'fixing'
    E_LOG_TYPE_CHECKING = 'checking'

    def __init__(self, attribute, log_type, is_rollback=False):
        self.log_type = log_type
        self.attribute = attribute
        self.is_rollback = is_rollback


class BOPLog(object):
    """ This class is responsible for logging the checkings and the fixes. """

    def __init__(self, log_path, run_time):
        self._csv_writers = {}
        self.logs_info = []
        self.run_time = run_time
        self.log_path = log_path

    def _get_log_path(self, file_name):
        """ Return the log file path
        """
        return os.path.join(self.log_path, file_name)

    def write_fixing_log(self, data, name):
        """ Write the data list to the specified log name,
        fixing log type
        """
        self._write_to_log(data, name, LogInfo.E_LOG_TYPE_FIXING)

    def write_checking_log(self, data, name):
        """ Write the data list to the specified log name,
        checking log type
        """
        self._write_to_log(data, name, LogInfo.E_LOG_TYPE_CHECKING)

    def _write_to_log(self, data, name, log_type):
        """ Write the data list to the specified log name and log type
        """
        (writer, _) = self._csv_writers[(log_type, name)]
        writer.writerow(data)

    def add_csv_writer(self, file_name, log_type, is_rollback=False):
        """ Open a csv writer
        """
        if is_rollback:
            file_name_template = "rb_{0}_{1}_{2}.csv"
        else:
            file_name_template = "{0}_{1}_{2}.csv"
        log_path = self._get_log_path(file_name_template.format(log_type,
                                                                  file_name,
                                                                  self.run_time))
        self._csv_writers[(log_type, file_name)] = BOPLog._open_writer(log_path)

    @classmethod
    def _open_writer(cls, csv_file_path):
        """ Open a new csv writer """
        csv_file = open(csv_file_path, 'wb')
        writer = csv.writer(csv_file)
        return (writer, csv_file)

    def close_all_logs(self):
        """ Close all log files """
        for _, (_, csv_file) in self._csv_writers.iteritems():
            csv_file.close()

class BOPRollbackLog(BOPLog):

    def __init__(self, log_path, run_time):
        super(BOPRollbackLog, self).__init__(log_path, run_time)

        for att in ATTRIBUTES:
            self.add_csv_writer(att, LogInfo.E_LOG_TYPE_FIXING, True)


class BOPFixingLog(BOPLog):

    def __init__(self, log_path, run_time):
        super(BOPFixingLog, self).__init__(log_path, run_time)

        for att in ATTRIBUTES:
            self.add_csv_writer(att, LogInfo.E_LOG_TYPE_CHECKING)
            self.add_csv_writer(att, LogInfo.E_LOG_TYPE_FIXING)


class Addresses(object):
    """ This class is used to hold a collection of addresses. """
    def __init__(self, _addresses, indexate=False):
        self._addresses = []
        self._by_country = defaultdict(lambda: Addresses([]))
        self._by_city = defaultdict(lambda: Addresses([]))
        self._addresses.extend(_addresses)
        self.indexate = indexate

    def is_empty(self):
        """ Return true if the collection is empty """
        return self._addresses == []

    def add(self, address):
        """ Adds the new address to the collection """
        self._addresses.append(address)

        if self.indexate:
            self._by_country[address.country.lower()].add(address)
            self._by_city[address.city.lower()].add(address)

    def get_country(self, country):
        """ Returns the addresses that correspond to the provided country """
        if self.indexate:
            if self._by_country.has_key(country.lower()):
                return self._by_country[country.lower()]
            else:
                return Addresses([])
        else:
            result = [address for address in self._addresses
                      if address.country.lower() == country.lower()]
            return  Addresses(result)

    def get_city(self, city):
        """ Returns the addresses that correspond to the provided city """
        if self.indexate:
            if self._by_city.has_key(city.lower()):
                return self._by_city[city.lower()]
            else:
                return Addresses([])
        else:
            result = [address for address in self._addresses
                      if address.city.lower() == city.lower()]
            return  Addresses(result)

    def get_zip(self, zipcode):
        """ Returns the addresses that correspond to the provided zipcode """
        result = Addresses([address for address in self._addresses
                               if address.zipcode.lower() == zipcode.lower()])

        return result

    def get_suburb(self, suburb):
        """ Returns the addresses that correspond to the provided suburb """
        result = Addresses([address for address in self._addresses
                               if address.suburb.lower() == suburb.lower()])

        return result

    def get_street(self, street):
        """ Returns the addresses that correspond to the provided street """
        result = Addresses([address for address in self._addresses
                               if address.street.lower() == street.lower()])

        return result

    def print_addresses(self):
        """ Print the address to output """
        for address in self._addresses:
            print "{0},\t{1},\t{2}".format(address.country,
                                           address.city, address.zipcode)

    def get_first_address(self):
        """ Returns the first address from the collection if exists """
        if len(self._addresses) > 0:
            return self._addresses[0]
        else:
            return None

class Address(object):

    _ignore_values = ['N/A', '-']

    """ This is a container for an address. """
    def __init__(self, country='', city='', suburb='', street='', zipcode=''):
        self.country = Address._clean_value(country)
        self.city = Address._clean_value(city)
        self.suburb = Address._clean_value(suburb)
        self.street = Address._clean_value(street)
        self.zipcode = Address._clean_value(zipcode)

        # the zipcode has to be a 4 digit number,
        self.zipcode = "{0}{1}".format("0"*(4 - len(self.zipcode)), self.zipcode)

    @classmethod
    def _clean_value(cls, value):
        value = value.strip()
        if value in Address._ignore_values:
            value = ""
        return value


class RollbackAddress(object):

    def __init__(self, party_id, attribute, old_value='', new_value='', err=''):
        self.party_id = party_id
        self.old_value = old_value
        self.new_value = new_value
        self.attribute = attribute
        self.err = err


class PartyUpdater(object):

    def __init__(self, commit, log):
        self.commit = commit
        self.log = log

    def update_party(self, party, attribute, new_value):
        """ Update the specified attribute for the specified party """
        if attribute not in ATTRIBUTES:
            raise Exception('Unexpected attribute {0}'.format(attribute))
        old_value = getattr(party, attribute)
        log_items = [party.ptyid, old_value, new_value.upper()]
        if self.commit:
            try:
                new_party = party.clone()
                setattr(new_party, attribute, new_value)
                new_party.commit()
            except Exception, ex:
                print ex
                log_items.append(ex)
        if self.commit:
            self.log.write_fixing_log(log_items, attribute)

class BOPDataUpdates(object):
    """ Contains the required functions to fix the parties addresses
    """

    def __init__(self, commit, fixing_files, log_path, run_time):
        # wrong title: correct title
        self.commit = commit
        self.log = BOPFixingLog(log_path, run_time)
        self.party_updater = PartyUpdater(self.commit, self.log)
        self.countries_fix = {}
        self.capitals = Addresses([], True)
        self.addresses = Addresses([], True)
        self._init_base_data(fixing_files)


    def _init_base_data(self, fixing_files):
        """ Initialises data from base files. """
        country_csv_file = fixing_files['input_file_country']  # r"C:\tmp\clean\countries.csv"
        cities_csv_file = fixing_files['input_file_cities']  # r"C:\tmp\clean\capitals.csv"
        zipcodes_csv_file = fixing_files['input_file_zipcodes']  # r"C:\tmp\clean\zip.csv"

        with open(country_csv_file) as csv_file:
            reader = csv.reader(csv_file)
            reader.next()
            for row in reader:
                self.countries_fix[row[0].lower()] = row[1].strip()


        with open(cities_csv_file) as csv_file:
            reader = csv.reader(csv_file)
            reader.next()
            for row in reader:
                address = Address(row[0], row[1])
                self.capitals.add(address)


        with open(zipcodes_csv_file) as csv_file:
            reader = csv.reader(csv_file)
            reader.next()
            for row in reader:
                address = Address(row[0], row[1], row[2], row[3], row[4])
                self.addresses.add(address)

    def fix_country(self):
        """ Fix the country

        Based on the list of countries to be fixed
        """
        parties = _get_parties()

        print 'Fixing country:...'
        header_data = ["Party", "OldCountry", "NewCountry"]
        self.log.write_fixing_log(header_data, E_COUNTRY)
        for party in parties:

            if party.country != party.country.strip():
                self.party_updater.update_party(party, E_COUNTRY,
                                                party.country.strip().upper())

            if self.countries_fix.has_key(party.country.lower()):
                self.party_updater.update_party(party, E_COUNTRY,
                                   self.countries_fix[party.country.lower()].upper())

        print 'Fixed country:...'
        print "-"*40

    def print_unknown_countries(self):
        """ Outputs the parties which don't ahve a valid country """
        parties = _get_parties()

        output = []
        print 'Unknown countries..'
        self.log.write_checking_log(["Party", "Country"], E_COUNTRY)
        for party in parties:
            has_country = party.country and party.country.lower() != 'null'
            country_cleaned = party.country.lower().strip()
            base_capital = self.capitals.get_country(country_cleaned).is_empty()
            if not has_country or not base_capital:
                continue
            if not self.countries_fix.has_key(country_cleaned):
                output.append(party)

        for party in output:
            self.log.write_checking_log([party.ptyid, party.country], E_COUNTRY)
        print 'Finished unknown countries'

    def fix_capital(self):
        """ Fix the city

        Based on the list of countries and capitals
        """
        parties = _get_parties()

        to_change = []
        print 'Checking cities:'
        header_data = ["Party", "Country", "ZipCode",
                       "WrongCity", "City(by zipcode)"]
        self.log.write_checking_log(header_data, E_CITY)
        for party in parties:
            if party.zipcode == "":
                continue
            if not self.addresses.get_city(party.city).is_empty():
                continue
            country = self.addresses.get_country(party.country)
            if country.is_empty():
                continue
            cities_by_zipcode = country.get_street(party.zipcode)
            if cities_by_zipcode.is_empty():
                cities_by_zipcode = country.get_zip(party.zipcode)
            if cities_by_zipcode.is_empty():
                continue
            new_city = cities_by_zipcode.get_first_address().city.upper()
            if new_city != "" and new_city != party.city:
                data = [party.ptyid, party.country, party.zipcode,
                        party.city, new_city]
                self.log.write_checking_log(data, E_CITY)
                to_change.append((party, new_city))

        print 'Finished checking cities'

        print 'Fixing cities'
        self.log.write_fixing_log(["Party", "OldCity", "NewCity"], E_CITY)
        for (party, new_city) in to_change:
            self.party_updater.update_party(party, E_CITY, new_city)
        print 'Finished fixing cities'
        print "-"*40

    def fix_zipcode(self):
        """ Fix the city

        Based on the list of cities and suburbs
        """
        parties = _get_parties()

        to_change = []
        print 'Checking zip code:'
        header_data = ["Party", "Country", "City", "Suburb",
                      "OldZipcode", "NewZipCode(by city and suburb)"]
        self.log.write_checking_log(header_data, E_ZIPCODE)
        for party in parties:
            # we want to fix only the empty values (email communication)
            if party.zipcode != "":
                continue
            if party.address2 == "":
                continue
            country = self.addresses.get_country(party.country)
            if country.is_empty():
                continue
            city = country.get_city(party.city)
            # the existing zip code is invalid
            if city.is_empty() or not city.get_street(party.zipcode).is_empty():
                continue
            suburb = city.get_suburb(party.address2)
            if suburb.is_empty():
                continue
            new_zipcode = suburb.get_first_address().street
            # could not find by street
            if new_zipcode == "":
                new_zipcode = suburb.get_first_address().zipcode
            if new_zipcode != "" and new_zipcode != party.zipcode:
                data = [party.ptyid, party.country, party.city,
                        party.address2, party.zipcode, new_zipcode]
                self.log.write_checking_log(data, E_ZIPCODE)
                to_change.append((party, new_zipcode))

        print 'Finished checking zip codes'

        print 'Fixing zip codes'
        header_data = ["Party", "OldZipCode", "NewZipCode"]
        self.log.write_fixing_log(header_data, E_ZIPCODE)
        for (party, new_zipcode) in to_change:
            self.party_updater.update_party(party, E_ZIPCODE, new_zipcode)
        print 'Finished fixing zip codes'

        print "-"*40

    def fix_address2(self):
        """ Fix the additional address

        Based on the list of countries and capitals and zip codes
        """
        parties = _get_parties()

        to_change = []
        print 'Checking additioanl addresses:'
        header_data = ["Party", "Country", "City", "ZipCode",
                       "WrongAdditionalAddress", "AdditionalAddress(by zipcode)"]
        self.log.write_checking_log(header_data, E_ADDRESS2)
        for party in parties:
            if party.country == "" or party.zipcode == "" or party.city == "":
                continue
            country = self.addresses.get_country(party.country)
            if country.is_empty():
                continue
            city = country.get_city(party.city)
            if city.is_empty():
                continue
            suburb_by_street = city.get_street(party.zipcode)
            if suburb_by_street.is_empty():
                continue
            new_address2 = suburb_by_street.get_first_address().suburb
            if new_address2 != "" and new_address2 != party.address2:
                data = [party.ptyid, party.country, party.city, party.zipcode,
                        party.address2, new_address2]
                self.log.write_checking_log(data, E_ADDRESS2)
                to_change.append((party, new_address2))

        print 'Finished checking  additional address'

        print 'Fixing  additional address'
        self.log.write_fixing_log(["Party", "OldAdditionalAddress", "NewAdditionalAddress"], E_ADDRESS2)
        for (party, new_add_address) in to_change:
            self.party_updater.update_party(party, E_ADDRESS2, new_add_address)
        print 'Finished fixing additional address'
        print "-"*40

    def run_all(self):
        """ Run all fixes """
        try:
            self.print_unknown_countries()
            self.fix_country()
            self.fix_capital()
            self.fix_zipcode()
            self.fix_address2()
        finally:
            self.log.close_all_logs()

class BOPRollback(object):
    """ Contains the required functions to perform a rollback
    """
    def __init__(self, commit, rb_files, log_path, run_time):
        self.commit = commit
        self.log = BOPRollbackLog(log_path, run_time)
        self.party_updater = PartyUpdater(self.commit, self.log)
        self.countries = []
        self.cities = []
        self.zipcodes = []
        self.address2 = []
        self._init_rollback_csv(rb_files)

    def _init_rollback_csv(self, rb_files):
        """ Initialise the data for rollback operation
        """
        rb_countries_file = rb_files['log_file_countries']  # r"c:\tmp\clean\log\fixing_country_2014-09-22 13-18-42.csv"
        rb_cities_file = rb_files['log_file_cities']  # r"c:\tmp\clean\log\fixing_city_2014-09-22 13-18-42.csv"
        rb_zipcodes_file = rb_files['log_file_zipcodes']  # r"c:\tmp\clean\log\fixing_zipcode_2014-09-22 13-18-42.csv"
        rb_address2_file = rb_files['log_file_address2']  # r"c:\tmp\clean\log\fixing_address2_2014-09-22 13-18-42.csv"

        self.countries = self._read_from_csv(rb_countries_file, E_COUNTRY)
        self.cities = self._read_from_csv(rb_cities_file, E_CITY)
        self.zipcodes = self._read_from_csv(rb_zipcodes_file, E_ZIPCODE)
        self.address2 = self._read_from_csv(rb_address2_file, E_ADDRESS2)


    def _read_from_csv(self, csv_file_path, attribute):
        """ Return a list of BOPRollback items from the CSV.
        """
        result = []
        with open(csv_file_path) as csv_file:
            reader = csv.reader(csv_file)
            reader.next()
            for row in reader:
                rb_address = BOPRollback._get_rb_address(row, attribute)
                result.append(rb_address)

        return  result


    @classmethod
    def _get_rb_address(cls, row, attribute):
        """ Return the RollbackAddress for the provided row
        """
        rb_address = RollbackAddress(row[0], attribute,
                                     row[1], row[2])
        if len(row) > 3:
            rb_address.err = row[3]

        return rb_address

    def _run_rollback(self, items, attribute):
        """ run the rollback with the specified list of
        rollback addresses, for the specified attribute.
        """
        for rb_address in [item for item in items if item.err == '']:
            party = ael.Party[rb_address.party_id]
            self.party_updater.update_party(party,
                                            attribute, rb_address.old_value)

    def run(self):
        try:
            self.log.write_fixing_log(["Party", "OldCountry", "NewCountry"], E_COUNTRY)
            self._run_rollback(self.countries, E_COUNTRY)

            self.log.write_fixing_log(["Party", "OldCity", "NewCity"], E_CITY)
            self._run_rollback(self.cities, E_CITY)

            self.log.write_fixing_log(["Party", "OldZipCode", "NewZipCode"], E_ZIPCODE)
            self._run_rollback(self.zipcodes, E_ZIPCODE)

            self.log.write_fixing_log(["Party", "OldAddress2", "NewAddress2"], E_ADDRESS2)
            self._run_rollback(self.address2, E_ADDRESS2)
        finally:
            self.log.close_all_logs()

def _export_all_addresses(log_path, run_time):
    """ Export to a csv file all the addresses.
    """
    file_name = "full_addresses_{0}.csv".format(run_time)

    with open(os.path.join(log_path, file_name), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        
        parties = _get_parties()
        writer.writerow(["Party", "Country", "City", "Zipcode", "Address2"])
        for party in parties:
            writer.writerow([party.ptyid, party.country,
                             party.city, party.zipcode,
                             party.address2])


def custom_run_rollback(field_values):
    """Input hook for ael_variables"""
    is_rollback = ael_variables[5].value == 'true'
    ael_variables[6].enabled = is_rollback
    ael_variables[7].enabled = is_rollback
    ael_variables[8].enabled = is_rollback
    ael_variables[9].enabled = is_rollback

    ael_variables[1].enabled = not is_rollback
    ael_variables[2].enabled = not is_rollback
    ael_variables[3].enabled = not is_rollback
    ael_variables[4].enabled = not is_rollback

    return field_values

ael_variables = AelVariableHandler()

ael_variables.add_bool(
    'commit_changes',
    label='Commit changes:',
    default=False,
    tab="Fixing"
    )

ael_variables.add_directory(
    name='log_path',
    label='Log location:',
    default=r'c:\tmp\clean\log',
    alt='The location of the created log files',
    mandatory=0,
    tab="Fixing")

ael_variables.add_input_file(
    'input_file_country',
    label='Countries fixes:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\countries.csv',
    alt='The file name (Wrong name, Correct name)',
    mandatory=0,
    tab="Fixing"
    )
ael_variables.add_input_file(
    'input_file_cities',
    label='Cities fixes:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\cities.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Fixing"
    )
ael_variables.add_input_file(
    'input_file_zipcodes',
    label='ZipCodes fixes:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\zipcodes.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Fixing"
    )


ael_variables.add_bool(
    'run_rollback',
    label='Run rollback:',
    default=False,
    hook=custom_run_rollback,
    tab="Rollback"
    )
ael_variables.add_input_file(
    'log_file_countries',
    label='Countries:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\fixing_countries.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Rollback"
    )
ael_variables.add_input_file(
    'log_file_cities',
    label='Cities:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\fixing_cities.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Rollback"
    )
ael_variables.add_input_file(
    'log_file_zipcodes',
    label='ZipCodes:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\fixing_zipcodes.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Rollback"
    )
ael_variables.add_input_file(
    'log_file_address2',
    label='Additional address:',
    file_filter='*.csv',
    default=r'c:\tmp\clean\fixing_add_addresses.csv',
    alt='The file name (...)',
    mandatory=0,
    tab="Rollback"
    )


def ael_main(params):
    """ Main entry point """

    run_time = datetime.today().strftime("%Y-%m-%d %H-%M-%S")
    commit = params['commit_changes']
    log_path = str(params['log_path'])

    _export_all_addresses(log_path, run_time)

    if params['run_rollback']:
        print 'Running rollback'
        rb_files = {'log_file_countries':str(params['log_file_countries']),
                    'log_file_cities':str(params['log_file_cities']),
                    'log_file_zipcodes':str(params['log_file_zipcodes']),
                    'log_file_address2':str(params['log_file_address2'])}
        bop_rollback = BOPRollback(commit, rb_files, log_path, run_time)
        bop_rollback.run()
    else:
        print 'Running fixing'
        fixing_files = {'input_file_country':str(params['input_file_country']),
                        'input_file_cities':str(params['input_file_cities']),
                        'input_file_zipcodes':str(params['input_file_zipcodes'])}
        bop_updates = BOPDataUpdates(commit, fixing_files, log_path, run_time)
        bop_updates.run_all()

    print 'Finished'

def _debug():

    params = {}
    params['input_file_country'] = r'c:\tmp\clean\countries.csv'
    params['input_file_cities'] = r'c:\tmp\clean\cities.csv'
    params['input_file_zipcodes'] = r'c:\tmp\clean\zipcodes.csv'
    params['run_rollback'] = False
    params['commit_changes'] = True
    params['log_path'] = r'c:\tmp\clean\log'
    
    ael_main(params)
