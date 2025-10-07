PY=python

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

ingest:
	$(PY) data_ingest/ingest_medlineplus.py
	$(PY) data_ingest/ingest_cdc.py

run:
	uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

eval:
	$(PY) eval/ragas_eval.py
