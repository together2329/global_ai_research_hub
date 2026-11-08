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
