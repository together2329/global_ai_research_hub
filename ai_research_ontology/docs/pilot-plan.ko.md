# 실제 연구 목록 적용 계획

먼저 실제 연구 20~30개를 골라 5개 Area의 경계와 Topic 중복을 검토합니다. 여러 분야·조직·개발 단계의 연구가 섞이도록 표본을 구성합니다. 조직·사람은 HR 및 승인된 Project Registry의 최소 참조로 연결합니다.

1. 연구별 ID·이름·목적·대표 Area·대표 기술 분야·Topic과 원본 문서 위치를 등록합니다.
2. Workload·Technique·개발 Asset·목표 Capability를 구분하고 모호한 항목을 남깁니다.
3. ProjectMembership과 RoleAssignment로 Owner·Developer를 연결합니다. 소속은 OrganizationMembership에서 해당 시점으로 조회합니다.
4. Workload 분석 → Requirement → Storage 연구와, RTL Agent → 실제 사용 → 설계 Commit → Simulation 결과를 각각 한 경로 이상 확인합니다.
5. Metric의 단위·분모·Benchmark·버전·조건을 확인하고 실제 수치가 있는 결과에만 Measurement를 등록합니다.
6. 검색과 재사용 질문을 실제로 수행해 누락·오분류·근거 부족·접근 범위 문제를 수정합니다.

| 검토 항목 | 통과 기준 |
| --- | --- |
| 대표 Area | 프로젝트당 하나이고 주된 질문과 인수 결과에 맞음 |
| 기술 분야 | 포트폴리오 Area·조직과 독립적으로 정하고 Topic의 분야 매핑과 일치함 |
| 공통 관점 | 품질·보안·신뢰성·효율·표준·재현성의 검토 여부와 인수 조건을 남김 |
| Topic | 중복·동의어가 정리되고 Technique·제품명과 혼동하지 않음 |
| 조직·사람 | 소속·참여·역할 기간과 근거가 분리됨 |
| 실제 자산 사용 | 실행 근거가 있으며 단순 참여 관계와 구분됨 |
| 결과 | Metric·단위·조건·실행·원본 근거가 연결됨 |
| 이력 | 조직 이동 뒤에도 과거 질문에 같은 ID로 답할 수 있음 |
| 접근 범위 | 사용자 권한에 따른 노드·관계·근거 조회 기준이 정의됨 |

검토가 필요한 경계는 AI Domain ↔ AI Workload, AI Workload ↔ AI Native Storage, AX Engineering ↔ AI Domain, 개별 연구용 Runtime ↔ Shared Infra입니다. 표본을 적용한 뒤 안정적인 용어와 관계를 승인하고 실제 시스템 연동 순서를 결정합니다.

서로 다른 검토자가 같은 프로젝트의 대표 Area와 기술 분야를 독립적으로 정하고, 일치율·미분류·억지 분류·동의어·근거 누락과 불일치 이유를 기록합니다. 현재 임의의 정확도 수치를 조직 성과로 제시하지 않습니다. 실제 Pilot 결과를 확인한 뒤 수용 기준을 정합니다. [보고용 제안서](executive-taxonomy-brief.ko.md)와 [검증 과제](executive-taxonomy-evidence.ko.md)를 함께 사용합니다.
