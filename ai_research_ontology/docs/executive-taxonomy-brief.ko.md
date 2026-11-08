# Memory Solutions 연구 Taxonomy 고도화 제안

부문장 보고용 초안 · 2026-11-08 KST · 조직의 확정 분류 또는 승인된 투자 계획이 아님

## 보고 요지

**AI Workload의 변화를 메모리·스토리지 솔루션 기회와 검증 가능한 개발 역량으로 연결하는 연구 지도를 제안한다.** 보고 화면은 6개 기술 분야로 정리하고, 기존 5개 Research Area는 연구 포트폴리오 관리에 유지한다. 조직·사람·자원·성과는 같은 프로젝트 ID를 중심으로 별도 연결한다.

분류의 완성도는 Topic 수보다 실제 연구를 빠짐없이 찾고, 중복 책임을 줄이며, 비교 가능한 근거로 다음 의사결정을 내릴 수 있는지로 판단한다. 현재 버전은 공개 자료와 가상 프로젝트로 구조를 검토한 초안이다. 실제 조직 연구 목록에 대한 분류 정확도는 아직 측정하지 않았다.

## 1. 공개 발언에서 확인되는 방향과 이번 설계의 해석

SK hynix의 [FMS 2026 공식 기사](https://news.skhynix.com/en/fms-2026/)는 김천성님의 발언을 통해 메모리 계층의 배치·연결과 데이터 이동 최소화가 시스템 효율에 중요하다고 설명한다. 기사 공개일은 2026-08-07이며 행사는 2026-08-04~06에 열렸다. 조회일은 2026-11-08 KST다.

**설계 해석:** 연구 목록에 제품과 기술명을 등록하는 것에 더해, 고객 Workload·시스템 병목·계층 간 연결·검증 결과를 함께 보여주는 구성이 이 공개 방향과 부합한다. 이것은 공개 자료에 근거한 보고 구성 제안이며, 부문장님의 내부 지시나 조직별 역할을 확인했다는 의미는 아니다.

## 2. 제안하는 6개 기술 분야

| 기술 분야 | 포함할 대표 연구 | 부문장 관점의 질문 | 역할 구분 예시 — 검토안 |
| --- | --- | --- | --- |
| **AI Models & Agent Systems** | MoE·SSM/Attention·Reasoning Budget·멀티모달·World Model·Agent 협업 | 모델 변화가 어떤 메모리·통신·저장 수요를 만드는가? | 선행 관찰·Workload 요구 도출 |
| **Retrieval, Knowledge & Data Systems** | Vector Search·RAG·Index·Agent 장기 기억·데이터/지식 관리 | 고객이 필요한 정보를 어떤 품질·최신성·지연으로 찾는가? | 고객 Use Case·공동 설계 |
| **AI Runtime & Distributed Systems** | Training/Serving·Kernel·Compiler·분산 병렬화·Collective·이종 가속기 | 메모리 병목이 실제 시스템 성능·효율을 얼마나 제한하는가? | 공동 최적화·시스템 검증 |
| **Memory Architecture & Interconnect** | HBM·DRAM·CXL·HBF·계층 배치·Chiplet/Package·메모리 RAS | 어떤 계층 구성과 연결 방식이 제약을 해결하는가? | 차별화 솔루션 개발 후보 |
| **Storage Systems & Data Paths** | SSD·Controller/Firmware·GPU 주도 I/O·KV/Checkpoint·File/Object·Computational Storage | 데이터 이동·보존·복구를 어떤 구조로 해결하는가? | 차별화 솔루션 개발 후보 |
| **AI for Engineering & Design** | Spec/RTL·Verification·Firmware·EDA·평가기 기반 탐색·개발 Workflow | AI가 만든 산출물을 어떤 검증으로 실제 개발에 재사용하는가? | 내부 개발 역량·생산성 개선 |

위 역할 예시는 자원 배분 결정이나 확정된 담당 조직이 아니다. 동일 기술 분야에서도 선행 연구·솔루션 개발·플랫폼 운영의 성격은 `work_kind`로 구분한다. 실제 개발 범위와 고객 검증 계획을 확인한 뒤 역할을 확정한다.

보안·개인정보, 품질·정확성, 신뢰성·복구, 전력·열·비용, 표준·상호운용, 평가·재현성의 **6개 공통 관점**을 모든 분야에 적용한다. 이들은 별도 팀으로 격리하는 상위 Area가 아니라 각 연구가 검토해야 할 제약과 인수 기준이다.

## 3. 현재 구조에서 보완한 내용

v0.4의 외부 자료 14건은 모두 AI Native Storage의 Topic과 연결돼 있었고 AX Engineering에 연결된 자료는 없었다. 따라서 그 버전을 부문 전체의 균형 잡힌 글로벌 연구 지도라고 제시하기에는 근거가 부족했다. Topic의 존재와 그 분야 문헌의 실제 검토를 구분해야 한다.

이번 v0.5에서는 모델·Agent 평가·Runtime/Compiler·Chiplet/CXL·엔지니어링 자동화·Edge 에너지·보안을 다룬 1차 자료 11건을 추가했다. 총 25건 중 1건은 공개일 미확인이다. 각 자료의 내용·검토 범위·한계를 보존했고 모두 내부 재현 전으로 등록했다. [보강 근거와 남은 조사 범위](executive-taxonomy-evidence.ko.md)

기존 5개 Area와 모든 ID를 보존하면서, 6개 TechnologyDomain을 독립 축으로 추가해 243개 세부 Topic을 각각 하나의 대표 기술 분야에 매핑했다. 필요한 관련 분야는 별도 참조로 표현한다. 모든 Topic이 개별 최신 논문 또는 조직 프로젝트로 검증됐다는 뜻은 아니다.

| 기존 Research Area | 유지하는 목적 | 새 기술 분야와의 관계 |
| --- | --- | --- |
| AI Domain | 모델·Agent·응용·Runtime 연구 포트폴리오 | Models/Agents, Retrieval/Data, Runtime 등으로 기술 내용을 구분 |
| AX Engineering | AI를 통한 엔지니어링 개선 포트폴리오 | 주로 Engineering, 필요 시 Runtime·Data와 연결 |
| AI Workload | 실행 특성·Trace·요구사항 분석 포트폴리오 | 분석 대상이 되는 모델·메모리·스토리지·분산 실행 분야와 연결 |
| AI Native Storage | 메모리·스토리지 솔루션 설계·검증 포트폴리오 | Memory/Interconnect, Storage/Data Paths, Retrieval 등과 연결 |
| Shared Infra | 공동 자원·서비스·연구 플랫폼 포트폴리오 | Runtime·Data·Engineering 기반 기술과 연결 |

## 4. 경계가 모호한 연구를 분류하는 기준

연구의 **주된 질문·산출물·인수 기준**으로 대표 기술 분야를 선택한다. 사용하는 도구·현재 소속·제품명으로 결정하지 않는다.

| 예시 | 대표 기술 분야 | 관련 분야와 구분 기준 |
| --- | --- | --- |
| Vector 검색의 Recall·Filter·Index 구조 개선 | Retrieval, Knowledge & Data Systems | SSD 경로가 실제 연구 대상이면 Storage를 추가 연결 |
| Vector 검색용 SSD Firmware의 Tail Latency 개선 | Storage Systems & Data Paths | Vector는 대상 Workload이며 검색 품질도 공통 인수 조건 |
| GPU-Initiated Storage·SCADA 경로 설계 | Storage Systems & Data Paths | Storage-Next 프로그램, SDK, 제품과 실제 호환 실험을 별도 객체로 연결 |
| MoE 통신 Trace 분석과 병렬 실행 최적화 | AI Runtime & Distributed Systems | Workload 분석은 AI Workload 포트폴리오, Memory/Interconnect는 관련 분야 |
| CXL Pooling·메모리 장애 복구 설계 | Memory Architecture & Interconnect | 규격 소개·시뮬레이션·제품 검증을 서로 다른 근거로 표시 |
| RTL/EDA Agent 개발과 독립 검증 | AI for Engineering & Design | 사용 모델·GPU와 실제 설계 성과를 구분 |

## 5. 부문 보고에서 프로젝트마다 보여줄 항목

1. 대상 고객 또는 내부 사용자와 해결할 Use Case
2. 현재 시스템 병목과 이를 확인한 Trace·실험·원문 근거
3. 대표 기술 분야, 관련 분야, 기존 포트폴리오 Area
4. 해결 가설·개발할 Asset·재사용 가능한 Capability
5. 책임자·참여 조직·필요 자원과 기간
6. 현재 검증 단계·내부 재현 여부·남은 기술 불확실성
7. 품질·SLO 조건을 보존한 성능·에너지·비용 또는 개발 품질 지표
8. 다음 검증 실험과 그 결과에 따른 계속·전환·종료 판단

위 항목은 보고 양식 제안이다. 실제 고객·책임자·예산·사업 성과는 원본과 승인 근거가 있을 때만 입력한다. 현재 예시 데이터로 ROI나 개발 생산성 향상을 주장하지 않는다.

## 6. 검토 요청 사항과 적용 절차

**검토 요청:** 6개 기술 분야와 6개 공통 관점을 보고용 초안으로 적용하고, 실제 연구 20~30개를 선정해 분류 경계와 근거 연결을 검토한다.

- 서로 다른 검토자가 같은 연구의 대표 분야·Area·인수 기준을 분류하고 불일치 이유를 남긴다.
- 미분류·억지 분류·중복 책임·용어 중복·판단 보류 항목을 기록한다. 분류 일치율과 근거 완전성을 측정한 뒤 조직이 수용 기준을 정한다.
- Vector Search, 계층 메모리/GPU Storage, Engineering Agent를 연결 사례로 검토한다. 문헌 → 요구사항 → 개발 자산 → 실행·검증 → 재사용을 실제 근거로 추적한다.
- 경계가 안정되면 용어 정의·담당 Steward·변경 규칙을 확정한다. 현재 조직 개편이나 인력 평가 기준으로 바로 사용하지 않는다.

현 단계에서 보고할 수 있는 성과는 **기술 분야·근거·프로젝트를 연결할 수 있는 구조와 조회 예제를 마련했다는 것**이다. 실제 조직 적용성·연구 우선순위·고객 효과는 Pilot과 검증 실험을 통해 확정해야 한다.
