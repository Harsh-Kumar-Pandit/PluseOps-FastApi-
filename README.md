<div align="center">

# ⚡ PulseOps

### IT & DevOps Monitoring and Incident Management Platform

*A production-style, containerized backend system for real-time monitoring, alerting, and incident response — built with FastAPI, Celery, Redis, and PostgreSQL.*

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Distributed%20Tasks-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20(Access%2FRefresh)-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

</div>

---

## 📌 Overview

**PulseOps** is a full-stack **IT/DevOps monitoring and incident management** system designed the way real production platforms are built — with a clean separation between the **API layer**, **asynchronous task processing**, and **scheduled background monitoring**.

At its core, PulseOps is built to answer the questions every ops/SRE team needs answered in real time:

- Is a service healthy right now?
- If something breaks, who gets notified, and how fast?
- What's the history of incidents, and how are they being tracked to resolution?

The system runs entirely on **Docker Compose**, orchestrating five independent services — API server, database, cache/broker, background worker, and task scheduler — mirroring how monitoring platforms are architected in production environments.

---

## 🏗️ System Architecture

\`\`\`
                         ┌─────────────────────┐
                         │      Frontend        │
                         │   (Client / Dashboard)│
                         └──────────┬───────────┘
                                    │ REST API (JWT Auth)
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend     │
                         │  (Auth, Monitoring,   │
                         │   Incidents, Alerts)  │
                         └──────┬───────┬────────┘
                                │       │
                     ┌──────────┘       └──────────┐
                     ▼                              ▼
           ┌──────────────────┐          ┌────────────────────┐
           │   PostgreSQL 16   │          │       Redis          │
           │  (Persistent Data)│          │ (Broker / Cache)     │
           └──────────────────┘          └─────────┬───────────┘
                                                      │
                                    ┌─────────────────┴──────────────────┐
                                    ▼                                     ▼
                        ┌─────────────────────┐             ┌─────────────────────┐
                        │   Celery Worker       │             │   Celery Beat         │
                        │ (Async Task Execution)│             │ (Scheduled Health/    │
                        │ e.g. alert dispatch,  │             │  Uptime Checks &       │
                        │ notification jobs)     │             │  Periodic Scans)       │
                        └─────────────────────┘             └─────────────────────┘
\`\`\`

Every service above runs as its own container, defined and networked together via \`docker-compose.yml\` — a genuine multi-service, event-driven backend rather than a single monolithic script.

---

## ✨ Key Features

- 🔐 **Secure Authentication** — JWT-based access & refresh token flow for stateless, scalable session management
- 📡 **Real-Time Monitoring** — Continuous service/health checks executed on a schedule via Celery Beat
- 🚨 **Incident & Alert Management** — Detected issues flow into an incident pipeline for tracking and resolution
- ⚙️ **Asynchronous Task Processing** — Celery workers handle heavy/background jobs (notifications, checks, alert dispatch) off the request/response cycle
- 🗃️ **Persistent Data Layer** — PostgreSQL for durable storage of services, incidents, users, and monitoring history
- ⚡ **Fast, Cache-Backed Operations** — Redis as both the Celery broker and an application-level cache
- 🐳 **Fully Containerized** — One-command startup for the entire stack (API, DB, cache, worker, scheduler) via Docker Compose
- 🧪 **Type-Safe Python** — Static type checking enforced with [Pyrefly](https://pyrefly.org/) for a more reliable backend codebase

---

## 🛠️ Tech Stack

| Layer               | Technology                                   |
| ------------------- | --------------------------------------------- |
| **API Framework**   | FastAPI (Python)                               |
| **Authentication**  | JWT — Access & Refresh Tokens                  |
| **Database**        | PostgreSQL 16                                  |
| **Cache / Broker**  | Redis 7                                        |
| **Async Tasks**     | Celery Worker                                  |
| **Job Scheduling**  | Celery Beat                                    |
| **Frontend**        | JavaScript/TypeScript client (\`frontend/\`)     |
| **Containerization**| Docker & Docker Compose                        |
| **Type Checking**   | Pyrefly                                        |

---

## 📁 Project Structure

\`\`\`
PluseOps/
├── backend/            # FastAPI app — auth, monitoring, incidents, Celery tasks
├── frontend/           # Client dashboard application
├── docs/               # Project & architecture documentation
├── .vscode/            # Editor configuration
├── docker-compose.yml  # Multi-service orchestration (API, DB, Redis, worker, beat)
├── pyproject.toml      # Python tooling config (Pyrefly static type checking)
└── .gitignore
\`\`\`

---

## 🐳 Running the Full Stack

### Prerequisites
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- Git

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/Harsh-Kumar-Pandit/PluseOps.git
cd PluseOps
\`\`\`

### 2. Configure environment variables

Create a \`.env\` file in \`backend/\` with your database, Redis, and JWT settings:

\`\`\`env
DATABASE_URL=postgresql://postgres:1234@db:5432/pulseops
REDIS_URL=redis://redis:6379/0

JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
\`\`\`

### 3. Launch everything with one command

\`\`\`bash
docker-compose up --build
\`\`\`

This starts all five services:

| Service   | Role                                        | Port    |
| --------- | -------------------------------------------- | ------- |
| \`backend\` | FastAPI REST API                             | \`8000\`  |
| \`db\`      | PostgreSQL 16 database                       | \`5432\`  |
| \`redis\`   | Broker + cache for Celery                    | \`6379\`  |
| \`worker\`  | Celery worker — executes async jobs          | —       |
| \`beat\`    | Celery beat — triggers scheduled health checks| —      |

API available at: **\`http://localhost:8000\`**

### 4. Run the frontend

\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

---

## 🔑 Authentication Flow

PulseOps uses a standard **JWT access + refresh token** pattern:

1. User logs in → receives a short-lived **access token** and a longer-lived **refresh token**
2. Access token authorizes protected API requests
3. When the access token expires, the client uses the refresh token to obtain a new one — without forcing re-login
4. Refresh tokens can be revoked to support secure logout across sessions

---

## ⚙️ Background Processing

\`\`\`bash
# Celery worker — executes queued tasks (alerts, notifications, checks)
celery -A app.core.celery_app.celery_app worker --loglevel=info

# Celery beat — schedules periodic monitoring jobs
celery -A app.core.celery_app.celery_app beat --loglevel=info
\`\`\`

Both run as dedicated, always-on services inside Docker Compose — decoupled from the API so monitoring keeps running independently of user traffic.

---

## 🗺️ Roadmap

- [ ] Expand alerting integrations (Slack/Email/Webhooks)
- [ ] Incident timeline & post-mortem reporting
- [ ] Role-based access control (RBAC)
- [ ] CI/CD pipeline & automated test suite
- [ ] Production deployment guide (Kubernetes/Cloud)

---

## 👤 Author

**Harsh Kumar Pandit**
B.Tech CSE, GGITS Jabalpur (RGPV) — SDE Aspirant, Full-Stack & AI Integration

[![GitHub](https://img.shields.io/badge/GitHub-Harsh--Kumar--Pandit-181717?style=flat&logo=github)](https://github.com/Harsh-Kumar-Pandit)

---

<div align="center">

*Built to demonstrate real-world backend architecture: async processing, scheduled jobs, secure auth, and container orchestration.*

</div>
