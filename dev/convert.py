import csv, sys

days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']

progress = 0
for day in days:
    print(day + '.csv', end = ' - ')
    rows = []

    toOpen = day

    if day == 'mo' or day == 'tu' or day == 'we':
        toOpen = 'mw'
    with open('./raw/' + toOpen + '.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            # remove garbage
            if row[0] != '' and row[0] !='Driver' and row[0] != 'Two' and row[0] != '6:05 PM &':
                rows.append(row)

    # remove header
    rows = rows[1:]

    #cleaning
    finalRows = []
    for row in rows:
        finalRow = []
        for i in range(0, len(row)):
            rowEle = row[i]
            if i == 2 and day not in days[:5]:
                finalRow.append('')
            if rowEle == '-' or rowEle == '–':
                finalRow.append('')
            else:
                finalRow.append(rowEle)
        finalRows.append(finalRow)

    with open('./data/' + day + '.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for finalRow in finalRows:
            spamwriter.writerow(finalRow)
    print('done')