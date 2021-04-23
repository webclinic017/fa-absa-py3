import acm
from datetime import datetime
from gen_swift_mt940 import set_next_statement_number


def set_28C(ins, tag_28C_value):
    set_next_statement_number(
        acm.FInstrument[ins],
        acm.Time.DateToday(),
        tag_28C_value
    )
    print("Call account: %s; 28C: %s" % (ins, tag_28C_value))


def main():
    mt940_instruments = [
        "6238847-ZAR-2203-01",
        "1732445-ZAR-2201-01",
        "1300034-ZAR-2201-01",
        "3162930-ZAR-2201-01",
        "4115670-ZAR-2201-01",
        "610907-ZAR-2201-01",
        "610907-ZAR-2229-01",
        "753189-ZAR-2201-01",
        "5898021-ZAR-2203-01",
        "5830575-ZAR-2201-01",
        "4668664-ZAR-2201-01",
        "4377110-ZAR-2201-01",
    ]

    tag_28C_value = datetime.now().timetuple().tm_yday - 1
    
    print(("New value: %s" % tag_28C_value))
    for instrument in mt940_instruments:
        set_28C(instrument, tag_28C_value)

main()
