import acm

tasks = acm.FAelTask.Select('name like "*LIVE_PrfView_SERVER"')

def update_task(task, key, new_val):
    params = task.Parameters()
    orig_val = params.At(key)
    params.AtPutStrings(key, new_val)
    new_val_added = params.At(key)
    print("Updating '%s'['%s']: '%s' => '%s'" %(task.Name(), key, orig_val, new_val_added))
    params.Commit()
    task.Parameters(params)
    task.Commit()

for t in tasks:
    if t.ModuleName() == 'FWorksheetReport':
        update_task(t, "instrumentRows", "True")
