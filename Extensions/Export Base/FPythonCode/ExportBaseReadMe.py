""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/ExportBaseReadMe.py"
"""
ABOUT
=====

NOTE: This document serves as a guide to developers looking to create or set up a new export.

The Export Base module provides a framework primarily for developing integrations with prime 
brokers and fund administrators. However, use of the framework is not restricted to this purpose.

An example of an integration using this framework is that with prime broker Morgan 
Stanley, available in the module "AMI Morgan Stanley". This module serves as a working, fully 
documented example of how this framework is intended to be used.

Further developer documentation related to this module is available in FCA 4573
"Developer Guide: Business Data Export".


MODULES
=======

 The Export Base module consists of the following FPythonCode extension modules:

 - FAssetManagementUtils, FExportUtils
        Common utility functions.

 - FBusinessProcessUtils
        Helper functions for error handling in business processes.

 - FSyncronizeBPWithTransHist
        Creates and updates business processes based on trade status transitions.
        Used to initialise the export process and identify events that may require 
        a re-export of modified data.

 - FColumnToXMLGenerator
        Responsible for generating XML used in creating files/reports, mapping data 
        to an exportable format.

 - FExportProcess
        Core classes used in the run-time processing of an export. These classes are 
        used to represent an instance of a export process, which is consumed and
        updated by the various processing engines within the framework.

 - FFileCreator
        Creates export files/reports from generated XML data (see FColumnToXMLGenerator).

 - FFileTransporter
        Classes for transferring files to remote destinations over a variety of 
        transport methods (e.g. S/FTP, email).

 - FIntegration
        Contains the core class defining the integration in its entirety. Specific 
        needs of an integration can be supported through callback hooks set on an
        instance of this class, defining everything from the location of required 
        configuration items, to the export file format and transfer process.

 - FSingleExportIdentifier
        Contains the identifier class for an exportable file/report.

 - FRunScriptBase
        Classes and functions to assist in building custom run script user 
        interfaces for export purposes.

 - FTransactionHistoryReader
        Classes used for detecting changes in stored objects based on events
        recorded in their transaction history.


EXPORT PROCESS OVERVIEW
=======================

The export of data to prime brokers and fund administrators is realised by the 
following architectural elements:

    A) The Export Base extension module, containing core export processing functionality.
    B) An extension module defining integration specific behaviour and setup.
    C) Pre-defined ACM queries (a.k.a insert item queries) identifying exportable items.
    D) Sheet template(s) defining exportable fields and data mapping.
    E) Business processes used for tracking the state of exportable items.

Creating an export for a new integration will typically involve the following steps:

NOTE: The following contains both steps required in creating/packaging a new integration,
      and steps that are commonly done during the installation of said integration.
      Where appropriate, installation steps must also be explicitly stated in the 
      installation documentation provided by the integration.

 1. Ensure that the "Export Base" module is in your context.
 2. Create a new extension module for the integration. By convention, this module
    should be called "AMI <Party Name>". 

    This module should include:

      - A definition of the FIntegration class, the configuration of which will
        establish all behavioural aspects of the export processing (e.g. business
        process state chart, notable trade transitions, file output format, export
        file transfer, etc).
      - Column definitions (and supporting Python functions) to map data to exportable 
        fields via the sheet template(s).
      - (optional) The XLSLT template for formatting the export file.
      - A run-script GUI definition, or equivalent method, for invoking the export
        processing made available by the framework.
      - A Python module serving as a read-me/guide for the installation of the 
        integration should be provided.
    
    Refer to the "AMI Morgan Stanley" module for more detailed information on these
    components and how they can be implemented.

 3. Create ACM queries (a.k.a. insert item queries) to select trades or other ACM 
    objects to be exported. Separate queries can be defined to allow for different 
    items to be exported over various export runs (e.g. export by product type). 
    All queries should be named with the prefix defined by the integrations 
    FIntegration object, such that they can be located during export processing.
 4. Create sheet templates to define the fields to be contained in the export files
    as columns, in accordance to the integration party's specification. 
    The "Column Creator" tool can be used for this purpose. These sheet templates 
    must be locatable by the FIntegration object through its configuration.
 5. Create a business process state chart representing the workflow of the export
    process. This state chart will be used to manage an exportable item through its
    various export states, both by the user and the export framework.
    A single event in the state chart is used to represent the act of exporting data
    and is used by the framework to determine when to do so. The name of this event,
    the name of the state chart itself, and how changes in the export objects 
    correspond to events in the state chart is determined by the FIntegration object.

Data changed within the system after export typically necessitates a re-export of the
changed object to notify the external system of this change (e.g. the voiding of a 
trade). 

The export framework utilises a custom trade status and transaction history functionality 
to detect these changes. Changes to exported trades then invoke corresponding changes to 
the export business process, causing them to be exported again as appropriate.

To enable use of this portion of the framework (it is possible to create/use a functional 
alternative if desired), additional configuration must be made to a default Front Arena 
installation:

 6. Transaction history must be enabled/configured on the ADS:
      - Transaction history must be enabled for trades.
      - The "history free text" setting must be set to map the trade status
        attribute to the transaction history description field.

    Refer to FCA 1327 "System Administration: ADS (Windows)" or FCA 1264 "System 
    Administration: ADS (Solaris and Linux)" for detailed configuration instructions.
 7. An additional trade status will need to be introduced (e.g. "FO Amend") to flag
    manual changes made to trades post-export (e.g. after "BO Confirmed"). This should 
    be configured as part of the trade transitions in the integrations FIntegration object.


"""

