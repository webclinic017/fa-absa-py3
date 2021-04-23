import acm

diary = acm.FSettlementDiary.Instances()
diarylist = list(diary)
count = 0
while len(diarylist) > 0:
    record = diarylist.pop()
    text = record.Text()
    if ('<PayDate>2017-06-05</PayDate>' in text and 'Status="Sent"' in text):
        print(text)
        count += 1
        record.Delete()

print(count)
