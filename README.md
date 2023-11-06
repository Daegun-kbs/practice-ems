# practice-ems
> ems 웹 프로그램

## 사용 기술

<div align=center>
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white">
    <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white">
    <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
    <img src="https://img.shields.io/badge/tailwindcss-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white">
    <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white">
    <img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
    <img src="https://img.shields.io/badge/influxdb-22ADF6?style=for-the-badge&logo=influxdb&logoColor=white">
    <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">
    <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
    <img src="https://img.shields.io/badge/eclipsemosquitto-3C5280?style=for-the-badge&logo=eclipsemosquitto&logoColor=white">
    
</div>

- python - 3.9.12 - 라이브러리는 requirement.txt에 기재
- django - 4.2.6
- mariaDB - 11.1.2
- redis - 5.0.7
- influxDB - v2
- MQTT Broker - mosquitto
- 날씨 api - 공공 데이터 포털: 기상청_단기예보 https://www.data.go.kr/data/15084084/openapi.do

## 필요한 환경변수

- SECRET_KEY - 장고 서비스키
- DEBUG - 장고 디버깅 모드 여부
- DB_NAME - 데이터베이스 이름
- DB_USER - 데이터베이스 유저 이름
- DB_PASSWORD - 데이터베이스 패스워드
- DB_HOST - 데이터베이스 호스트
- DB_PORT - 데이터베이스 포트
- WEATHER_URL - 날씨 api 요청url
- WEATHER_KEY - 날씨 api 요청 서비스키
- INFLUX_ORG - influxDB organizations 이름
- INFLUX_TOKEN - influxDB 토큰
- INFLUX_URL - influxDB url
- NPM_BIN_PATH - npm 설치 위치
- REDIS_HOST - 레디스 호스트
- ALARM_URL - 알람서버 api 요청 url
- ALARM_TOKEN - 알람서버 api 요청 인증키


## 시스템 구성도

### 서비스 구성도
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/7ba782e3-b1c7-4755-87d8-55b1c1a99880)



### 서버 구성도
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/e2c547e0-45bc-4ddd-b64c-41c71ea94d47)




## 화면 구성

### 메인 화면
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/14250918-15e5-433b-ba05-100fceb6f996)

### 실시간 데이터 화면
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/4f36d22f-a819-4213-8d85-bea0780d053f)

### 초단위 데이터 화면
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/61fd267e-2d01-45c6-843c-ff31028faf5f)

### 분단위 데이터 화면
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/12e1cd81-275a-4bf9-9312-35a1383b84c6)

### 통계 화면
![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/1b5864ad-9be6-4e4f-b1c4-c8cd83d053a4)


## 주요 기능


### 웹 앱

- 메인 메뉴 - 구성도 그림, 실시간 내용, 금일 차트 <img src="https://img.shields.io/badge/svg-FFB13B?style=for-the-badge&logo=svg&logoColor=white"><img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"><img src="https://img.shields.io/badge/chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white">
- 실시간 메뉴 - 1초마다 실시간 데이터 갱신(websocket) <img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
- 초단위 메뉴 - 1초단위 데이터 조회 <img src="https://img.shields.io/badge/influxdb-22ADF6?style=for-the-badge&logo=influxdb&logoColor=white">
- 분단위 메뉴 - 1분단위 데이터 조회 <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white">
- 통계 메뉴 - 15분단위 전력량 데이터 시각화 및 조회 <img src="https://img.shields.io/badge/chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white">

### publisher.py, subscriber.py

- publisher.py - ![image](https://github.com/LifeLikeMine/practice-ems/assets/114338420/d9e96e5a-e4a0-41c7-9daa-d5483510a915)Modbus simulator에 데이터 입력 및 데이터 조회, 조회 된 데이터 MQTT로 전송<img src="https://img.shields.io/badge/eclipsemosquitto-3C5280?style=for-the-badge&logo=eclipsemosquitto&logoColor=white">
- subscriber.py - MQTT로 전송된 데이터 수신 및 데이터 저장<img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white"><img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"><img src="https://img.shields.io/badge/influxdb-22ADF6?style=for-the-badge&logo=influxdb&logoColor=white">

