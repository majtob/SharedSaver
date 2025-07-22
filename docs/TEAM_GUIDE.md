# SharedSaver Team Development Guide

Welcome to the SharedSaver team! This guide will help you get started and understand our development process.

## 🚀 Quick Start for New Team Members

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd SharedSaver

# Run the setup script (recommended)
./scripts/setup_dev.sh

# Or set up manually:
conda create -n sharedsaver python=3.11 -y
conda activate sharedsaver
pip install -r requirements.txt
createdb sharedsaver_db
python manage.py migrate
python manage.py createsuperuser
```

### 2. Start Development
```bash
conda activate sharedsaver
python manage.py runserver
```

## 📋 Project Overview

### What We're Building
SharedSaver is a fintech application that enables:
- **Shared Saving Accounts**: Families and friends can pool money together
- **Interest-Free Loans**: Members can borrow from the shared pool
- **Transparent Transactions**: All activities are tracked and visible
- **Role-Based Access**: Different permission levels for members

### Tech Stack
- **Backend**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: React (coming soon)
- **Authentication**: JWT tokens
- **Deployment**: Docker

## 🏗️ Architecture

### Django Apps
1. **users** - User management and profiles
2. **accounts** - Shared account management
3. **transactions** - Financial transaction tracking
4. **loans** - Loan management and approval workflow

### Key Models
- `User` - Extended user model with financial profile
- `SharedAccount` - Shared saving accounts
- `AccountMembership` - User-account relationships with roles
- `Transaction` - All financial transactions
- `Loan` - Interest-free loans

## 🔄 Development Workflow

### Git Branch Strategy
```
main (production)
├── develop (integration)
    ├── feature/user-authentication
    ├── feature/shared-accounts
    ├── feature/loan-management
    └── hotfix/critical-bug
```

### Daily Workflow
1. **Start of day**: `git pull origin develop`
2. **Create feature branch**: `git checkout -b feature/your-feature`
3. **Make changes**: Code, test, commit
4. **Push and create PR**: `git push origin feature/your-feature`
5. **Code review**: Get approval from team
6. **Merge**: Merge to develop branch

### Commit Message Format
```
type(scope): description

feat(users): add email verification
fix(accounts): resolve balance calculation bug
docs(readme): update installation instructions
test(loans): add unit tests for loan approval
```

## 🧪 Testing Strategy

### Running Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test users

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Guidelines
- Write tests for all new features
- Test both success and failure cases
- Use factories for test data
- Mock external services

## 📚 API Development

### Current Endpoints
- `/api/users/` - User management
- `/api/accounts/` - Shared accounts
- `/api/transactions/` - Transactions
- `/api/loans/` - Loans

### Adding New Endpoints
1. Create serializers in `app/serializers.py`
2. Create views in `app/views.py`
3. Add URLs in `app/urls.py`
4. Write tests
5. Update documentation

### API Standards
- Use consistent naming conventions
- Include proper error handling
- Add pagination for list endpoints
- Use proper HTTP status codes

## 🔐 Security Guidelines

### Authentication & Authorization
- Use JWT tokens for API authentication
- Implement role-based permissions
- Validate all user inputs
- Never expose sensitive data in responses

### Data Protection
- Use environment variables for secrets
- Encrypt sensitive data at rest
- Implement proper session management
- Regular security audits

## 🐳 Docker Development

### Using Docker
```bash
# Start services
docker-compose up -d db redis

# Build and run application
docker-compose up web

# View logs
docker-compose logs -f
```

### Docker Benefits
- Consistent environment across team
- Easy PostgreSQL and Redis setup
- Production-like environment
- Simplified deployment

## 📝 Documentation

### What to Document
- API endpoints and usage
- Database schema changes
- Configuration options
- Deployment procedures
- Troubleshooting guides

### Documentation Standards
- Keep docs up to date
- Include code examples
- Add screenshots for UI changes
- Document breaking changes

## 🤝 Team Communication

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code reviews and discussions
- **Team Chat**: Quick questions and coordination
- **Weekly Standups**: Progress updates

### Code Review Process
1. **Self-review**: Test your changes locally
2. **Create PR**: Include clear description
3. **Team review**: At least one approval required
4. **Address feedback**: Make requested changes
5. **Merge**: After approval

### Review Guidelines
- Be constructive and respectful
- Test changes before approving
- Check for security issues
- Ensure code follows standards

## 🚀 Deployment

### Environment Setup
```bash
# Production environment variables
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=sharedsaver_prod
DB_USER=prod_user
DB_PASSWORD=secure_password
```

### Deployment Process
1. **Staging**: Test on staging environment
2. **Code review**: Final review before production
3. **Deploy**: Use Docker or cloud platform
4. **Monitor**: Check logs and performance
5. **Rollback**: Plan for quick rollback if needed

## 🐛 Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check PostgreSQL status
brew services list | grep postgresql

# Restart PostgreSQL
brew services restart postgresql

# Check database exists
psql -l | grep sharedsaver_db
```

#### Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial

# Show migration status
python manage.py showmigrations
```

#### Environment Issues
```bash
# Recreate conda environment
conda deactivate
conda env remove -n sharedsaver
conda create -n sharedsaver python=3.11 -y
conda activate sharedsaver
pip install -r requirements.txt
```

## 📈 Performance & Monitoring

### Performance Guidelines
- Optimize database queries
- Use caching where appropriate
- Monitor response times
- Profile memory usage

### Monitoring Tools
- Django Debug Toolbar (development)
- Database query logging
- Application performance monitoring
- Error tracking and alerting

## 🎯 Next Steps

### Immediate Tasks
1. Set up your development environment
2. Explore the codebase
3. Run the test suite
4. Create your first feature branch

### Learning Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

### Questions?
- Check the documentation first
- Search existing issues
- Ask in team chat
- Create an issue with "question" label

Welcome to the team! Let's build something amazing together! 🚀 