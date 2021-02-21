"""
    중간 중간 누락된 날짜의 데이터를 이전 날짜의 데이터로 덮어씌우는 프로그램
    파일의 첫 행은 항상 헤더가 있어야 함
    날짜는 CSV 파일 첫 번째 위치에 있어야 함
"""
import csv
import datetime
import locale

locale.setlocale(locale.LC_ALL, "ko_KR.UTF8")

DATE = -3
TIME = -2
CORONA = 0
WOHAN = 1

weekdays = ['월', '화', '수', '목', '금', '토', '일']
filename = "newsList_raw_count"

with open(filename + ".csv", 'r', encoding="UTF8", newline="") as f:
    content = list(csv.reader(f))

#header 기록
listToWrite = [ (content[0] + ["시간대", "요일", "코로나 + 우한 폐렴"]) ]

for news in content[1:]:
    d = datetime.date(
        int(news[DATE][:4]),
        int(news[DATE][4:6]),
        int(news[DATE][6:])
    ).weekday() # 뉴스의 날짜에 해당하는 요일

    tmp = []

    for n in news: tmp.append(n) # 행 정보 담기

    if weekdays[d] == '토' or weekdays[d] == '일':
        tmp.append('주말') # 주말인 경우 '주말'
    else:
        time = int(news[TIME]) # 시간 정보
        if time < 90000: tmp.append("장전") # 85959는 08:59:59와 같은 의미 => 0~85959는 장전
        elif time < 153000: tmp.append("장중") # 90000~152959 => 9:00:00~15:29:59는 장중
        else: tmp.append("장후") # 나머지 범위는 장후

    tmp.append(weekdays[d]) # 요일 정보 담기
    tmp.append(int(news[CORONA]) + int(news[WOHAN]))

    # print(news[TIME], '\t', tmp[-1])

    listToWrite.append(tmp) # 파일에 기록될 리스트에 담기

with open(filename + "_classified.csv", 'w', encoding="UTF8", newline="") as f:
    print("기록 중...")
    csv.writer(f).writerows(listToWrite)

input("완료! 종료하려면 엔터 키를 누르십시오...")