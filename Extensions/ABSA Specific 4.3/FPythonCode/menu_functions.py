import acm


def start_application(eii):
    application = eii.Definition().Name()
    acm.StartApplication(application, None)
