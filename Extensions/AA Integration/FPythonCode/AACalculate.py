""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AACalculate.py"
"""----------------------------------------------------------------------------
MODULE
    AACalculate - Static class containing all AA attributes and
        calculate function pointer.

    (c) Copyright 2019 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import collections
import os
import platform
import re
import sys

import AAAttributes
import importlib
importlib.reload(AAAttributes)
import AAIntegrationUtility
importlib.reload(AAIntegrationUtility)

# Calculate should be treated as a singleton container/wrapper
# containing AA engine activator instance and static information.
class Calculate(object):
    __ATTRIBUTES = None
    __CALCULATE_REQUEST_SENDER = None
    __Responses = collections.namedtuple(
        'Responses', 'infos warnings errors unparsed'
    )

    @staticmethod
    def initialise(attributes=None):
        if Calculate.__ATTRIBUTES is None:
            Calculate._initialise(attributes)

        return

    @staticmethod
    def reinitialise(attributes=None):
        assert Calculate.__ATTRIBUTES, __name__ + ' not initialised'
        Calculate._cleanLibPath(ref_path=Calculate.__ATTRIBUTES['LIB_PATH'])
        importlib.reload(AAAttributes)
        Calculate.__ATTRIBUTES = None
        Calculate._initialise(attributes)
        return

    @staticmethod
    def getAttributes():
        assert Calculate.__ATTRIBUTES, __name__ + ' not initialised'
        return Calculate.__ATTRIBUTES.copy()

    @staticmethod
    def sendRequest(request):
        assert Calculate.__ATTRIBUTES, __name__ + ' not initialised'
        response = Calculate.__CALCULATE_REQUEST_SENDER(request, 1)
        print(response)
        response = response.encode('ascii', 'ignore')
        response_break_down = Calculate._parseResponse(response)
        response = Calculate.__Responses(*response_break_down)
        return response

    @staticmethod
    def _cleanLibPath(ref_path):
        get_path = lambda path: \
            AAIntegrationUtility.forwardSlashedPath(path=path, real=True)
        ref_path = get_path(path=ref_path)
        for idx, p in reversed(list(enumerate(sys.path))):
            if get_path(path=p) == ref_path:
                sys.path.pop(idx)
        return

    @staticmethod
    def _initialise(attributes):
        assert Calculate.__ATTRIBUTES is None, __name__ + ' already initialised'
        if (platform.system() != 'Windows') or \
            (platform.architecture()[0].lower() != '64bit'):
            raise Exception('AA libraries cannot be imported on this machine')

        try:
            import clr
        except:
            raise Exception('Could not import module clr')

        attrs = {}
        attrs.update(AAAttributes.ATTRIBUTES)
        attrs.update(attributes)
        lib_path = AAIntegrationUtility.forwardSlashedPath(
            path=attrs['LIB_PATH'], real=True
        )
        if os.path.isdir(lib_path):
            Calculate._cleanLibPath(ref_path=lib_path)
            sys.path.insert(0, lib_path)
        else:
            raise Exception('Invalid AA path: %s' % lib_path)
        
        #new call:
        #SunGard.Adaptiv.Analytics.Analysis.ArtiqHost.Instance.StartDataService()
        if attrs['START_MEMORY_CUBE_SERVICE']:
            mod_name = 'SunGard.Adaptiv.Analytics.Analysis'
            ISH = None
            try:
                import SunGard.Adaptiv.Analytics.Analysis as SAAA
                assert SAAA.__name__ == mod_name
            except:
                msg = 'Could not import %s from LIB_PATH=%s' % (mod_name, lib_path)
                raise Exception(msg)

            try:
                SAAA.ArtiqHost.Instance.StartDataService()
            except Exception as e:
                raise Exception('Failed to start Memory Cube data service: ' + str(e))
        
        mod_name = 'SunGard.Adaptiv.Analytics.Framework'
        AA = None
        try:
            import SunGard.Adaptiv.Analytics.Framework as AA
            assert AA.__name__ == mod_name
        except:
            msg = 'Could not import %s from LIB_PATH=%s' % (mod_name, lib_path)
            raise Exception(msg)

        engine_activator = None
        try:
            engine_activator = AA.EngineActivator()
        except Exception as e:
            raise Exception('Could not instantiate ' + mod_name + ': ' + e)

        Calculate.__CALCULATE_REQUEST_SENDER = engine_activator.Calculate
        Calculate.__ATTRIBUTES = {}
        Calculate.__ATTRIBUTES['LIB_PATH'] = lib_path
        Calculate.__ATTRIBUTES['START_MEMORY_CUBE_SERVICE'] = \
            attrs['START_MEMORY_CUBE_SERVICE']
        return

    @staticmethod
    def _parseResponse(response):
        def findAll(severity):
            type1 = []
            for result in re.findall(getRegexType1(severity), response.decode()):
                if result != 'Beginning staged calculation.' and \
                    result != 'Finished staged calculation.':
                    type1.append(result)

            type2 = []
            for result in re.findall(getRegexType2(severity), response.decode()):
                result = result.replace('">', '": ')
                result = result.replace('Summary=', 'RowID=')
                type2.append(result)

            responses = map(cleanResponse, type1 + type2)
            unique_responses = []
            for r in responses:
                if r not in unique_responses:
                    unique_responses.append(r)

            return unique_responses

        def getRegexType1(severity):
            return r'<Error Severity="%s">(.*)</Error>' % severity

        def getRegexType2(severity):
            return r'<Error Severity="%s" (.*)</Error>' % severity

        def cleanResponse(response):
            response = response.replace('&#xD;&#xA;', '').replace('   ', '\n   ')
            split = response.rsplit('\n', 1)
            if len(split) == 2:
                response, last_line = split
                response += '\n' + '\n'.join(last_line.split('": ', 1))

            return response

        infos = findAll('Information')
        warnings = findAll('Warning')
        errors = findAll('Error')
        return infos, warnings, errors, response
