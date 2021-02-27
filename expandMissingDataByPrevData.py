"""
    중간 중간 누락된 날짜의 데이터를 이전 날짜의 데이터로 덮어씌우는 프로그램
    파일의 첫 행은 항상 헤더가 있어야 함
    날짜는 항상 첫 번째 열에 있어야 함
"""
import csv
import datetime
import sys

def makeDateObject(string):
    '''
        날짜 문자열로부터 datetime.date 객체를 생성하는 함수
        string: 날짜 문자열
        반환값: 날짜 문자열의 정보를 담고 있는 datetime.date 객체
    '''
    global dateSeperator

    if not dateSeperator: # 구분자 없음 => "19700101" 형식
        try:
            return datetime.date(
                int(string[:4]),
                int(string[4:6]),
                int(string[6:])
            )

        except Exception as e: # 변환 도중 오류 발생시 호출(올바르지 않은 날짜 형식)
            print("올바르지 않은 날짜 형식입니다.")
            sys.exit(1)
    else:
        sep = string.split(dateSeperator) # 구분자가 존재하는 경우 - 구분자를 기준으로 split

        if len(sep) != 3: #년, 월, 일의 3개 원소가 아닌 경우
            print("올바르지 않은 날짜 형식이 발견되었습니다.")
            raise Exception

        return datetime.date(
            int(sep[0]),
            int(sep[1]),
            int(sep[2])
        )

filename = input("불러올 파일의 이름을 입력하십시오: ")
try:
    with open(filename + '.csv', 'r', encoding="UTF8") as f:
        csvContent = list(csv.reader(f)) #csv 파일 내용을 담은 리스트

except Exception as e: # 파일이 존재하지 않거나 사용중인 경우
    print("파일을 여는 중 오류가 발생하였습니다: " + str(e))
    sys.exit(1)

#날짜의 구분자 확인
dateSeperator = ""

if not csvContent[1][0][4].isdigit(): #csvContent[1][0] = "yyyy-mm-dd" 에서, 4번째 원소는 구분자 '-'임 
    dateSeperator = csvContent[1][0][4]

#만약 구분자가 없는 경우 4번째 원소는 월 정보일 것(=> 숫자) - 구분자는 없음(빈 문자열)

csvIdx = 0 # csv 파일 내용 리스트 인덱스

startDate = makeDateObject(csvContent[1][0]) #csv 상 첫 날짜
endDate = makeDateObject(csvContent[-1][0]) #csv 상 마지막 날짜

f = open(filename + "_edited.csv", 'w', encoding="UTF8", newline="") # 출력 파일 스트림
output = csv.writer(f)

# header 정보 출력
output.writerow(csvContent[csvIdx])
csvIdx += 1 # 인덱스 1 증가

currentDate = startDate # currentDate = 처리중인 날짜

print("처리 중...", end='')

while currentDate <= endDate and csvIdx < len(csvContent): # currentDate가 마지막 날짜보다 작거나 같고, csv 파일 인덱스가 리스트 길이를 벗어나지 않아야 함
    currentContent = csvContent[csvIdx] # csv 파일의 현재 내용 => 처리중인 행
    currentCsvDate = makeDateObject(currentContent[0]) # 처리중인 행의 날짜 정보

    if currentDate != currentCsvDate: # 순차적으로 세고 있는 날짜와의 차이 발견 (= 누락된 자리 발견)
        prevContent = csvContent[csvIdx - 1] # 이전 날짜의 csv 파일 내용

        while currentDate != currentCsvDate: # currentDate는 1씩 증가 / currentCsvDate와 같을 때 까지 반복

            # csv 파일 현재 내용의 날짜를 하루씩 증가시키면서 이전 날짜의 csv 파일 내용을 출력
            listToWrite = [ str(currentDate).replace('-', dateSeperator) ] # 기록할 행 리스트: 첫 번째 열은 날짜 / 파일에서 사용하는 날짜 구분자로 치환해줌
            for i in prevContent[1:]: # 이전 날짜의 csv 파일 내용을 기록할 행 리스트에 append - 날짜 정보는 제외
                listToWrite.append(i)
            
            #debug: 이전 날짜 데이터의 날짜 부분을 같이 쓰기 (데이터의 원래 날짜 정보도 출력)
            # listToWrite.append(prevContent[0])

            #만든 리스트 내용을 csv 파일에 기록
            output.writerow(listToWrite)
            # 현재 날짜를 1 증가시킴
            currentDate += datetime.timedelta(+1)

    output.writerow(currentContent)
    currentDate += datetime.timedelta(+1)
    csvIdx += 1

print("완료!\n수정된 파일: " + filename + "_edited.csv")
f.close()
input("계속하려면 엔터 키를 입력하십시오...")
