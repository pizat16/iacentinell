# IA CENTINELL v6.0 — ENTERPRISE SECURITY PLATFORM

## 🚀 QUICK START

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 16+ (if running locally)

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/ia-centinell.git
cd ia-centinell

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Start with Docker
docker-compose up -d

# Initialize database
docker-compose exec backend python -m alembic upgrade head
