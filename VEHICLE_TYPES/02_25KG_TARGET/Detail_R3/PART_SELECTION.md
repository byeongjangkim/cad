# 25kg B형 부품 선정표

기준: 총25kg, 평지,0.1–2m/s,145mm 바퀴. 아래는 설계 기준 부품과 미선정품을 구분한 표다. 구매 확정 BOM이 아니다.

| 부위 | 모델 / 수량 | 선정 상태 | 남은 확인 |
|---|---|---|---|
| 구동 모터 | HOBBYWING AXE4274 R3 1700KV / 1 | 시제품 설계 기준 후보로 유지 | 연속 토크·온도, 실제 감속기 및 축 결합 |
| ESC | HOBBYWING AXE PLUS R3,30113201 / 1 | 위 모터와 호환되는 설계 기준품 | 배터리·제동·자율주행 제어 신호 통합 |
| 허브 베어링 | NSK6001 규격 / 8 | 12×28×8 치수 기준품 | 밀봉형 정확한 품번, 끼워맞춤, 축방향 지지 |
| 현가 스프링 | MISUMI SWL16-100 / 4 | 강성8.6N/mm 기준 후보 | 하강 이탈 여유와 하중 편차, 받침 조정 |
| 조향 액추에이터 | ROBOTIS XW540-T260-R / 1 | 직접 구동 채택 보류 | 외부 감속·지지축·12V 계통·RS485 제어 |
| 감속기 | 미선정 | 추가4:1은 목표 가정일 뿐 | 연속 입력 회전수/토크, 축경, 정격, 설치 치수 |
| 프론트·센터·리어 차동기어 | Traxxas8991 /8980 /8992 각1 | 완성품 후보 확인 | 25kg 정격·외부 연결 치수 미확인 |
| CV/신축 구동축 | 미선정 | D10은 설계 치수 | 작동각, 신축량, 정격과 축 연결 |
| 오일 댐퍼 | 미선정 / 4 | D28 외형은 예약공간 | 유효 스트로크·감쇠력·장착 치수 확인 |
| 타이어 | 미선정 / 4 | D145×69 공간 | 바퀴당6.25kg 정적 하중 및 동하중, 림 체결 |

## 제조사 확인 근거
[HOBBYWING 모터](https://www.hobbywing.com/products/xerunaxer3motor): AXE4274 R3 1700KV,3–6S,외경42×길이74mm. [2026 설명서](https://www.hobbywing.com/uploads/file/20260312/d1df5447c1d6adde1d65e217572ae561.pdf)는 축경5mm·돌출20.5mm를 제시한다. 연속 토크를 차량25kg 적합성으로 환산할 자료는 확인하지 못했다.

[HOBBYWING ESC](https://www.hobbywing.com/en/index.php/products/xerunaxeplusr3): AXE4274 R3 지원,2–6S,135A 표기. BEC는6/7.4/8.4V,6A다. ESC 전류 정격이 모터의 연속 출력 정격을 뜻하지 않는다.

[NSK6001](https://www.nsk.com/engineering/6001-apn.html): 기본동정격5600N,기본정정격2370N. 이 수치를 밀봉형 품번의 확정치나 전체 허브 수명으로 대체하지 않는다.

[MISUMI SWL 규격표](https://tw.misumi-ec.com/pdf/fa/2015/p2_395.pdf): SWL16-100 자유장100mm,외경16/내경8mm,강성8.6N/mm. D28댐퍼 외부에 씌울 수 없어 별치 방식이다.

[ROBOTIS 제품](https://robotis.us/products/dynamixel-xw540-t260-r),[매뉴얼](https://emanual.robotis.com/docs/en/dxl/x/xw540-t260/):12V 스톨9.5Nm와 제조사 추정 정격1.9Nm를 구분한다. 현재 조향 선별값7.95Nm를 스톨값과 비교해 채택하지 않는다. 별도 축 지지와 감속이 필요하다. ESC BEC의 최대8.4V는 이 액추에이터의12V 설계 전원으로 사용할 수 없다. 전원 변환기와RS485 제어를 포함해야 한다.

## 선정 순서
현재 가장 큰 미결정은 감속기·차동기어·CV다. 이 부품들의 실제 인터페이스를 정한 뒤 프레임 장착점을 수정해야 한다. 기존 ZD13T/46T와 입력11T 가정만으로 총감속비를 확정하지 않는다. 전체 동력 전달이 연결되지 않은 상태에서 위 표 전체를 구매 대상으로 표시하지 않는다.


실제품 연결 검토 결과: [DRIVELINE_REVIEW.md](DRIVELINE_REVIEW.md), [연결표 CSV](DRIVELINE_INTERFACES.csv). 감속기 PLE040 i4 및 Traxxas Maxx 계열을 상세 비교 대상으로 추가했다. 완결 호환 조합으로 확정한 것은 아니다.


후속 확인: [완성 조립품 후보와 CAD 변경 조건](ASSEMBLY_SELECTION_UPDATE.md), [후보 조립 BOM](CANDIDATE_ASSEMBLY_BOM.csv).

추가 검증: [핀·베어링 규격과 자료 모순 검토](VERIFICATION_LOG.md).
