import csv

filename = "newsList_raw_count"

HEADER = 0
DATE = -2
TIME = -1
CORONA = 2

with open(filename + ".csv", 'r', encoding="UTF8") as f:
    content = list(csv.reader(f))

header = content[HEADER][:-1] # 필요하지 않은 항목은 여기서 제거 후 사용
listToWrite = [header]

sumList = [0 for _ in range(len(header) - 1)] # 41

standardDate = content[1][DATE]

for news in content[1:]:
    if news[DATE] != standardDate: # 다음 날짜를 마주침
        listToWrite.append(sumList + [standardDate]) # 지금까지 더해왔던 합계를 출력
        standardDate = news[DATE] # 새 기준 날짜는 '다음 날짜'가 됨

        for i in range(len(sumList)): sumList[i] = 0 # 합계 초기화

    for i in range(len(sumList)): # 합계에 카운트한 행들을 더함
        sumList[i] += int(news[i])

listToWrite.append(sumList + [standardDate]) # 마지막 날 합계
        
with open(filename + "_merged.csv", 'w', encoding="UTF8", newline="") as f:
    csv.writer(f).writerows(listToWrite)
