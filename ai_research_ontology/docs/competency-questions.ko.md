# 답해야 할 질문과 예시 조회

아래 조직·사람 조회는 `examples/graph.yaml`의 가상 데이터에 대한 결과입니다. `research-landscape`는 별도 Registry의 실제 공개 출처를 조회합니다. 출처 내용 확인은 내부 재현을 뜻하지 않습니다.

| 질문 | 근거를 따라가는 경로 | 실행 가능한 예시 |
| --- | --- | --- |
| CXL 전문성을 검증받은 사람은 누구인가? | Person ← ExpertiseAssertion → Expertise + Evidence | `cxl-experts` |
| CXL 연구에 어느 사람과 조직이 참여하는가? | ProjectMembership, RoleAssignment, OrganizationParticipation | `project-people` |
| RTL Agent를 실제 사용한 사람은 누구인가? | AssetUsage → Execution → Evidence | `asset-users` |
| HBF와 KV Cache를 모두 이해하는 사람은 누구인가? | 같은 Person의 검증된 ExpertiseAssertion 교집합 | `dual-expertise` |
| 이동한 연구원의 이전 소속과 연구를 찾을 수 있는가? | Person → 소속 기간 + 참여 기간 + 역할 + 사용 기록 | `person-history` |
| Vector Search와 관련된 공개 자료·병목·지표는 무엇인가? | ResearchDirection → Topic / Facet / ExternalResearch → SourceRecord | `research-landscape --direction vector_search` |
| Storage-Next는 어떤 프로그램이며 제품 상태는 어디까지 확인됐는가? | TechnologyInitiative ← ResearchDirection → ExternalResearch의 제공·검증 상태 | `research-landscape --direction storage_next` |
| 부문 전체의 기술 연구 지도를 어떻게 보는가? | TechnologyDomain ← Topic ← ExternalResearch + ResearchConcern | `executive-map` |

저장소 루트에서 실행합니다.

```bash
python3 ai_research_ontology/scripts/query.py --query cxl-experts
python3 ai_research_ontology/scripts/query.py --query project-people --as-of 2026-10-31
python3 ai_research_ontology/scripts/query.py --query project-people --as-of 2026-11-01
python3 ai_research_ontology/scripts/query.py --query asset-users
python3 ai_research_ontology/scripts/query.py --query dual-expertise
python3 ai_research_ontology/scripts/query.py --query person-history
python3 ai_research_ontology/scripts/query.py --query executive-map
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction vector_search
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction storage_next
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction vector_search --as-of 2026-03-31
```

Engineer A의 10월 31일 소속은 Interface Team, 11월 1일 소속은 AX Team입니다. CXL 프로젝트 참여는 두 날짜에 모두 `membership_a_cxl`로 조회됩니다. Asset 사용 결과의 소속은 현재 소속이 아니라 `used_at` 시점의 소속입니다.

`dual-expertise`에는 Engineer B가 나옵니다. Engineer A의 HBF 전문성은 Git 활동에서 나온 `candidate`이므로 검증된 전문성 조회에 포함되지 않습니다. `asset-users`에는 실행 근거가 있는 Engineer A만 나오며, 같은 Agent 개발 프로젝트에 참여한 Engineer B는 자동 포함되지 않습니다.

실제 pilot에서는 다음 질문도 확인합니다.

- CMX 프로젝트에 공식 참여한 팀과 연구원은 누구인가? 참여 기간과 소속 기간을 어떻게 다르게 보여줄 것인가?
- 어떤 Workload 분석이 특정 Storage Requirement를 도출했는가?
- 어떤 Agent 버전이 어떤 설계 Commit과 Simulation 결과를 만들었는가?
- HBF와 CMX 연구에 비교 가능한 Benchmark가 있는가? 조건이 다르면 무엇이 비교를 제한하는가?
- GPU·EDA 사용량을 개인 활동이 아닌 프로젝트·실행 ID에 어떻게 귀속할 것인가?

연구 조회는 원문 URL, 공개일과 정밀도, 조회일, 읽은 범위, 검증·발표 당시 제공 상태, 내부 재현 여부, 확인 내용과 한계를 반환합니다. `--as-of`는 문헌의 공개일 상한입니다. 월 단위 날짜는 해당 월의 말일 이후 조회에서 포함합니다. `curation_snapshot`은 분류를 작성한 날짜이며 과거 시점에 시스템이 알고 있던 상태를 재현하는 기능은 아닙니다. 출처에서 프로젝트로의 연결도 가상 프로젝트가 명시적으로 참조한 경우만 보여줍니다.

`executive-map`은 대표 기술 분야별 Topic과 연결된 공개 자료를 보여줍니다. 자료는 여러 분야에 중복될 수 있으며 출처 수를 검증 완료율·중요도·우선순위로 해석하지 않습니다. 공개일 미확인 자료는 별도 목록으로 보존하고, Watchlist 방향도 완료된 개발 영역과 구분합니다.

CLI는 public 범위 자료를 읽는 예제입니다. 사용자 인증·조직별 권한·민감 정보 필터링을 갖춘 실제 인사 검색 서비스로 사용하려면 별도 접근 제어가 필요합니다.
