# B형 BUYRC 조달 검토 — 2026-09-15

현재 우선 조달처는 사용자가 지정한 **buyrc.co.kr / 용산알씨**다. 기존 Traxxas 우선 선정은 철회하고, ARRMA KRATON/OUTCAST 6S 계열 부품을 우선 후보로 정리했다. 샤시는 별도 가공한다. 적재10kg, 4개 모터, 독립현가, 전륜 기계식 조향, 0.1–2m/s 요구는 유지한다. A형은 수정하지 않았다.

## 결과

`BOM_BUYRC.csv`와 상위 `BOM.csv`를 갱신했다. 28개 판매 항목의 주요/대안/보류 후보와 6개 미완료 항목을 구분했다. `listing_checks.json`은 제외 후보까지 포함한 33개 상세 페이지의 가격 및 주문 버튼 확인 기록이다. **주문 버튼이 있다는 사실은 실재고 수량이나 즉시 출고 확약이 아니다.** 로그인·장바구니·주문·판매점 연락은 하지 않았다.

주요 기계 부품 후보:

| 기능 | 제품 | BUYRC 링크 |
|---|---|---|
| 전륜 상/하부암 | AR330218 / AR330219 | [상부](https://buyrc.co.kr/product/product_detail.asp?product_number=99085), [하부](https://buyrc.co.kr/product/product_detail.asp?product_number=99084) |
| 후륜 하부암 | AR330249 | [상품](https://buyrc.co.kr/product/product_detail.asp?product_number=99086) |
| 전륜 조향 블록 / 후륜 허브 | AR330505 / AR330404 | [전륜](https://buyrc.co.kr/product/product_detail.asp?product_number=99103), [후륜](https://buyrc.co.kr/product/product_detail.asp?product_number=99047) |
| 전륜 CVD | AR310458 + AR310590 + AR310452 | [샤프트](https://buyrc.co.kr/product/product_detail.asp?product_number=99029), [액슬](https://buyrc.co.kr/product/product_detail.asp?product_number=99028), [연결 부속](https://buyrc.co.kr/product/product_detail.asp?product_number=99031) |
| 후륜 기본 축 / CVD 대안 | AR310459 + AR310591 / GPM MAK140RS-BK | [도그본](https://buyrc.co.kr/product/product_detail.asp?product_number=99041), [액슬](https://buyrc.co.kr/product/product_detail.asp?product_number=99110), [CVD 대안](https://buyrc.co.kr/product/product_detail.asp?product_number=116862) |
| 전륜/후륜 조립 쇼크 | GPM MAK115FAA-R-S / MAK135RAA-R-S | [전륜](https://buyrc.co.kr/product/product_detail.asp?product_number=107520), [후륜](https://buyrc.co.kr/product/product_detail.asp?product_number=107221) |
| 벨크랭크 | AR340073, AR340072, AR340066, AR340062 | [벨크랭크](https://buyrc.co.kr/product/product_detail.asp?product_number=99098) |
| 조향 서보 | RC935DMG | [상품](https://buyrc.co.kr/product/product_detail.asp?product_number=124575) |

후륜 상부는 전륜과 같은 삼각암이 아니라 캠버 링크를 사용하는 부품군이다. R0의 전후 동일 상부암 공간 모델을 그대로 재사용하면 안 된다. 전륜 역시 Maxx C허브와 ARRMA 피벗볼 구조를 같은 형상으로 취급하면 안 된다.

## 규격을 잘못 혼합하지 않기 위한 판정

- AR330550/551은 이번 6S 현가의 확정 쇼크로 채택하지 않았다. AR330551은 주문 버튼이 없었고 판매점에 ARA-2094 대체 표기가 있다.
- AR330552/553은 이름에 Big Bore와 Kraton이 있지만, 제조사 제품 적용표는 **Kraton/Outcast 4S**다. 6S 제품으로 혼용하지 않는다. [제조사 전륜 적용표](https://www.arrma-rc.com/en/product/arrma-big-bore-shock-set-front-2/ARA330552.html), [후륜 적용표](https://www.arrma-rc.com/en/product/arrma-big-bore-shock-set-rear-2/ARA330553.html).
- GPM 조립 쇼크를 후보로 전환했다. 판매점 표기 전115mm/후135mm를 확인했지만, 최소길이·스프링 강성·허용 하중은 아직 확인되지 않았다. 표기 길이를 서스펜션 스트로크로 사용하지 않는다.
- GPM MAK142FS-BK 전륜 조립 CVD는 상세 페이지에 주문 버튼이 없어 주요 후보에서 제외했다. 전륜은 기본 ARRMA 샤프트/액슬/연결 부속으로 검토한다.
- 구형 6S 암과 최신 V5/V6/EXB 암을 자동 호환으로 취급하지 않는다. RPM 제조사가 AR330218/219를 대체하는 제품군을 안내하고 있어 구형 기준 부품군 확인에 참고했다. [RPM 제조사](https://rpmrcproducts.com/rpm-products-pages/a-arms/front-a-arms/kraton-6s-front-arms/).
- 공식 ARRMA 분해도에서 필요한 핀·볼·베어링·링크·출력컵을 모두 대조한 뒤 구매 수량을 확정해야 한다. [ARRMA 공식 구형 설명서/분해도](https://www.arrma-rc.com/on/demandware.static/-/Sites-horizon-master/default/dw759b6c42/Manuals/ARA10604-Manual-MULTI.pdf). 현재는 완결된 발주 BOM이 아니다.

## 모터: 판매 확인과 설계 적합성을 분리

BUYRC에 [AXE4274 R3 1700KV](https://buyrc.co.kr/product/product_detail.asp?product_number=125482), [AXE PLUS R3 ESC](https://buyrc.co.kr/product/product_detail.asp?product_number=125481)가 등록되어 있고 주문 버튼을 확인했다. 하지만 AXE 모터는 일체형 감속모터가 아니다. 4개 바퀴를 각각 구동하려면 각 모터의 감속/지지/컵 연결을 별도로 구성해야 한다. ServoCity 감속모터 STEP를 AXE 이름으로 변경하는 방식은 사용하지 않는다.

예를 들어 24V·1700KV의 무부하 계산 회전수는40,800rpm, Ø160 바퀴2m/s는239rpm이다. 단순 무부하 기준으로 약171:1이므로 무감속 직결은 맞지 않는다. 이 계산은 요구 감속비 확정값이 아니며, 실제 전압·부하 회전수·모터 운전 영역을 먼저 정해야 한다. BUYRC에서 적합한 일체형 감속모터 또는 독립4개 감속기 조합은 아직 확인하지 못했다. 외부 조달로 확정한 것도 아니다.

RC935DMG의 35kg급·방수·메탈기어는 판매점 표기다. 서보 정격 전압, 토크 단위/조건, 혼 스플라인, 외형 및 정지 조향 토크를 확인하기 전 제작용으로 확정하지 않는다. 주행 제어와 조향 서보 전원은 별도로 검토한다.

## CAD 반영 상태

**이번에는 조달 기준과 후보 BOM을 변경했다. R0 FCStd/STEP 형상은 아직 ARRMA 제품으로 교체하지 않았다.** R0는 이전 Maxx 후보/ServoCity 모터의 배치 이력이다. 주황색 공간 모델을 그대로 두고 ARRMA 품번만 바꾼 실제 제품 도면으로 제시하지 않는다.

다음 형상 수정은 다음 순서다.

1. 선정 후보의 장착 치수/원본 CAD 또는 실측 확보.
2. 전륜 피벗볼과 후륜 캠버 링크 구조로 변경.
3. 전115/후135 쇼크의 실제 장착 길이와 모션비 적용.
4. 구동축의 관절 중심·컵 삽입 여유·모터 감속기 패키지를 기준으로 윤거 재계산. 142mm 샤프트의 명칭 길이를 전체 모듈 길이로 사용하지 않는다.
5. 전륜 조향·범프/리바운드 간섭과 적재10kg 스프링/지지 강도 검토 후 샤시 구멍과 가공도 확정.

520×440mm, 질량 예산21.66kg은 R0의 잠정치로서 새 조달 구성의 확정치가 아니다. 그 크기에 맞추기 위해 구매 부품 형상을 축소하지 않는다.
