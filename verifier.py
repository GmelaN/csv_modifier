import csv

csvFile = input("CSV 파일 이름 입력: ")

with open(csvFile + ".csv", 'r', encoding="UTF8") as f:
    csvContent = list(csv.reader(f))

headers = csvContent[0]

print('|', end='')
for head in headers:
    print(head, '|', sep='', end='')

cell1, cell2 = [int(i) for i in input("\n비교할 두 셀의 인덱스를 입력(0부터 시작):").split()]

print(headers[cell1], headers[cell2])
for i in range(1, len(csvContent)):
    if int(csvContent[i][cell1]) != int(csvContent[i][cell2]):
        print(i, "번 내용이 일치하지 않음")

print("확인 끝")
