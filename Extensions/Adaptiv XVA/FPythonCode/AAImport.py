""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAImport.py"
import platform
import sys

if platform.system() == 'Windows':

    import AAParamsAndSettingsHelper
    logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

    try:
        import clr
    except:
        logger.ELOG("Could not import module clr")

    try:
        PATH = AAParamsAndSettingsHelper.getAdaptivPath()
        if PATH not in sys.path:
            sys.path.insert(0, PATH)
    except Exception as e:
        logger.ELOG(str(e))

    try:
        import SunGard.Adaptiv.Analytics.Framework
    except:
        logger.ELOG("Could not import SunGard.Adaptiv.Analytics.Framework")
    ea = SunGard.Adaptiv.Analytics.Framework.EngineActivator()
