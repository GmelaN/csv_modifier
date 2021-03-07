import csv
from collections import deque

filename = "newsList_raw_count_merged_edited"

HEADER = 0
DATE = 0
SINGLE_WORD_RANGE = 37
with open(filename + ".csv", 'r', encoding="UTF8") as f:
    content = list(csv.reader(f))

header = content[HEADER]
pairs = []

#통합할 행의 짝 구하기
for i in range((DATE + 1) + 4 , len(header)):
    if header[i - 4].replace(' ', '') == header[i].replace(' ', ''):
        pairs.append([i - 4, i])

sumList = [ header[:SINGLE_WORD_RANGE] ] # 기존 항목들의 header

for k in [header[i[0]] for i in pairs]: sumList[0].append(k)

for c in content[1:]:
    tmp = [i for i in c[:SINGLE_WORD_RANGE]] # 기존 항목을 append
    for i in range(len(pairs)):
        idx0 = pairs[i][0]
        idx1 = pairs[i][1]

        tmp.append(int(c[idx0]) + int(c[idx1])) # 합계를 append
    sumList.append(tmp)

#코로나, 우한 폐렴 통합
pairs.clear()

for i in range(len(sumList[0])):
    if sumList[0][i].count("코로나") != 0:
        pairs.append(i)
        break
for i in range(len(sumList[0])):
    if sumList[0][i].count("우한 폐렴") != 0:
        pairs.append(i)
        break

sumList[0].append("코로나_")
sumList[0].append("코로나_장전")
sumList[0].append("코로나_장중")
sumList[0].append("코로나_장외")


idx0 = pairs[0]
idx1 = pairs[1]

for i in range(1, len(content)):
    for j in range(4):
        sumList[i].append(int(sumList[i][idx0 + j]) + int(sumList[i][idx1 + j]))

with open(filename + "_pairs.csv", 'w', encoding="UTF8", newline="") as f:
    csv.writer(f).writerows(sumList)

