import acm, ael
import FMacroGUI
import TradeBucketGUI
import csv
import os

directorySelection = acm.FFileSelection()
directorySelection.PickDirectory(True)
directorySelection.SelectedDirectory('C:/')
ael_gui_parameters = {'windowCaption':'SAGEN Trade Buckets BO report'}
parties = acm.FParty.Select('')
default_name = 'SAGEN_Trade_Buckets_BO'

ael_variables = [
    ['file_name', 'File Name',
     'string', None, default_name, 1, 0,
     'The output file name. A date stamp will be added automatically.', None, 1],
    ['output_directory', 'Output Directory',
     directorySelection, None, directorySelection, 1, 1,
     'The directory where the report(s) will be generated.', None, 1],
    ['acquirer', 'Acquirer',
     'string', parties, None, parties, 0, 1,
     'Choose the acquiring party for which the report will be run.', None, 1],
    ['details', 'Details',
     'string', ['No', 'Yes'], 'Yes', 1, 0,
     'Show details.', None, 1]
]

def ael_main(parameters):
    # get the params
    output_directory = str(parameters['output_directory'].SelectedDirectory())
    acquirer = parameters['acquirer']
    show_details = parameters['details']
    file_name = parameters['file_name']

    # check the path
    if not os.path.isdir(output_directory):
        raise ValueError('"{0}" is not a valid directory.'.format(output_directory))

    # build the filename
    if file_name.endswith('.csv'):
        file_name = file_name[:-4]

    today = ael.date_today().to_ymd()
    today_str = "-".join(map(lambda i: str(i).zfill(2), today))

    file_name += '_' + today_str + '.csv'

    # polish the acquirer field
    if not acquirer:
        acquirer = 'All'

    # get the query text and macros
    query_text = acm.FSQL['SAGEN_Trade_Buckets_BO'].Text()
    macros = FMacroGUI.searchMacros(query_text)
    bindings = {'1_Acquirer': acquirer,
                '2_ShowDetails': show_details}

    # fill the params
    macro_list, value_list = FMacroGUI.mapMacros(bindings, macros)

    # run the query
    res = ael.asql(query_text, 0, macro_list, value_list)

    with open(os.path.join(output_directory, file_name), 'wb') as csvfile:
        writer = csv.writer(csvfile)

        # write the header
        writer.writerow(res[0][:14]+['Comments']+res[0][14:])

        # process and write the rows
        for table in res[1]:
            for row in table:
                # the textobject records are pulled here because in ASQL, the data length
                # is limited to 256 characters
                text_object = ael.TextObject.read(
                    'type="Customizable" and name="{0}"'.format(row[8]))

                if text_object:
                    comments = TradeBucketGUI.get_formatted_comments(text_object)
                else:
                    comments = ''

                new_row = list(row)
                new_row = new_row[:14]+[comments]+new_row[14:]
                writer.writerow(new_row)

    fileName = output_directory + "/" + file_name
    print("Wrote secondary output to " + fileName)
    print("completed successfully")

