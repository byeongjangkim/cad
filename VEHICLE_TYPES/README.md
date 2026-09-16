# 현재 작업: C형 독립 구동 4WD

- A형: ZD9021-V3 기준 유지
- B형: 기존 RC 부품 조합 보존, C형 완료 후 재검토
- [C형 개념 도면](03_INDEPENDENT_4WD/TypeC_Independent4WD_R0.FCStd): 4모터·스윙암·차동속도 조향
- [C형 설명 및 미확정 사항](03_INDEPENDENT_4WD/README.md)

아래는 기존 검토 이력입니다.

# 현재 B형: R2 허브·지지 구조 검토

[현재 검토 보고서](02_DIY_10KG_PAYLOAD/REVIEW_R2.md) · [FreeCAD](02_DIY_10KG_PAYLOAD/TypeB_DIY_10kg_R2.FCStd)

아래는 이전 검토 이력입니다.

# 현재 B형 R1

[BUYRC 후보 및 샤시 변경 검토](02_DIY_10KG_PAYLOAD/REVIEW_R1.md) · [B형 FreeCAD](02_DIY_10KG_PAYLOAD/TypeB_DIY_10kg_R1.FCStd)

# 차량 A/B 현재 파일

- **A형 유지**: [ZD9021-V3 참조 모델](01_ZD9021V3/TypeA_ZD9021V3.FCStd). 기존 파일을 수정하지 않는다. 제조사 정밀 CAD가 아닌 참조 재구성본이다.
- **현재 B형**: [별도 가공 샤시·적재10kg·전륜조향 4모터 설계](02_DIY_10KG_PAYLOAD/README.md). [FreeCAD 배치검토 R0](02_DIY_10KG_PAYLOAD/TypeB_DIY_10kg_R0.FCStd). 구매 후보/미확인 치수 포함, 가공 출도 전이다.

이전 `02_KRATON_EXB`는 조달 불가에 따른 중단된 키트 검토 이력, `02_25KG_TARGET`은 이전 구조 검토 이력이다. 현재 B형으로 사용하지 않는다. 총중량25kg 고정 조건은 없으며, 현재 요구는 적재하중10kg·0.1–2m/s·4륜 독립현가·바퀴별 모터·전륜 조향이다. 배터리는 미정이다.

`open_two_types.FCMacro`는 저장된 A/B 문서를 여는 용도이며 원본에 덮어쓰지 않는다.

현재 B형 구매 후보는 [BUYRC 선정표](02_DIY_10KG_PAYLOAD/BUYRC/README.md)를 우선한다. R0 CAD는 이전 배치 이력이며 신규 선정품의 실제 형상으로 전환 전이다.
