import acm

x = '\xa0'
rtms = acm.FPhysicalPortfolio.Select('name like "Absa*RTM*"')

to_fix = [r for r in rtms if x in r.Name()]

for portf in to_fix:
    old_name = portf.Name()
    new_name = old_name.replace(x, ' ')
    print("'%s' -> '%s'" %(old_name, new_name))
    portf.Name(new_name)
    portf.Commit()
