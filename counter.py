'''
뉴스 기사를 읽어 키워드 빈도를 계산하는 프로그램
이 때 빈도는 제목과 부제 각각 단어의 합임
'''

import csv

TITLE = 0
SUBTITLE = 1
DATE = -2
TIME = -1

csvFile = "./newsList_raw"

f = open(csvFile + ".csv", 'r', encoding="utf8", newline="")
c = list(csv.reader(f))

wordList = {
    "코로나": 0, "코로나 장전": 0, "코로나 장중": 0, "코로나 장외": 0,
    "우한 폐렴": 0, "우한 폐렴 장전": 0, "우한 폐렴 장중": 0, "우한 폐렴 장외": 0,
    "제약":0, "제약 장전":0, "제약 장중":0, "제약 장외":0,
    "바이오":0, "바이오 장전":0, "바이오 장중":0, "바이오 장외":0, 
    "백신":0, "백신 장전":0, "백신 장중":0, "백신 장외":0,
    "바이러스":0, "바이러스 장전":0, "바이러스 장중":0, "바이러스 장외":0,
    "확진":0, "확진 장전":0, "확진 장중":0, "확진 장외":0,
    "누적":0, "누적 장전":0, "누적 장중":0, "누적 장외":0,
    "사망":0, "사망 장전":0, "사망 장중":0, "사망 장외":0,
    "신규":0, "신규 장전":0, "신규 장중":0, "신규 장외":0
    }



listToWrite = [([i for i in wordList.keys()] + ["날짜", "시각"])]

for news in c[1:]:
    for word in [list(wordList.keys())[i] for i in range(0, len(wordList.keys()), 4)]:
        sum_ = news[TITLE].count(word) + news[SUBTITLE].count(word)
        # 총합
        wordList[word] += sum_

        # 시간대별 합
        time = int(news[TIME])
        if time < 90000:
            timeStr = " 장전"
        elif time < 153000:
            timeStr = " 장중"
        else:
            timeStr = " 장외"

        wordList[word + timeStr] += sum_

    listToWrite.append(
        list(wordList.values()) + [news[DATE], news[TIME]]
        )
    
    #wordList item을 모두 0으로 초기화
    for word in wordList.keys():
        wordList[word] = 0

with open(csvFile + '_count.csv', 'w', encoding="utf8", newline="") as w:
    csv.writer(w).writerows(listToWrite)

f.close()