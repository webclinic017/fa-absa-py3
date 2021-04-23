import ael
B = []
A = ael.ExerciseEvent.select()
for i in A:
    if i.type == 'Break':
    	print(i.type)
	B.append(i)
for c in B:
    b = c.insaddr 
    print(b.insid)
    bc = b.clone()
    for t in bc.exercise_events():
    	t.delete()
    bc.commit()
