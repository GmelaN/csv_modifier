# csv_modifier

getDataFromNaver.py
---

**네이버 증권 뉴스 모바일 페이지에서 기사 목록을 담은 json 파일을 불러와 csv 파일로 변환하여 저장합니다.**


실행 전 TOTAL_FETCH_COUNT(요청 횟수), newsCountPerPage(각 요청마다 불러올 기사 수) 값을 상황에 맞게 수정 후 실행해주세요.


csv 파일에는 다음과 같은 항목이 있습니다.


* 기사 제목
* 기사 부제목
* 개재 날짜("yyyymmdd" 형식)
* 개재 시각("hhmmss" 형식, 가장 왼쪽 자리가 0인 경우 생략(ex. 00시 05분 01초: 501))

변수 csvFileName에 저장할 csv 파일의 이름을 지정할 수 있습니다. 경로와 확장자(.csv)까지 모두 적어야 합니다.



countAndClassifyByTime.py
---

**getDataFromNaver.py에서 생성한 csv 파일로부터 뉴스 기사를 읽고, 각 기사의 제목, 부제목을 대상으로 키워드 출현 빈도를 세어 csv 파일로 저장합니다.**


csv 파일에는 다음과 같은 항목이 있어야 하고, 실행 전 TITLE, SUBTITLE, DATE, TIME 값을 csv 파일에 맞게 수정 후 실행하여야 합니다.
* TITLE(기사 제목)
* SUBTITLE(부제목)
* DATE(날짜 - "yyyymmdd" 형식)
* TIME(시각 - "hhmmss" 형식, 가장 왼쪽 자리가 0인 경우 생략(ex. 00시 05분 01초: 501))


세어 나갈 키워드는 wordList 값을 수정하여 지정할 수 있습니다.

* 두 음절 이상으로 이루어진 단어의 경우, 띄어쓰기 여부에 따라 다른 단어로 인식합니다. ("우한 폐렴"과 "우한폐렴"을 서로 다른 단어로 인식합니다.)
    - 이렇게 띄어쓰기 여부에 따라 다르게 세어진 단어들은 mergeColumn.py에서 다시 하나의 열로 합쳐집니다.
* 한 키워드를 추가할 때, "{키워드}"와 함께 "{키워드} 장전", "{키워드} 장중", "{키워드} 장외" 항목도 같이 추가해야 합니다.


csv 파일에는 다음과 같은 항목이 있습니다. n번째 행의 정보는 n번째 기사에 대한 정보입니다.
* 개재 날짜("yyyymmdd" 형식)
* 키워드 1의 출현 빈도
* 장전 키워드 1의 출현 빈도
* 장중 키워드 1의 출현 빈도
* 장외 키워드 1의 출현 빈도


...
* 키워드 n의 출현 빈도
* 장전 키워드 n의 출현 빈도
* 장중 키워드 n의 출현 빈도
* 장외 키워드 n의 출현 빈도
        
장전, 장중, 장외 키워드 n의 출현 빈도는 기사의 개재 시각에 따라 결정됩니다.


예를 들어 기사 i가 장전 시간에 개재되었다면, 키워드 n의 장전 출현 빈도는 결국 기사 i에서 키워드 n의 출현 빈도와 같게 됩니다.

mergeTimeDataToDate.py
---   
**countAndClassifyByTime.py에서 생성한 빈도 csv 파일로부터, 각 날짜별 키워드 전체 출현 빈도를 계산하여 csv 파일로 저장합니다.**


countAndClassifyByTime.py에서 생성한 csv 파일은 각 행에 각 기사에 대한 정보를 담고 있습니다. 이를 취합하여 날짜별 키워드 출현 빈도로 변환합니다.


csv 파일에는 다음과 같은 항목이 있습니다. n번째 행의 정보는 yyyy년 mm월 dd일 개재된 기사들 전체에 대한 정보입니다.
* 개재 날짜("yyyymmdd" 형식)
* 키워드 1의 출현 빈도
* 장전 키워드 1의 출현 빈도
* 장중 키워드 1의 출현 빈도
* 장외 키워드 1의 출현 빈도


...
* 키워드 n의 출현 빈도
* 장전 키워드 n의 출현 빈도
* 장중 키워드 n의 출현 빈도
* 장외 키워드 n의 출현 빈도
    
실행 전 변수 filename에 불러올 csv 파일의 이름(확장자(.csv) 제외)을 지정하여야 합니다.


작업이 완료된 csv 파일의 이름은 "{filename}\_merged.csv"입니다.

expandMissingDataByPrevData.py
---

**mergeTimeDataToDate.py에서 생성한 csv 파일로부터, 날짜가 누락된 항목을 찾아 직전 데이터로 덮어씌웁니다.**


mergeTimeDataToDate.py에서 생성한 csv 파일의 개재 날짜 항목은 기간 내의 모든 날짜 정보를 담고 있지 않을 수 있습니다. yyyy년 mm월 dd일에 개재된 뉴스가 하나도 없을 수 있기 때문입니다.


이렇게 누락된 날짜를 찾아 직전 데이터 값으로 덮어씌웁니다.


csv 파일에는 다음과 같은 항목이 있습니다. n번째 행의 정보는 yyyy년 mm월 dd일 개재된 기사들 전체에 대한 정보입니다.
* 개재 날짜("yyyymmdd" 형식)
* 키워드 1의 출현 빈도
* 장전 키워드 1의 출현 빈도
* 장중 키워드 1의 출현 빈도
* 장외 키워드 1의 출현 빈도


...
* 키워드 n의 출현 빈도
* 장전 키워드 n의 출현 빈도
* 장중 키워드 n의 출현 빈도
* 장외 키워드 n의 출현 빈도

실행 후 불러올 csv 파일의 이름(확장자(.csv) 제외)를 프롬프트에 입력하여야 합니다.


작업이 완료된 csv 파일의 이름은 "{filename}\_edited.csv" 입니다.


mergeColumn.py
---
**countAndClassifyByTime.py에서 띄어쓰기 여부에 따라 다르게 세어진 단어들을 하나의 열로 취합합니다.**
작성중

dateChecker.py
---
**csv 파일이 기간 내 모든 날짜 데이터를 갖고 있는지 확인합니다.**


csv 파일의 날짜 항목의 구분자(yyyy-mm-dd이면 '-', yyyy.mm.dd이면 '.')는 한 글자여야 합니다. (yyyy--mm--dd에서의 구분자 "--"는 인식 불가)


csv 파일은 날짜 기준 오름차순으로 정렬되어 있어야 합니다.


실행 전 변수 DATE에 csv 파일 내 날짜 열의 위치(0부터 시작)를 지정하여야 합니다.


실행 후 불러올 csv 파일의 이름(확장자(.csv) 제외)를 프롬프트에 입력하여야 합니다.
