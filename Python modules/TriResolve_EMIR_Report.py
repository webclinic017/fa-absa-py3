# coding=ascii
"""
Brendan Bosman      MINT-164.3      2015/09/01      1. Created as part of a refactoring process of TriResolve_EMIR.py
Brendan Bosman      MINT-366        2015/09/15      Implement Non EU files

Main Purpose:
1. Class declarations of EmirReportGenerator

To the developers working on this file:
1. This file was taken rom FA where tabsstop was equal to 8 spaces. In FA, most of the indention was 4 space, so
   reading the outside of FA was difficult if tabstop was not 8 spaces. Please be aware of this
2. Going forward, all indentions are 4 spaces, but tabstop is still 8
"""

import TriResolve_EMIR_Exporter
import TriResolve_EMIR_Context


class EmirReportGenerator(object):
    """Generates EMIR report."""

    def __init__(self, ctx):
        """

        :type ctx: BaseEMIRContext
        :type self: EmirReportGenerator
        """
        self.context = ctx

    @property
    def get_context(self):
        """

        :rtype : TriResolve_EMIR_Context.BaseEMIRContext
        :return:
        """
        return self.context

    def run(self):
        """Generate the report. This is the main method of this class."""

        self.get_context.print_params()
        with open(self.get_context._output_path, 'wb') as f:

            if self.get_context._is_front_arena_data_run:
                run = TriResolve_EMIR_Exporter.EMIRFrontArena(self.get_context)
                fieldnames = run.create_fieldnames()
                writer = run.create_writer(f)
                header_row = dict((k, k) for k in fieldnames)
                writer.writerow(header_row)  # writeheader added in Python 2.7 :P
                run.run(writer)

                # Testing switch
                assert isinstance(self.context, TriResolve_EMIR_Context.BaseEMIRContext)
                if self.context.get_write_to_log_test():
                    run.write_error("Hello test. this is a test message")
            else:            
                run = TriResolve_EMIR_Exporter.EMIRMidasTrades(self.get_context)
                fieldnames = run.create_fieldnames()
                writer = run.create_writer(f)
                header_row = dict((k, k) for k in fieldnames)
                writer.writerow(header_row)  # writeheader added in Python 2.7 :P

                # Process only Midas data
                print("Processing Midas trades.")

                run.run(writer)
