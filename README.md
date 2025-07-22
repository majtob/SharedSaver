# SharedSaver

A fintech application for shared saving and lending accounts among family members or groups of friends. Participants can contribute to funding the account for saving purposes and take interest-free loans from the shared pool.

## Features

- **Shared Accounts**: Create and manage shared saving accounts for families or friend groups
- **Contributions**: Members can contribute funds to the shared account
- **Interest-Free Loans**: Participants can borrow from the shared pool without interest
- **Transparency**: Track all transactions, contributions, and loans
- **Notifications**: Real-time updates on account activities

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: React (TypeScript) + Tailwind CSS
- **Database**: PostgreSQL
- **Authentication**: Django REST Framework with JWT
- **API**: RESTful API with Django REST Framework

## Project Structure

```
SharedSaver/
├── sharedsaver/          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                # User management app
├── accounts/             # Shared accounts app
├── transactions/         # Transactions app
├── loans/                # Loans app
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker setup
├── Dockerfile          # Docker configuration
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.11+
- Conda (recommended) or pip
- PostgreSQL

### Option 1: Using Docker (Recommended)

1. **Install Docker Desktop** (if not already installed):
   ```bash
   brew install --cask docker
   ```

2. **Start Docker Desktop** and wait for it to be ready

3. **Start the database services**:
   ```bash
   docker-compose up -d db redis
   ```

4. **Set up the environment**:
   ```bash
   conda create -n sharedsaver python=3.11 -y
   conda activate sharedsaver
   pip install -r requirements.txt
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Option 2: Local PostgreSQL Setup

1. **Install PostgreSQL locally**:
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. **Create the database**:
   ```bash
   createdb sharedsaver_db
   ```

3. **Set up the environment**:
   ```bash
   conda create -n sharedsaver python=3.11 -y
   conda activate sharedsaver
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Frontend Setup** (Optional):
   ```bash
   # Install frontend dependencies
   cd frontend
   npm install

   # Start frontend development server
   npm start
   ```

8. **Full Stack Development**:
   ```bash
   # Run both backend and frontend simultaneously
   npm run dev

   # Or run them separately
   npm run backend  # Django server on http://127.0.0.1:8000
   npm run frontend # React server on http://localhost:3000
   ```

## API Endpoints

- `/api/users/` - User management
- `/api/accounts/` - Shared accounts
- `/api/transactions/` - Transactions
- `/api/loans/` - Loans

## Team Development

### For New Team Members
1. **Quick Setup**: Run `./scripts/setup_dev.sh` for automatic environment setup
2. **Read the Guide**: Check `docs/TEAM_GUIDE.md` for detailed team workflow
3. **Contributing**: See `CONTRIBUTING.md` for contribution guidelines

### Development Workflow
- **Branch Strategy**: `main` → `develop` → `feature/feature-name`
- **Code Quality**: Pre-commit hooks ensure consistent code style
- **Testing**: Write tests for all new features
- **Code Review**: All changes require team approval

### Code Quality Tools
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run code formatting
black .
isort .

# Run tests
python manage.py test
```

## Development

This project uses Django for the backend API. The backend provides RESTful endpoints for managing shared accounts, users, transactions, and loans.

## Docker Commands

```bash
# Start all services
docker-compose up -d

# Start only database and Redis
docker-compose up -d db redis

# View logs
docker-compose logs

# Stop services
docker-compose down

# Rebuild containers
docker-compose build
```

## License

MIT License
