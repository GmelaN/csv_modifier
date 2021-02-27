"""
    일정 기간 동안의 종목 종가를 불러오는 프로그램
"""

import FinanceDataReader as fdr
import pandas as pd

print("***실행 전 소스 코드를 편집하여 종목 데이터를 지정하여야 합니다! (17번째 줄)***")

startDate = input("수집을 시작할 날짜를 입력하세요 (\"yyyy-mm-dd\"): ")
endDate = input("수집을 종료할 날짜를 입력하세요 (\"yyyy-mm-dd\"): ")

title = input("결과를 저장할 csv 파일의 이름을 입력하세요(기본값: stocks): ").strip().replace(' ', '_')
if not title: title = "stocks"

# 불러올 종목의 {종목 코드: 종목 이름}
stocks = {
    '207940': "삼성바이오로직스",
    '068270': "셀트리온",
    '000100': "유한양행",
    '019170': "신풍제약",
    '128940': "한미약품",
    '096530': "씨젠",
    '185750': "종근당",
    '006280': "녹십자"
}

data = []

for stock in stocks.keys():
    print(stocks[stock] + "의 데이터를 가져오고 있습니다...")
    a = fdr.DataReader(stock, start=startDate, end=endDate)["Close"].rename(stocks[stock])
    data.append(a)

data = pd.concat(data, axis=1)

print("기록중...", end='')
with open(title + '.csv', 'w', encoding="UTF8", newline="") as f:
    f.write(data.to_csv())

print("완료!")
