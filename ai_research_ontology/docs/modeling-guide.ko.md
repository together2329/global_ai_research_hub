# 모델링 기준 v0.4

Research Taxonomy는 기술 분류를, Organization & People은 조직과 사람의 이력을, Resource & Evidence는 개발·실행·검증의 관찰 기록을 담당합니다. ResearchProject가 이 축들을 연결합니다.

| 객체 묶음 | 주요 객체 | 등록 기준 |
| --- | --- | --- |
| 연구 분류 | ResearchPortfolio, ResearchArea, ResearchTopic | 통제 용어와 분류 경계 |
| 공통 연구 축 | WorkloadUseCase, Technique, Capability, ResearchSubject | 적용 환경·방법·기능·연구 대상을 구분 |
| 교차 분류 | DataObjectKind, SystemLayer, Bottleneck, ValidationStage | 데이터 종류·시스템 위치·해결 제약·검증 범위를 구분 |
| 외부 연구 | ExternalResearch, ResearchDirection, TechnologyInitiative | 공개 근거·분류 판단·업체 프로그램을 구분 |
| 조직·사람 | Organization, Person | HR 원본의 안정적 식별자에 매핑 |
| 이력 | OrganizationRelation, OrganizationMembership, ProjectMembership | 조직 상하위·소속·연구 참여의 기간 |
| 역할·전문성 | Role, RoleAssignment, Expertise, ExpertiseAssertion | 공식 지정 또는 검토 근거를 가진 주장 |
| 조직의 연구 참여 | OrganizationParticipation | 참여 조직을 공식 기록으로 확인 |
| 개발·자원 | Asset, Resource, AssetUsage | 구현 자산, 공유 실행 자원, 실제 사용 사실 |
| 검증 | Benchmark, Experiment, ExperimentRun, AgentExecution, Measurement | 설계한 평가와 실제 실행·수치를 구분 |
| 근거 | Artifact, Evidence, SourceRecord, RelationAssertion | 원본 위치, 관찰, 관계의 검증 상태 |

## 기술 분류와 조직의 연결

프로젝트는 `primary_area_ref` 하나와 `topic_refs` 하나 이상을 가집니다. 다른 분야가 실제로 관련되면 `related_area_refs`를 추가합니다. 프로젝트의 주된 질문과 산출물·인수 기준으로 대표 분야를 정합니다.

- AI Domain: 모델·Runtime·Serving·Agent 시스템 자체를 개선하는 연구.
- AX Engineering: AI로 반도체·소프트웨어 엔지니어링 업무를 수행하는 연구.
- AI Workload: 실행 특성을 분석해 Trace·모델·시스템 요구사항을 만드는 연구.
- AI Native Storage: 그 요구사항에 대응하는 메모리·스토리지 시스템을 설계·평가하는 연구.
- Shared Infra: 여러 연구에서 반복 활용하는 자원과 공통 서비스를 제공하는 연구.

하나의 팀이 여러 Area의 프로젝트를 수행할 수 있고, 하나의 프로젝트에 여러 팀이 참여할 수 있습니다. ResearchArea에는 Organization이나 Person을 자식으로 넣지 않습니다.

`work_kind`는 과학적 연구·솔루션 엔지니어링·플랫폼 개발·운영을 Area와 별도로 표현합니다. 5개 Area는 포트폴리오의 시작점이며 모든 국제 연구를 배타적으로 분할하는 보편 분류는 아닙니다.

## 기간과 안정적 ID

모든 소속·참여·역할·전문성 주장은 `[valid_from, valid_to)` 구간을 사용합니다. 시작일은 포함하고 종료일은 제외합니다. `valid_to: null`은 계속 유효함을 뜻합니다.

예시에서 `affiliation_a_old`는 2026-11-01 직전에 끝나고 `affiliation_a_new`는 2026-11-01부터 시작합니다. Person ID와 `membership_a_cxl` 프로젝트 참여 ID는 그대로 유지됩니다. 조직의 부모가 바뀌면 OrganizationRelation 기간을 닫고 새 관계를 추가합니다. 같은 조직의 명칭 변경은 ID를 유지하고 변경 이력을 보존하며, 실체가 분리·통합되면 새 ID와 근거 있는 `SUPERSEDES` 관계를 사용합니다.

`valid_from/valid_to`는 사실이 유효한 시간이고 `recorded_at`은 이를 기록한 시간입니다. 현재 예시 조회는 유효 시간의 `as_of` 조회를 지원합니다. 과거에 시스템이 무엇을 알고 있었는지까지 재현하는 완전한 이중 시간 조회는 구현돼 있지 않습니다.

## 소속, 참여, 역할, 전문성

Person에 현재 팀·프로젝트·전문성을 단일 문자열로 저장하지 않습니다.

1. OrganizationMembership은 조직 소속입니다. HR 근거와 소속 기간을 기록합니다.
2. ProjectMembership은 연구 참여입니다. 조직 이동과 별개로 참여가 지속될 수 있습니다.
3. RoleAssignment는 해당 참여 기간 안에서 유효한 Project Owner·Developer·Reviewer 역할입니다.
4. ExpertiseAssertion은 특정 기술 전문성에 대한 근거·평가 방법·검토자·기간·검증 상태입니다.

프로젝트 Owner 표시는 현재 유효하고 검증된 `role_project_owner` 역할 지정에서 계산합니다. Git 작성자 필드와 중복 저장하지 않습니다. 전문성도 Git Commit 수나 파일명으로 확정하지 않습니다. 그런 단서는 `candidate`이며, 공식 프로필 또는 검토된 수행 결과가 있어야 `verified`로 승격할 수 있습니다. 현재의 practitioner/specialist/expert 용어는 제안된 수준이며 조직이 평가 기준을 정해야 합니다.

OrganizationParticipation은 프로젝트에 참여하는 팀·조직을 명시합니다. 개인의 현재 소속만으로 조직의 연구 참여를 자동 생성하지 않습니다.

## 자산과 실제 사용

CMX는 Platform 종류의 Asset, RTL Agent v1은 버전이 있는 Agent Asset, RTL Generation은 Capability, B200 GPU Pool은 Resource입니다. KV Cache는 ResearchSubject, Offloading은 Technique, Offloading Optimization은 ResearchTopic으로 구분합니다.

`planned_asset_refs`는 연구가 사용하려는 자산입니다. 실제 사용자는 AssetUsage에서 찾습니다. 이 기록은 Person·Asset·Project·Execution과 실행 시각·근거를 연결합니다. 자산 사용 사실로 전문성이나 프로젝트 책임을 자동 부여하지 않습니다.

CMX와 HBF는 별개 개념입니다. 같은 Workload를 대상으로 연구한다는 이유로 `COMPATIBLE_WITH`를 만들지 않습니다. 검증된 호환 관계에는 실험 근거가 필요합니다.

NVIDIA Storage-Next는 TechnologyInitiative이고 GPU-Initiated Storage는 일반 기술 Topic입니다. 프로그램과 연결된 프로젝트가 모든 SDK·장치와 호환된다는 의미는 아닙니다. Embedding Vector·ANN Index·KV Cache·Agent Memory는 DataObjectKind로 구분합니다. DataObjectKind는 데이터 종류이고 Artifact는 실제 파일·버전입니다. 기존 ResearchSubject와 같은 개념이면 `subject_ref`로 연결합니다.

## 실험과 결과

Experiment는 반복 가능한 평가 설계이고 ExperimentRun은 한 번의 실제 실행입니다. AgentExecution은 실행된 Agent 버전과 요청자를 연결합니다. 코드 Commit은 Artifact로 참조하고 실행 설정·자원·로그·결과를 별도로 기록합니다.

EvaluationMetric은 정의, 단위, 필요한 조건을 가집니다. Measurement는 실행의 값과 단위·집계 방식·조건·근거를 가집니다. `contract_status: candidate`인 지표에는 Measurement를 등록할 수 없습니다. PPA는 하나의 단위 없는 값이 아니라 Power·Performance·Area의 묶음이며 각 값을 구체적인 지표로 정의해야 합니다.

예시의 Simulation Pass Rate 1.0은 가상 48/48 테스트의 비율입니다. 기능 완전성이나 실제 양산 검증을 뜻하지 않습니다. 실제 비교에는 Benchmark 버전, 설계·모델 버전, 부하, 도구, 측정 구간 등 지표 계약의 조건을 함께 보존합니다.

Vector QPS는 같은 Run·Benchmark·조건의 Recall@k와 p99를 함께 등록하고 최소 Recall을 명시합니다. 작은 I/O IOPS도 같은 조건의 p99를 동반합니다. Metric의 `required_companion_metric_refs`가 이 연결을 정의합니다. Recall 비율은 테스트 통과율의 passed_count/total_count 산식과 구분합니다. 신규 Metric의 자세한 조건은 [연구 동향 반영 근거](research-landscape-20261108.ko.md)를 참고합니다.

## 공개 문헌과 내부 검증

ExternalResearch는 SourceRecord의 원문·공개일·조회 시각과 확인된 내용·한계·검토 범위를 연결합니다. `inspection_scope: paper_abstract`는 초록 확인이며 전체 논문의 실험 검증이 아닙니다. 공개일이 월 단위면 월 단위로 유지합니다. 사건 일자는 `event_started_on/event_ended_on`으로 공개일과 분리할 수 있습니다.

`review_status`는 출처의 심사·공개 유형이고 `validation_stage_ref`는 제시한 검증 범위, `availability_at_publication`은 발표 당시 제공 상태입니다. `internal_reproduction_status`는 별도이며 실제 내부 실행 근거 없이 reproduced로 바꾸지 않습니다. 공식 업체 발표는 업체 발표 내용의 출처이며 성능에 대한 독립 검증은 아닙니다.

ResearchDirection은 시점별로 선정한 연구 방향입니다. Topic·Facet 연결은 분류자의 판단이며 이를 외부 기관의 확정 분류 또는 조직의 승인 전략으로 표시하지 않습니다. ResearchProject의 `external_research_refs`는 참고 문헌 연결이고 해당 기술의 실제 사용·성과는 실행과 실험 근거로 기록합니다.

## 관계와 근거

명시적인 참조 필드는 타입이 정해진 그래프 연결을 제공합니다. 기간·역할·평가 맥락이 필요한 관계는 독립 객체로 만듭니다. 추가 기술 연결은 RelationAssertion으로 기록합니다.

`candidate`, `verified`, `rejected`를 구분하고, 검증된 주장에는 Evidence와 SourceRecord가 연결돼야 합니다. 공식 시스템 기록과 AI가 제안한 기술적 관련성을 같은 기준으로 취급하지 않습니다. 기술적 의미의 최종 검토는 해당 Research Owner와 Domain Steward의 책임입니다.
