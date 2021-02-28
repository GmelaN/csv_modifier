import csv

filename = "newsList_raw_countmerged"

HEADER = 0
DATE = -1
CORONA = 0
WOHAN = 4

with open(filename + ".csv", 'r', encoding="UTF8") as f:
    content = list(csv.reader(f))

header = content[HEADER][:4]
listToWrite = [header]

sumList = [0 for _ in range(len(header))]

standardDate = content[HEADER + 1][DATE]

for news in content[HEADER + 1:]:
    if news[DATE] != standardDate: # 다음 날짜를 마주침
        listToWrite.append(sumList + [standardDate]) # 지금까지 더해왔던 합계를 출력
        standardDate = news[DATE] # 새 기준 날짜는 '다음 날짜'가 됨

        for i in range(len(sumList)): sumList[i] = 0 # 합계 초기화

    for i in range(len(sumList)):
        sum_ = (int(news[CORONA + i]) + int(news[WOHAN + i]))
        if sum_ != 0: print(i, news[CORONA + i], '\t', news[WOHAN + i], '\t', sum_)
        sumList[i] += sum_

listToWrite.append(sumList + [standardDate])

with open(filename + "merged.csv", 'w', encoding="UTF8", newline="") as f:
    csv.writer(f).writerows(listToWrite)
