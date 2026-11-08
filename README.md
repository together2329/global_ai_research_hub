# Global AI Research Hub

AI·반도체·메모리·스토리지 연구를 찾고, 관련 기술과 사람, 개발 자산, 실험 근거를 연결하기 위한 연구 지식 저장소입니다.

첫 모듈은 [ai_research_ontology](ai_research_ontology/README.md)입니다. Memory Solutions Research Taxonomy v0.2에 Organization & People 모델을 더한 **v0.3 제안 초안**을 담습니다.

| 구성 | 내용 |
| --- | --- |
| Research Taxonomy | AI Domain · AX Engineering · AI Workload · AI Native Storage · Shared Infra |
| Organization & People | 조직, 사람, 역할, 전문성, 기간이 있는 소속·연구 참여 이력 |
| Resource & Evidence | Asset, Agent 실행, 자원 사용, Experiment, Measurement, 원본 근거 |

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 ai_research_ontology/scripts/validate.py
python3 -m unittest discover -s ai_research_ontology/tests -v
python3 ai_research_ontology/scripts/query.py --query all
```

현재 포함된 사람·조직·프로젝트·실행·측정값은 모두 가상 예시입니다. 실제 연구 목록과 HR 연동을 적용하기 전의 모델 검토 단계입니다.
