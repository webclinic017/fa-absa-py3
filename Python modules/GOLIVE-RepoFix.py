import acm

grp = acm.FChoiceList['ValGroup']
repo = acm.FChoiceList['AC_GLOBAL_Repos']
if not repo:
    bond = acm.FChoiceList['AC_GLOBAL_Bonds']
    repo = bond.Clone()
    repo.Name('AC_GLOBAL_Repos')
    repo.Description('Val group for repos')
    repo.Commit()

for i in acm.FRepo.Instances():
    old_val_group = i.ValuationGrpChlItem().Name()
    i.ValuationGrpChlItem(repo)
    i.Commit()
    print(i.Name(), old_val_group, " =>", i.ValuationGrpChlItem().Name())
