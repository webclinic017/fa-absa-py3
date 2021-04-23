import acm, ael

ai_specs = acm.FAdditionalInfoSpec.Select('')

ret = []
for ai_spec in ai_specs:
    msg = '\rChecking spec %i (%s on %s)' % (ai_spec.Oid(), ai_spec.Name(), ai_spec.RecType())
    print(msg, end=' ')
    ai_cnt = ael.dbsql('SELECT COUNT(*) FROM additional_info WHERE addinf_specnbr = %i' % ai_spec.Oid())[0][0][0]
    if ai_cnt == 0:
        print('No addinfos for spec number %i (%s)!' % (ai_spec.Oid(), ai_spec.Name()))
        ret.append(ai_spec)

print("\nFor deletion")
print("==============")
for spec in ret:
    print('Specnbr: %i, "%s" on "%s"' % (spec.Oid(), spec.Name(), spec.RecType()))
