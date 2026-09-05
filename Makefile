.PHONY: install-backend backend frontend dev

install-backend:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

backend:
	cd backend && . .venv/bin/activate && uvicorn main:app --reload --port 8000

frontend:
	python -m http.server 8080

dev: backend frontend
