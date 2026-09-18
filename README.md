# NEXTO — SNS 정보를 검증된 다음 행동으로

SNS에서 발견한 정보를 AI가 공식 출처로 검증하고, 캘린더·장소·실행 항목으로 바꾸는 Personal Action Agent.
원티드 AI 챔피언십 2026 · 명세서 v3.0 기준.

## 구조
```
NEXTO_Wicked/
├── frontend/   Vue 3 + Vite + Pinia (SCR-01~05)
├── backend/    FastAPI 단일 백엔드 — API + AI 파이프라인 + DB
│   ├── app/api/        라우터 (auth, shares, jobs, items, calendar)
│   ├── app/pipeline/   understand → extract → normalize → search → verify
│   ├── app/services/   job 실행, SSE, 등급 산정
│   ├── app/db/         SQLAlchemy 모델 + 세션
│   ├── fixtures/demo/  데모모드 fallback 결과
│   └── eval/golden/    골든셋 20건 + 평가 스크립트
├── docs/       명세서
└── docker-compose.yml
```

## 빠른 시작
```bash
cp .env.example .env
docker compose up --build      # web:5173 / api:8000 / db:5432
```
개별 실행
```bash
cd backend  && pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm i && npm run dev
```

## 핵심 흐름
`POST /api/shares` → job QUEUED → BackgroundTask가 단계 실행(결과를 단계별 DB 저장) →
`GET /api/jobs/{id}/stream`(SSE) 또는 2초 polling → `GET /api/shares/{id}/result` → `POST /api/items`.
외부 API 3회 연속 실패 시 `fixtures/demo/`로 fallback (DEMO_MODE).

## 신뢰등급
숫자 confidence 없음. HIGH / REVIEW / UNVERIFIED 3단계 + 필드별 상태(VERIFIED/REFINED/CONFLICT/ADDED/AMBIGUOUS/UNVERIFIED).

## 브랜치
`main`(데모 가능) ← `dev` ← `feat/fe-*`, `feat/be-*`, `feat/ai-*`
