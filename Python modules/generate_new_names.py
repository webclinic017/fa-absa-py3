"""ABITFA-4270 Rename instruments with invalid names.

This script gets all the instruments with invalid names from Front Arena,
generates fixed names, and saves those into a tab-separated-values file.

Developer: Vojtech Sidorin
"""

import string

import ael
import acm

from at_ael_variables import AelVariableHandler


# List of forbidden characters that will be replaced.
FORBIDDEN_CHARS = r"\;,|"
# Forbidden characters will be replaced with this char.
REPLACE_CHAR = "_"
trans_table = string.maketrans(FORBIDDEN_CHARS, REPLACE_CHAR*len(FORBIDDEN_CHARS))


ael_variables = AelVariableHandler()
ael_variables.add_output_file(
        name="ofilename",
        label="Output file",
        mandatory=True,
        alt=("The list of instruments with invalid names, plus fixed names, "
             "will be saved into this tab-separated-values file."),
        )


def ael_main(kwargs):
    assert "ofilename" in kwargs
    ofilename = str(kwargs["ofilename"])
    print("Started.")
    with open(ofilename, "w") as ofile:
        ofile.write("insaddr\toriginal_insid\tnew_insid\n")  # Header line.
        print("Getting all instruments.")
        instruments = acm.FInstrument.Select("")
        print("Retrieved {0} instruments.".format(len(instruments)))
        print(("Checking instruments' names. Writing those with invalid names "
               "to file '{0}'.".format(ofilename)))
        already_taken = []  # Already taken new instrument names.
        for instrument in instruments:
            insaddr = instrument.Oid()
            original_insid = instrument.Name()
            for char in FORBIDDEN_CHARS:
                if char in original_insid:
                    new_insid = generate_fixed_name(insaddr, original_insid, already_taken)
                    already_taken.append(new_insid)
                    ofile.write("{0}\t{1}\t{2}\n".format(
                                    insaddr,
                                    original_insid,
                                    new_insid))
                    break
    print("Finished.")


def generate_fixed_name(insaddr, original_insid, already_taken):
    """Return fixed and unique insid."""
    new_insid = original_insid.translate(trans_table)
    # Make sure the new name is unique.
    if insid_exists(new_insid, insaddr) or new_insid in already_taken:
        # Try solving duplicities by altering the name.
        i = 1
        try_new_insid = "{0}_{1}".format(new_insid, i)
        while ((insid_exists(try_new_insid, insaddr) or try_new_insid in already_taken) and i < 9):
            i += 1
            try_new_insid = "{0}_{1}".format(new_insid, i)
        new_insid = try_new_insid
    if insid_exists(new_insid, insaddr) or new_insid in already_taken:
        raise Exception("Cannot generate a unique insid. The last tried "
                        "was '{0}'".format(new_insid))
    return new_insid


def insid_exists(insid, exclude_insaddr=None):
    """Return true if insid already exists in the database.

    If exclude_insaddr is given, that record will be skipped when checking
    for duplicities.
    """
    if exclude_insaddr:
        result = ael.dbsql("""
            SELECT insaddr
            FROM instrument
            WHERE insid = '{insid}'
                AND insaddr <> {insaddr}
            """.format(insid=mssql_escape(insid), insaddr=int(exclude_insaddr)))
    else:
        result = ael.dbsql("""
            SELECT insaddr
            FROM instrument
            WHERE insid = '{insid}'
            """.format(insid=mssql_escape(insid)))
    record = result[0]
    return bool(record)


def mssql_escape(text):
    """Return escaped text ready for using in MSSQL query."""
    text = str(text)
    return text.replace("'", "''")
