# Global AI Research Hub

AI·반도체·메모리·스토리지 연구를 찾고, 관련 기술과 사람, 개발 자산, 실험 근거를 연결하기 위한 연구 지식 저장소입니다.

첫 모듈은 [ai_research_ontology](ai_research_ontology/README.md)입니다. Memory Solutions의 연구 분류와 조직·사람 모델에 공개 연구 근거를 연결한 **v0.5 제안 초안**을 담습니다. [부문장 보고용 제안서](ai_research_ontology/docs/executive-taxonomy-brief.ko.md)는 기존 5개 포트폴리오 Area와 독립된 6개 기술 분야·6개 공통 관점으로 연구 지도를 정리합니다.

| 구성 | 내용 |
| --- | --- |
| Research Taxonomy | AI Domain · AX Engineering · AI Workload · AI Native Storage · Shared Infra |
| Executive Technical View | Models/Agents · Retrieval/Data · Runtime/Distributed · Memory/Interconnect · Storage/Data Paths · Engineering AI |
| Organization & People | 조직, 사람, 역할, 전문성, 기간이 있는 소속·연구 참여 이력 |
| Resource & Evidence | Asset, Agent 실행, 자원 사용, Experiment, Measurement, 원본 근거 |
| Public Research | 공개 자료 25건, 18개 연구 방향, 데이터 종류·시스템 계층·병목·검증 범위 |

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 ai_research_ontology/scripts/validate.py
python3 -m unittest discover -s ai_research_ontology/tests -v
python3 ai_research_ontology/scripts/query.py --query all
python3 ai_research_ontology/scripts/query.py --query executive-map
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction vector_search
python3 ai_research_ontology/scripts/query.py --query research-landscape --direction storage_next
```

현재 포함된 사람·조직·내부 프로젝트·실행·측정값은 모두 가상 예시입니다. 공개 문헌 목록은 실제 출처이며 내부 재현 결과와 구분합니다. 세계 연구를 전수 수집한 목록은 아닙니다. 범위와 한계는 [연구 동향 반영 근거](ai_research_ontology/docs/research-landscape-20261108.ko.md)에 기록했습니다.
