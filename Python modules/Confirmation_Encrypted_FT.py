"""
PURPOSE           : Used in PostprocessStlmConf_ATS to zip and move confirmations
                    which need to be encrypted from the Adaptiv server to a shared
                    folder where it is picked up by Integration.

================================================================================
HISTORY
================================================================================
Date        Change no           Developer               Description
--------------------------------------------------------------------------------
2017-11-07  CHNG0005091348      Willie van der Bank     Initial development.
2018-08-14  FAU-332             Stuart Wilson           Upgrade compatibility 2018
"""

import logging
import os
import shutil

from collections import defaultdict
from datetime import date
from zipfile import ZipFile
from Confirmation_Encrypted_XML import CONFIG_DICT, ZIP_NAME_PREFIX


DATA_FOLDER = CONFIG_DICT['Server_Folder']
REMOTE_FOLDER = CONFIG_DICT['Remote_Folder']


def get_files_in_folder(folder):
    return next(os.walk(folder))[2]


def group_files(folder, archive_folder):
    """Group files belonging to the same transaction."""
    try:
        abs_folder = os.path.abspath(folder)
        file_groups = defaultdict(set)
        files = get_files_in_folder(folder)

        for f in files:

            fabs = os.path.join(abs_folder, f)

            fname, ext = os.path.splitext(os.path.basename(f))
            ext = ext.lstrip('.')

            if ext == 'xml':
                file_groups[fname].add(fabs)
            if ext == 'pdf':
                fname = fname.split('_')[0]
                file_groups[fname].add(fabs)
        
        for fname, fgroup in file_groups.iteritems():
            if len(fgroup) == 1 and list(fgroup)[0].endswith('.xml'):
                print('PDF not found in default location...')
    except Exception, e:
        print('Error:', e)
    return file_groups


def create_zip(zip_name, files):
    if not zip_name.endswith('.zip'):
        zip_name += ".zip"
    try:
        zarch = ZipFile(zip_name, 'w')
        for f in files:
            zarch.write(
                f,
                os.path.join(
                    os.path.basename(zip_name).split('.')[0],
                    os.path.basename(f)
                ),
            )
    except Exception, e:
        print('Error:', e)
    finally:
        zarch.close()

    return zip_name


def move_file_to_folder(file,
                        source_folder,
                        destination_folder,
                        overwrite=False):

    source_path = os.path.join(
        source_folder,
        os.path.basename(file)
    )

    destination_path = destination_folder

    # Only file to file copy allows override see
    # >>> help(shutil.move)
    if overwrite:
        destination_path = os.path.join(
            destination_folder,
            os.path.basename(file)
        )
    shutil.move(source_path, destination_path)
    

def archive_files(archive_folder, files, overwrite):
    for src in files:
        move_file_to_folder(os.path.basename(src), os.path.dirname(src), archive_folder, overwrite)


def _process_file_group(zip_name,
                        files,
                        data_folder,
                        remote_folder,
                        archive_folder,
                        error_folder,
                        confirmation):

    group_id = os.path.basename(zip_name)
    today = date.today()

    if len(files) != 2:
        #logging.error("Invalid number of files for %s: %s/2", group_id, len(files))
        for file in files:
            # If file older than today move to error folder
            if date.fromtimestamp(os.path.getctime(file)) < today:
                move_file_to_folder(
                    file,
                    data_folder,
                    error_folder,
                    overwrite=False
                )
                logging.info("%s moved to ERROR folder.", file)
            if file.endswith('.pdf'):
                return

    if zip_name == str(confirmation.Oid()):
        try:
            zip_name = ZIP_NAME_PREFIX + zip_name
            zip_name = os.path.join(data_folder, zip_name)
            zip_fname = create_zip(zip_name, files)
        except:
            logging.exception("Unable to create zip file for %s", group_id)
            return

        try:
            move_file_to_folder(
                zip_fname,
                source_folder=data_folder,
                destination_folder=remote_folder,
                overwrite=True
            )

            archive_files(
                archive_folder,
                files,
                overwrite=True
            )
            logging.info("Processed: %s", group_id)
            return True
        except Exception, e:
            print('Error:', e)
    else:
        return


def move_zip_file_main(confirmation):
    data_folder = DATA_FOLDER
    remote_folder = REMOTE_FOLDER
    found = False
    
    try:
        os.chdir(data_folder)
        date_folder = ''
        remote_folder = os.path.join(remote_folder, date_folder)
        archive_folder = os.path.join(data_folder, 'Processed')
        error_folder = os.path.join(data_folder, "ERROR")

        # create folders
        for folder in (remote_folder, archive_folder, error_folder):
            if not os.path.exists(folder):
                os.makedirs(folder)
    except Exception, e:
        print('Error:', e)
        
    # get the files to process
    file_groups = group_files(data_folder, archive_folder)
    #print file_groups
    for zip_name, files in file_groups.iteritems():
        if _process_file_group(
            zip_name,
            files,
            data_folder,
            remote_folder,
            archive_folder,
            error_folder,
            confirmation
        ):
            found = True
    #logging.info("Processing finished successfully.")
    return found
