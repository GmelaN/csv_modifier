'''
네이버 증권 뉴스 json 파일을 불러오고, 이를 csv 파일로 변환하여 출력하는 프로그램

'''

import json
import csv
import requests

newsCountPerPage = 1000 #한 요청마다 불러올 뉴스 기사의 수
#보통 하루에 20여 개 정도의 뉴스가 올라옴 => 한 요청마다 {newsCountPerPage}개씩 불러오므로, 한 요청당 약 100일 분량의 뉴스를 불러옴

# DATETIME = "20191231" #{DATETIME}~오늘(프로그램을 실행하는 시점)까지의 뉴스 기사를 불러옴
#ex> 2020년 AA월 BB일까지의 뉴스 기사를 불러옴 => DATETIME = "2020AABB" | 2020년 X월 Y일 => DATETIME = "20200X0Y"

TOTAL_FETCH_COUNT = 35 #최대 요청 횟수
#어떤 경우라도 네이버 서버에 TOTAL_FETCH_COUNT번 이상 요청을 보내지 않음

#기록할 csv 파일
csvFileName = "./newsList_raw.csv"
#읽어올 json 파일
jsonFileName = "./out.json"

currentPage = 1 #현재 페이지
url = f"https://m.stock.naver.com/api/json/news/newsListJson.nhn?category=mainnews&pageSize={newsCountPerPage}&page="
# targetedExpectedDate = False
listJson = []

# def compareDateWithoutTime(date0, date1):
#     #3: 매개변수 오류, 0: 일치, 2:date0이 date1보다 이름, 1: date0이 date1보다 늦음
#     if type(date0) is not str or type(date1) is not str: raise TypeError #매개변수의 자료형이 string이 아닌 경우
#     if len(date0) != len(date1) != 8: return 3 #두 매개변수의 길이가 일치하지 않는 경우

#     #첫 번째 루프 => 월 비교 | 두 번째 루프 => 일 비교
#     for i in range(0, 3, 2):
#         diff = int(date1[4 + i : 6 + i]) - int(date0[4 + i : 6 + i])

#         if diff > 0: return 2 #date0 다음 date1
#         elif diff < 0: return 1 #date1 다음 date0
#         else: continue #같은 월인 경우
    
#     return 0 #날짜가 일치하는 경우

counter = 0
while counter < TOTAL_FETCH_COUNT:
    #기사 불러오기
    print(f"네이버로부터 {currentPage} 번째 JSON 파일을 불러옵니다...")
    try: out = requests.get(url + str(currentPage)).json()["result"]["newsList"] #json 구조를 가진 dictionary
    except: raise Exception
    counter += 1
    print(out[newsCountPerPage - 1]["dt"][:8], "일 뉴스까지 불러왔습니다.")

    for k in range(len(out)): listJson.append(json.dumps(out[k], ensure_ascii=False)) #불러온 뉴스는 리스트에 추가
        
    currentPage += 1 #다음 페이지로 이동

json_str = '{"newsList":[{' + ",".join(listJson).replace('[', '{').replace(']', '}')[1:-1] + "}]}"

print("파일에 저장하고 있습니다...")
with open("./out.json", 'w', encoding="UTF8") as jsonFile: jsonFile.write(json_str)

#csv 파일 불러오기
try:
    print("csv 파일 만드는 중...", csvFileName)
    csvFile = open(csvFileName, 'w', encoding="UTF8", newline="")
    csvObj = csv.writer(csvFile)
except:
    print("csv 파일 열기 오류: ", csvFileName, "을 쓸 수 없음")
    exit(1)

#json 파일 불러오기
try:
    print("json 파일 불러오는 중...", jsonFileName)
    with open(jsonFileName, 'r', encoding="UTF8") as jsonFile:
        jsonObj = json.load(jsonFile)["newsList"]
except:
    print("파일 읽기 오류: ", jsonFileName, "이/가 존재하지 않음")
    csvFile.close()
    exit(1)

#json 파일에 있는 뉴스 기사의 수 저장
jsonFileLength = len(jsonObj)

#뉴스 기사의 각 인덱스 리스트
jsonDicKeys = ["tit", "subcontent", "dt"]

#제목 열 기록
csvObj.writerow(["제목", "부제", "날짜", "시각"])

for i in range(jsonFileLength):
    #csv 파일의 각 열이 될 리스트
    listToWrite = []

    for key in jsonDicKeys:
        if key == "dt": #dt => 날짜, 시각으로 분리하여 기록
            listToWrite.append(str(jsonObj[i][key][:8]))
            listToWrite.append(str(jsonObj[i][key][8:]))
        else:
            listToWrite.append(str(jsonObj[i][key]))

    csvObj.writerow(listToWrite) #csv파일에 리스트 기록

print("작업 완료: ", csvFileName, "에 저장됨")
csvFile.close()
