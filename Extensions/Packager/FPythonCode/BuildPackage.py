import acm
import ael
import DatabaseDependenciesNetworkX as DatabaseDependencies

import FLogger
import json
import os
from PackageFileRepository import PACKAGE_DEF_FILE
import PackageInstallerParametersManager

import tempfile

import traceback
import Transporters
import TransporterExport

parameters = PackageInstallerParametersManager.ParametersManager()
logger = FLogger.FLogger(name=__name__, level = int(parameters.read('message_verbosity')))
try:
    import PackageInstallerReferences
except ImportError:
    try:
        import PackageInstallerReferencesTemplate as PackageInstallerReferences
    except:
        logger.error(traceback.format_exc())

amba_message_datetime_format = parameters.read('AmbaMessageDatetimeFormat')

ignoreClassesDefault = ['FPreferences', 'FTransactionHistory', 'FTransactionHistorySubscription', 'FUserLog', 'FServerClientProcess', 'FServerClientLog']
keepChildRecord       = ['FParameterMapping', 'FInstrumentSpreadCurveBidAsk']

def acm_to_ael(object):
    if object:
        return getattr(ael, str(object.Table().Name()))[object.Oid()]

def get_parent_object(object):
    parent = acm_to_ael(object).parent()
    if parent:
        return acm.Ael().AelToFObject(parent)
        
def get_child_objects(object):
    return [acm.Ael().AelToFObject(child) for child in acm_to_ael(object).children()]

def BuildPackageFromGraph(graph, package_manifest_objects, exclusions = None, exclusion_types = None, update_status = None):
    try:
        objects = DatabaseDependencies.GetDependencyList(graph)
        # If there are package objects not in the graph, append them to the list of dependencies.
        for package_object in package_manifest_objects:
            if package_object not in objects:
                objects.append(package_object)
                logger.debug('Added missing object')
        if not objects:
            logger.warn('No objects, no package will be built')
            return


        path = tempfile.mkdtemp()
        transportersPerClass = dict((handler.ClassName(), (name, handler)) for name, handler in Transporters.Transporter.all_handlers.items() if isinstance(handler, Transporters.XMLTransporter))
        transporterParams = dict((var[0], '') for var in TransporterExport.ael_variables)
        transporterParams['LogDefaults'] = 'True'
        ambamessages = acm.FAMBAMessage()
        ambamessages.Type("MESSAGES")
        generator = acm.FAMBAMessageGenerator()
        packageObjects = {}
        packageDefActions = []
        for object in objects:

            table = str(object.Table().Name())
            className = str(object.ClassName())
            
            ambadef = PackageInstallerReferences.amba_definition_for_class(className)
            generator.Parameters(ambadef)
            
            if className in transportersPerClass:
                packageObjects.setdefault(className, []).append(object)
            elif table == 'TextObject':
                logger.info('%-40s%-20s%-20s UNHANDLED object type, ignoring ' % (object.StringKey(), className, table))
                continue
            else:
                packageObjects['AMBA'] = 'AMBA.xml'
                if object.IsKindOf('FTrade') and not object.OptionalKey():
                    object.OptionalKey = object.Oid()
                    message = generator.Generate(object)
                    object.Undo()
                else:
                    message = generator.Generate(object)
                if message == None:
                    logger.error('Null message.')
                    raise "Null message."
                reference = DatabaseDependencies.get_attribute(graph, object, 'reference')
                reference_description = 'reference: %s' % reference
                message.AtPut('REFERENCE_TYPE', reference) 
                # Also check if this is a skipped link record.
                exclude_from_import = False
                if (exclusions and object in exclusions) or (exclusion_types and object.ClassName().AsString() in exclusion_types):
                    exclude_from_import = True
                if (PackageInstallerReferences.should_import_link_record(object) == True)  and (not exclude_from_import):
                    message.AtPut('EXCLUDE_FROM_IMPORT', 0)
                else:
                    message.AtPut('EXCLUDE_FROM_IMPORT', 1)
                logger.info('AMBA message for: %-60s%-20s %s' % (DatabaseDependencies.node_id(object), table, reference_description))
                #logger.debug(str(message))
                if className not in keepChildRecord:
                    DatabaseDependencies.remove_sub_messages(message)
                # To prevent the dreaded "inconsistent object state" with consequent mayhem,
                # we save the entity key in the message so that the message object can be fetched 
                # back into the source ADS without recreating the object from the message. This will 
                # have the state of the ADS, not the state of the message.
                message.AtPut('ORIGINAL_KEY', DatabaseDependencies.key_for_entity(object))
                if update_status != None:
                    update_status('Created AMBA message for: %s...' % DatabaseDependencies.key_for_entity(object))
                ambamessages.AddMessage(message)

        for objectType in packageObjects:
            if objectType == 'AMBA':
                packageDefActions.append({"type" : "ambamsg", "file" : packageObjects['AMBA']})
                ambaFile = os.path.join(path, packageObjects['AMBA'])
                output = acm.FCharacterOutputFileStream(ambaFile)
                acm.FTaggedMessageXMLFormatter().FormatStream(output, ambamessages)
                output.Close()
                logger.info('  Created AMBA file: %s.' % ambaFile)
                if update_status != None:
                    update_status('Created AMBA file: %s...' % ambaFile)
            else:
                name, handler = transportersPerClass[objectType]
                action = {"type" : "transporter", 'transporter': name}
                if name == "Workbook":
                    action["setDefaultContext"] = "True"
                objects = packageObjects[objectType]
                if len(objects) > 1:
                    action['folder'] = name.title().replace(' ', '') + 's'
                    folder = os.path.join(path, action['folder'])
                    os.mkdir(folder)
                else:
                    folder = path
                transporterParams['basepath'] = acm.FSymbol(folder)
                for obj in objects:                
                    objectName = handler.Names([obj])[0]
                    output = handler.ExportSingle(transporterParams, objectName)
                    if output:
                        #Modified StringToFile to return the fileName
                        file = handler.StringToFile(folder, output, objectName)
                        fileName = os.path.relpath(file, folder)
                        logger.info('  Created %s file %s' % (name, file))
                        if update_status != None:
                            update_status('Created %s file: %s...' % (name, file))
                        if not 'folder' in action:
                            action['file'] = fileName
                packageDefActions.append(action)
        fileName = os.path.join(path, PACKAGE_DEF_FILE)
        source_ads = acm.ADSAddress().strip()
        package_manifest_object_ids = []
        for object in package_manifest_objects:
            package_object_id = str(DatabaseDependencies.node_id(object))
            logger.debug('Package manifest object ID: %s' % package_object_id)
            package_manifest_object_ids.append(package_object_id)
        logger.debug('Temporary package filename: %s' % fileName)

        with open(fileName, 'w') as f:
            data = {'source_ads': source_ads, 'actions': packageDefActions, 'objects': package_manifest_object_ids}
            text = json.dumps(data, indent=4, separators=(',', ': '), encoding='latin-1')
            f.write(text)

        logger.info('  Created package definition file.')

        if update_status != None:
            update_status('Finished creating package at: %s' % path)
        return path
    except:
        logger.error(traceback.format_exc())

