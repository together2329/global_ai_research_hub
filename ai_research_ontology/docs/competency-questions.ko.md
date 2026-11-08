# 답해야 할 질문과 예시 조회

아래 결과는 모두 `examples/graph.yaml`의 가상 데이터에 대한 결과입니다. 실제 직원, 프로젝트 상태, 기술 성과를 나타내지 않습니다.

| 질문 | 근거를 따라가는 경로 | 실행 가능한 예시 |
| --- | --- | --- |
| CXL 전문성을 검증받은 사람은 누구인가? | Person ← ExpertiseAssertion → Expertise + Evidence | `cxl-experts` |
| CXL 연구에 어느 사람과 조직이 참여하는가? | ProjectMembership, RoleAssignment, OrganizationParticipation | `project-people` |
| RTL Agent를 실제 사용한 사람은 누구인가? | AssetUsage → Execution → Evidence | `asset-users` |
| HBF와 KV Cache를 모두 이해하는 사람은 누구인가? | 같은 Person의 검증된 ExpertiseAssertion 교집합 | `dual-expertise` |
| 이동한 연구원의 이전 소속과 연구를 찾을 수 있는가? | Person → 소속 기간 + 참여 기간 + 역할 + 사용 기록 | `person-history` |

저장소 루트에서 실행합니다.

```bash
python3 ai_research_ontology/scripts/query.py --query cxl-experts
python3 ai_research_ontology/scripts/query.py --query project-people --as-of 2026-10-31
python3 ai_research_ontology/scripts/query.py --query project-people --as-of 2026-11-01
python3 ai_research_ontology/scripts/query.py --query asset-users
python3 ai_research_ontology/scripts/query.py --query dual-expertise
python3 ai_research_ontology/scripts/query.py --query person-history
```

Engineer A의 10월 31일 소속은 Interface Team, 11월 1일 소속은 AX Team입니다. CXL 프로젝트 참여는 두 날짜에 모두 `membership_a_cxl`로 조회됩니다. Asset 사용 결과의 소속은 현재 소속이 아니라 `used_at` 시점의 소속입니다.

`dual-expertise`에는 Engineer B가 나옵니다. Engineer A의 HBF 전문성은 Git 활동에서 나온 `candidate`이므로 검증된 전문성 조회에 포함되지 않습니다. `asset-users`에는 실행 근거가 있는 Engineer A만 나오며, 같은 Agent 개발 프로젝트에 참여한 Engineer B는 자동 포함되지 않습니다.

실제 pilot에서는 다음 질문도 확인합니다.

- CMX 프로젝트에 공식 참여한 팀과 연구원은 누구인가? 참여 기간과 소속 기간을 어떻게 다르게 보여줄 것인가?
- 어떤 Workload 분석이 특정 Storage Requirement를 도출했는가?
- 어떤 Agent 버전이 어떤 설계 Commit과 Simulation 결과를 만들었는가?
- HBF와 CMX 연구에 비교 가능한 Benchmark가 있는가? 조건이 다르면 무엇이 비교를 제한하는가?
- GPU·EDA 사용량을 개인 활동이 아닌 프로젝트·실행 ID에 어떻게 귀속할 것인가?

CLI는 공개된 가상 데이터 전용 예제입니다. 사용자 인증·조직별 권한·민감 정보 필터링을 갖춘 실제 인사 검색 서비스로 사용하려면 별도 접근 제어가 필요합니다.
