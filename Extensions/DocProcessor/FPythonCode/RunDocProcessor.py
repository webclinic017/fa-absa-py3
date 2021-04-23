import DocProcessor


ael_variables = [['path', 'thepath', 'string', "", None, 0, 0, 'whatevah', None, 1]]

def ael_main(args):
    DocProcessor.process(maillist=["gary.niemen@sungard.com", "rickard.bergelius@sungard.com"], alwaysConfirmwithMail=False, verboseOutput=False, xmrlocation=args['path'])  

