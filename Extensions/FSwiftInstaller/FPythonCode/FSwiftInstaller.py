from SwiftInstaller_Utilities import install_SwiftSolution_modules, notifier, SwiftInstaller


def ael_main(variables_dictionary):
    notifier.INFO("Installing SwiftSoultion modules")

    install_SwiftSolution_modules(variables_dictionary)

    #notifier.INFO("Done Installing SwiftSoultion modules")


# Call Swift Installer Task GUI

ael_gui_parameters = {'windowCaption': "SwiftSolution Installer"}

ael_variables = SwiftInstaller()
ael_variables.LoadDefaultValues(__name__)


