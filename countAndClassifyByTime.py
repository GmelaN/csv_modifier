'''
뉴스 기사를 읽어 키워드 빈도를 계산하는 프로그램
이 때 빈도는 제목과 부제 각각 단어의 합임
맥락을 고려한 단어 세기 필요 => ex> 코로나, 사망자 모두 > 0이면 "코로나 사망자"++
'''

import csv

TITLE = 0
SUBTITLE = 1
DATE = -2
TIME = -1

csvFile = "./newsList_raw"

with open(csvFile + ".csv", 'r', encoding="utf8", newline="") as f:
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

wordList_keywords = [ list(wordList.keys())[i] for i in range(0, len(wordList.keys()), 4) ]



listToWrite = [([i for i in wordList.keys()] + ["날짜", "시각"])] # 기록할 최종 리스트 - 헤더 행을 미리 append한 상태임

for news in c[1:]:
    for word in wordList_keywords:
        newsString = news[TITLE] + news[SUBTITLE] # 한 기사의 제목, 부제 행 정보를 담은 문자열
        sum_ = newsString.count(word) # newsString으로부터 키워드 횟수를 구함

        # sum_ = news[TITLE].count(word) + news[SUBTITLE].count(word)

        # 한 기사에서 word가 나온 횟수를, word 횟수의 총합 변수에 더함
        wordList[word] += sum_

        # 시간대별 합 => 해당 기사의 개재 시각을 봄
        time = int(news[TIME])
        if 0 <= time < 90000:
            timeStr = " 장전"
        elif 90000 <= time < 153000:
            timeStr = " 장중"
        elif 153000 <= time <= 235959:
            timeStr = " 장외"

        #wordList의 "### 장*" 항목에 한 기사에서 word가 나온 횟수를 더함
        wordList[word + timeStr] += sum_

    # write할 최종 리스트에 현재 기사의 키워드 빈도 결과 리스트를 append
    listToWrite.append(
        list(wordList.values()) + [news[DATE], news[TIME]]
        )
    
    #wordList item을 모두 0으로 초기화
    for word in wordList.keys():
        wordList[word] = 0

with open(csvFile + '_count.csv', 'w', encoding="utf8", newline="") as w:
    csv.writer(w).writerows(listToWrite)

print("작업 완료, 다음에서 찾을 수 있음:", csvFile + '_count.csv')
