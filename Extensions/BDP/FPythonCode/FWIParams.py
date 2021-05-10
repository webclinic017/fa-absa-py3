""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/wi_processing/etc/FWIParams.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FWIParams - Parameters for the When Issue procedure.

DESCRIPTION
    Extracts and computes parameters for the When Issue procedure. Also
    performs processing or rollback.

----------------------------------------------------------------------------"""


import ael


import FWIGeneral


class FWhenIssued:
    """------------------------------------------------------------------------
    CLASS
        FWI - Parameters for When Issue.
    INHERITS
        FWIProcessing
    DESCRIPTION
        The class extracts all parameters needed to perform When Issue
        processing.
    CONSTRUCTION
        tradefilter Tradefilter  A tradefilter in which all trades are included
                                 that should be considered for processing
        ins         Instrument   The instrument to which processed trades will
                                 belong.
        verbosity   int          Integer that indicate the level of information
                                 that will be generated in the AEL console
    ------------------------------------------------------------------------"""

    def __init__(self, tradefilter, ins, verb):
        """
        Constructor. Initialize and start When Issue processing.
        """
        self.tradefilter = tradefilter
        self.instrument = ins
        self.verb = verb
        self.l = {}

    def get_ins_and_trds_for_processing(self):

        trds = ael.TradeFilter[self.tradefilter[0]].trades()
        for t in trds:
            ins = t.insaddr
            if (ins.incomplete == 'Unprocessed WI' and
                    t.status == 'FO Confirmed'):
                if ins in self.l:
                    self.l[ins].append(t)
                else:
                    self.l[ins] = [t]
        for i in self.l:
            FWIGeneral.log(2, self.verb, i.insid)
            for t in self.l[i]:
                FWIGeneral.log(2, self.verb, '   %s' % t.trdnbr)

    def get_ins_and_trds_for_rollback(self):

        trds = ael.TradeFilter[self.tradefilter[0]].trades()
        for t in trds:
            found = 0
            t_orig = t
            if t.correction_trdnbr and t.status == 'FO Confirmed':
                t2 = t.correction_trdnbr
            while found == 0:
                if (t2.status == 'Simulated' and
                        t2.insaddr.incomplete == 'Unprocessed WI'):
                    found = 1
                    t_orig = t2
                elif (t2.status == 'Void' and t2.correction_trdnbr and
                        t2.correction_trdnbr != t2):
                    t2 = t2.correction_trdnbr
                else:
                    found = 1
            if (found and t_orig):
                if t_orig.insaddr in self.l:
                    self.l[t_orig.insaddr].append(t)
                else:
                    self.l[t_orig.insaddr] = [t]
        for i in self.l:
            FWIGeneral.log(2, self.verb, i.insid)
            for t in self.l[i]:
                FWIGeneral.log(2, self.verb, '   %s' % t.trdnbr)

    def process_wi(self):
        for i in self.l:
            if i.insaddr == ael.Instrument[self.instrument]:
                FWIGeneral.log(2, self.verb, 'New trades are created in the '
                        'original instrument %s' % i.insid)
            else:
                FWIGeneral.log(2, self.verb, 'New trades are created in the '
                        'given instrument %s' % self.instrument)
            for t in self.l[i]:
                try:
                    t_new = t.new()
                    t_new.correction_trdnbr = t.trdnbr
                    t_new.insaddr = ael.Instrument[self.instrument]
                    t_new.status = 'FO Confirmed'
                    ins = ael.Instrument[self.instrument]
                    if ins.quote_type == 'Pct of Nominal':
                        d = ael.date(t.value_day.to_string())
                        t_new.price = ins.dirty_from_yield(d, None, None,
                                t.price)
                    t_new.commit()
                    FWIGeneral.log(2, self.verb, 'Created new trade: %s' %
                            t_new.trdnbr)
                    t_clone = t.clone()
                    t_clone.status = 'Simulated'
                    t_clone.archive_status = 1
                    t_clone.commit()
                    FWIGeneral.log(2, self.verb, 'Trade %s, has been '
                            'Processed, Archived and set to Simulated' %
                            t.trdnbr)
                    ael.poll()
                except Exception:
                    FWIGeneral.log(0, self.verb, 'Commit() failed when '
                            'Processing trades')
            ael.poll()

    def rollback_wi(self):
        for i in self.l:
            for t in self.l[i]:
                found = 0
                t_orig = t
                if (t.correction_trdnbr and t.status == 'FO Confirmed'):
                    t2 = t.correction_trdnbr
                while found == 0:
                    if (t2.status == 'Simulated' and
                            t2.insaddr.incomplete == 'Unprocessed WI'):
                        found = 1
                        t_orig = t2
                    elif (t2.status == 'Void' and t2.correction_trdnbr and
                            t2.correction_trdnbr != t2):
                        t2 = t2.correction_trdnbr
                    else:
                        found = 1
                try:
                    tprocessed_clone = t.clone()
                    tprocessed_clone.status = 'Void'
                    tprocessed_clone.commit()
                    FWIGeneral.log(2, self.verb, 'Trade %s, has been '
                            'rollbacked and set to Void' % t.trdnbr)
                    torig_clone = t_orig.clone()
                    torig_clone.status = 'FO Confirmed'
                    torig_clone.archive_status = 0
                    torig_clone.commit()
                    FWIGeneral.log(2, self.verb, 'Trade %s, has been set to '
                            'Non-Archived and FO Confirmed' %
                            torig_clone.trdnbr)
                except Exception:
                    FWIGeneral.log(0, self.verb, 'Commit() failed when '
                            'Rollbacking trades')
