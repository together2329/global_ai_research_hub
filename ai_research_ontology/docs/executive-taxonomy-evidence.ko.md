# 보고용 기술 분야 확장의 근거와 한계

조회일: 2026-11-08 KST. v0.4의 14건에 아래 11건을 추가했다. 출처 내용 확인과 분류 매핑은 내부 재현 또는 조직의 실제 채택을 뜻하지 않는다. 6개 기술 분야는 이 저장소의 설계 제안이며 출처 기관들의 공통 분류라는 의미는 아니다.

## 추가 확인한 1차 자료

| 자료 | 공개일 | 확인 범위·분류에 반영한 내용 | 제한과 후속 검토 |
| --- | --- | --- | --- |
| [NVIDIA Nemotron 3 Super](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/) | 2026-03-11 | 기술 글: SSM/Attention·MoE·Multi-token Prediction·저정밀 학습 | 업체 조건의 결과이며 다른 모델의 메모리 요구나 성능으로 일반화하지 않음 |
| [Google Agent Scaling](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) | 2026-01-28 | 연구 소개 글: 협업 구조·Task 의존성과 조정 비용 평가 | 전체 논문 재현 전이며 Agent 수와 성과의 보편 관계를 확인한 것은 아님 |
| [Google DeepMind AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/) | 2026-05-07 | 기술 글: 평가기 기반 탐색의 설계·Cache 정책·Compaction 적용 | 업체 보고 적용 사례이며 자체 엔지니어링 효과는 별도 검증 필요 |
| [NIST Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) | 2026-02-17 | 공식 발표: 상호운용·보안·식별 연구와 프로토콜 개발 방향 | 완성된 의무 규격이나 개별 제품 보안 인증이 아님 |
| [PyTorch Conference 2026 정리](https://pytorch.org/blog/pytorch-conference-north-america-2026-accelerating-open-intelligence-together/) | 2026-10-22 | 공식 글: Backend·Compiler·병렬화·통신·Edge 실행 | 행사 2026-10-20~21. 개별 프로젝트의 지원 상태와 검증 조건은 다름 |
| [UCIe 3.0 기술 소개](https://www.uciexpress.org/post/ucie-3-0-specification-redefining-chiplet-interconnects) | 2025-09-03 | 표준기관 글: Package 내 연결·전력·관리 기능 | 글의 공개일이며 최초 규격 공개일과 구분. 전체 조항·제품 적합성 미검토 |
| [CXL 공식 Pressroom](https://computeexpresslink.org/news/) | 2025-11-18, 규격 공개 항목 | CXL 4.0 공개 상태와 날짜 | RAS·Pooling 상세 조항 또는 구현 호환을 확인한 자료로 사용하지 않음 |
| [MLPerf Inference v6.1 분석](https://mlcommons.org/2026/09/chairs-mlperf-inference-v6-1/) | 2026-09-17 | 공식 분석: End-to-end RAG·Agentic Edge와 시나리오별 평가 | 다른 Benchmark 간 점수 비교·일반적인 Agent 성과로 확대하지 않음 |
| [MLPerf Tiny v1.4](https://mlcommons.org/2026/07/mlperf-tiny-v1-4-results/) | 2026-07-07 | 공식 글: 품질 조건 아래 지연·에너지 평가 | Edge/TinyML의 근거로 Datacenter 에너지·TCO를 단정하지 않음 |
| [Kimi K3 기술 글](https://www.kimi.com/en/blog/kimi-k3) · [날짜 확인 Index](https://www.kimi.com/en/blog/) | 2026-07-16 | 업체 글: 모델 구조·Kernel·Compiler·Chip 설계의 초기 사례 | Chip 사례는 시뮬레이션 기반이며 실제 실리콘 성능으로 해석하지 않음. 예고한 Weight 공개는 별도 확인 대상 |
| [Google DeepMind Genie 4 소개](https://deepmind.google/models/genie/) | 미확인 | 조회 시 공식 페이지의 상호작용 세계 시뮬레이션 설명 | 공개일을 추정하지 않음. 제품 소개와 정량 메모리 분석·실환경 로봇 검증을 구분 |

성능 배수나 제품별 우열 수치는 이번 등록에 사용하지 않았다. 세부 내용은 [공개 연구 Registry](../research/public_research_registry.yaml)의 `inspection_scope`, `availability_at_publication`, `key_findings`, `limitations`에 기록했다. 모두 `internal_reproduction_status: not_reproduced`다.

## 여전히 보완해야 하는 분야

- **메모리·패키지:** HBM/Logic Base Die·3D/Chiplet·열·신호 무결성의 정량 설계 근거, PIM/PNM, 실제 RAS·복구 검증.
- **분산 시스템:** Scale-up/Scale-out 네트워크·광 연결·Collective의 Trace·정량 병목과 고객 구성별 실험.
- **엔지니어링:** 실제 RTL/Verification/Firmware/EDA Task의 독립 인수 결과, 전체 개발 시간과 검토 비용. 업체 사례만으로 내부 생산성을 추정할 수 없음.
- **신뢰·효율:** Prompt Injection·권한 위임·데이터 유출·오류 전파의 실제 평가, Datacenter 전력·열·비용 측정 경계와 품질/SLO 조건.
- **선행 관찰:** Physical AI·World Model·On-device AI의 메모리/스토리지 요구를 확인할 Trace와 실제 Use Case. 모델 개발 전체를 Memory Solutions가 담당한다는 제안은 아님.
- **범위:** 최신 학회·국가·기업을 전수 조사하지 않았다. AI for Science·Quantum AI 등은 직접적인 고객/시스템 요구가 확인될 때 별도 조사·분류 확장을 검토한다.

## 분류 품질을 확인하는 방법

| 확인할 항목 | 측정 또는 검토 방법 | 현재 상태 |
| --- | --- | --- |
| 포괄성 | 실제 프로젝트 중 미분류·억지 분류·추가 용어가 필요한 비중 | 실제 프로젝트 미적재, 측정 전 |
| 경계의 명확성 | 독립 검토자의 대표 분야·Area 일치율과 불일치 사유 | Pilot 예정 |
| 기술·제품·조직 구분 | Topic·Technique·Initiative·Asset·Organization 타입 혼용 점검 | 타입·참조 검사 구현, 조직 적용성 검토 전 |
| 최신성과 근거 | 원문·공개일 정밀도·조회일·확인 범위·한계의 존재와 내용 검토 | 공개 자료 25건 등록, 전수 수집 아님 |
| 성과의 신뢰성 | 외부 주장·내부 재현·실제 운영을 구분하고 실행·조건·근거 추적 | 구조 구현, 실제 내부 성과 없음 |
| 활용성 | 전문가 탐색·기술 재사용·중복 과제 발견·후속 검증 결정 사례 | 가상 조회 예제 검증, 현업 효과 측정 전 |

Topic 수와 테스트 통과는 위 항목의 모든 답을 대신하지 않는다. 수용 기준과 우선순위는 실제 연구 Owner·Domain Steward·부문 의사결정자가 Pilot 결과를 보고 정한다.

## 재현 가능한 조회

```bash
python3 ai_research_ontology/scripts/query.py --query executive-map
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction engineering_intelligence
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction runtime_compiler
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction world_edge
```

`executive-map`의 출처 수는 Topic 매핑을 따라 연결된 자료의 수다. 자료 하나가 여러 분야에 중복 집계될 수 있고, 이 수는 분야의 중요도·성숙도·검증 완료율이 아니다. 공개일 미확인 자료는 별도 목록으로 표시한다. `research-landscape`는 날짜 상한 조회에서 날짜 미확인 자료를 결과 본문에 포함하지 않고 해당 ID를 별도로 남긴다.
