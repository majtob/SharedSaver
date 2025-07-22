#!/bin/bash

# SharedSaver Development Setup Script
# This script helps team members set up the development environment

set -e  # Exit on any error

echo "🚀 Setting up SharedSaver development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    print_error "Conda is not installed. Please install Anaconda or Miniconda first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL is not installed. Installing via Homebrew..."
    brew install postgresql
    brew services start postgresql
fi

# Create conda environment
print_status "Creating conda environment..."
if conda env list | grep -q "sharedsaver"; then
    print_warning "Conda environment 'sharedsaver' already exists. Skipping creation."
else
    conda create -n sharedsaver python=3.11 -y
fi

# Activate conda environment
print_status "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate sharedsaver

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Check if database exists
print_status "Checking database..."
if psql -lqt | cut -d \| -f 1 | grep -qw sharedsaver_db; then
    print_warning "Database 'sharedsaver_db' already exists. Skipping creation."
else
    print_status "Creating database..."
    createdb sharedsaver_db
fi

# Run Django migrations
print_status "Running Django migrations..."
python manage.py migrate

# Check if superuser exists
print_status "Checking for superuser..."
if python manage.py shell -c "from users.models import User; print('Superuser exists' if User.objects.filter(is_superuser=True).exists() else 'No superuser')" 2>/dev/null | grep -q "Superuser exists"; then
    print_warning "Superuser already exists. Skipping creation."
else
    print_status "Creating superuser..."
    echo "Please create a superuser account:"
    python manage.py createsuperuser
fi

# Create media directories
print_status "Creating media directories..."
mkdir -p media/profile_pictures
mkdir -p staticfiles

# Set up pre-commit hooks (optional)
if command -v pre-commit &> /dev/null; then
    print_status "Setting up pre-commit hooks..."
    pre-commit install
else
    print_warning "pre-commit not installed. Install with: pip install pre-commit"
fi

print_status "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: conda activate sharedsaver"
echo "2. Start the development server: python manage.py runserver"
echo "3. Access the admin interface: http://127.0.0.1:8000/admin/"
echo "4. Start coding! 🎉"
echo ""
echo "For Docker setup, run: docker-compose up -d db redis" 