import acm

for text_object in acm.FCustomTextObject.Select("").AsArray():
    if text_object.Name().startswith('ATS_SINGLETON'):
        print(('Removing singleton entry: {entry}'.format(
            entry = text_object.Name()
        )))
        text_object.Delete()
