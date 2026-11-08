# 설계 결정 기록

2026-11-08, v0.3 제안 초안.

| 결정 | 이유 |
| --- | --- |
| 기존 Hub의 `ai_research_ontology/` 모듈로 구성 | 연구 Hub와 같은 저장소에서 관리하되 모델 진입점을 명확히 함 |
| 5개 Research Area 유지 | 기존 v0.2의 기술 중심 분류를 보존 |
| Topic 그룹 ID에 `topic_group_` 접두어 사용 | CXL Memory Expansion 등 그룹과 세부 Topic의 ID 충돌 해소 |
| 조직·사람을 독립 객체로 추가 | 조직 개편과 인사 이동을 연구 분류와 분리 |
| 소속·참여·역할·전문성 주장을 별도 객체로 관리 | 서로 다른 원본 권위, 유효 기간, 근거를 보존 |
| Project Owner를 RoleAssignment로 계산 | Commit 작성자·현재 팀·단일 Owner 문자열과 혼동 방지 |
| 실제 AssetUsage를 실행 기록에 연결 | 프로젝트 참여와 실제 사용 사실을 구분 |
| PPA를 Metric family로 정의 | 서로 다른 단위의 결과를 하나의 수치로 기록하지 않음 |
| 대부분의 지표는 계약 후보로 유지 | 실제 Benchmark와 조직 기준으로 산식·분모·조건을 검토해야 함 |
| 8개 공통 지표에 예시 측정 계약 제공 | TTFT, TPOT, Tokens/s, RTL Compile Pass Rate, Simulation Pass Rate, GPU Utilization, Bandwidth, Tail Latency |

남은 결정은 실제 연구 목록에서 Area 경계를 조정하는 일, Role·Expertise 승인 기준, 원본 ID 매핑과 접근 권한, 지표 계약 승인, 실제 데이터 규모에서의 조회 성능입니다. 초기 Git 구성과 예시 validator의 통과는 조직 승인이나 실제 연구 성과를 뜻하지 않습니다.

## 2026-11-08, v0.4 공개 연구 확장

| 결정 | 이유 |
| --- | --- |
| 5개 Area와 기존 ID 유지, 세부 Topic 57개 추가 | 기존 포트폴리오를 보존하면서 Vector·GPU I/O·Checkpoint·Agent Memory 등의 연구 질문 수용 |
| ResearchDirection으로 여러 Area 연결 | 시점별 연구 흐름을 배타적 상위 분류와 구분 |
| DataObjectKind·SystemLayer·Bottleneck·ValidationStage 추가 | 데이터 종류·위치·제약·검증 범위를 독립 축으로 조회 |
| 공개 자료 14건과 내부 가상 예시 분리 | 실제 공개 출처를 가상 실험·인사 기록과 혼동하지 않도록 함 |
| Storage-Next를 TechnologyInitiative로 등록 | 업체 프로그램을 일반 Topic·실제 자산·확정 표준과 구분 |
| 공개일 정밀도·검토 범위·발표 당시 제공 상태 보존 | 초록 확인을 전체 논문 검증으로, 계획을 출하로 해석하지 않도록 함 |
| 내부 재현 여부 별도 보존 | 외부 저자·업체 결과를 내부 성과로 승격하지 않도록 함 |
| QPS에 Recall·p99, 작은 I/O IOPS에 p99 요구 | 같은 조건에서 품질·처리량·지연을 함께 평가 |
| work_kind를 Area와 독립적으로 추가 | 연구·솔루션 엔지니어링·플랫폼·운영의 성격 구분 |

현재 39개 타입·578개 객체·218개 세부 Topic이다. 근거 범위와 미조사 영역은 [연구 동향 반영 근거](research-landscape-20261108.ko.md)에 남겼다. 출처 기반 분류 초안이며 세계 연구의 전수 목록 또는 조직 승인 기준은 아니다.
