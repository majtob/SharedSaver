# Contributing to SharedSaver

Thank you for your interest in contributing to SharedSaver! This document provides guidelines for team collaboration.

## Getting Started

### Prerequisites
- Python 3.11+
- Conda (recommended) or pip
- PostgreSQL
- Git

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SharedSaver
   ```

2. **Set up the environment:**
   ```bash
   # Create conda environment
   conda create -n sharedsaver python=3.11 -y
   conda activate sharedsaver
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   ```bash
   # Option 1: Local PostgreSQL
   brew install postgresql
   brew services start postgresql
   createdb sharedsaver_db
   
   # Option 2: Docker (recommended for consistency)
   docker-compose up -d db redis
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## Development Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/feature-name` - Feature branches
- `hotfix/hotfix-name` - Critical bug fixes

### Git Workflow
1. Create a feature branch from `develop`
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add docstrings to functions and classes
- Write unit tests for new features

### Database Changes
- Always create migrations for model changes
- Test migrations on a copy of production data
- Document breaking changes

## Project Structure

```
SharedSaver/
├── sharedsaver/          # Main Django project
├── users/                # User management
├── accounts/             # Shared accounts
├── transactions/         # Transactions
├── loans/                # Loans
├── frontend/             # React frontend (coming soon)
├── tests/                # Test files
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
- Test models, views, and API endpoints
- Use factories for test data
- Mock external services
- Test both success and failure cases

## API Documentation

### Endpoints
- `/api/users/` - User management
- `/api/accounts/` - Shared accounts
- `/api/transactions/` - Transactions
- `/api/loans/` - Loans

### Authentication
- JWT tokens for API authentication
- Session authentication for admin interface

## Deployment

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=sharedsaver_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

### Docker Deployment
```bash
docker-compose up -d
```

## Communication

### Team Channels
- Use project issues for bug reports
- Create feature requests with detailed descriptions
- Discuss architecture changes in pull requests

### Code Reviews
- All code must be reviewed before merging
- Provide constructive feedback
- Test the changes locally before approving

## Security

### Best Practices
- Never commit sensitive data
- Use environment variables for secrets
- Validate all user inputs
- Implement proper authentication and authorization

### Reporting Security Issues
- Report security vulnerabilities privately
- Include detailed reproduction steps
- Provide suggested fixes if possible

## Questions?

If you have questions about contributing, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with the "question" label

Thank you for contributing to SharedSaver! 🚀 