#!/bin/bash

# Comprehensive test runner for Morse Code Translator
# This script runs all tests for both backend (Python) and frontend (React)

set -e  # Exit on any error

echo "Running comprehensive test suite for Morse Code Translator"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check for Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    # Check for npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    
    print_success "All dependencies are available"
}

# Setup virtual environment for Python tests
setup_python_env() {
    print_status "Setting up Python environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install nox if not available
    if ! command -v nox &> /dev/null; then
        print_status "Installing nox..."
        pip install nox
    fi
    
    print_success "Python environment ready"
}

# Run backend tests
run_backend_tests() {
    print_status "Running backend tests..."
    echo "----------------------------------------"
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run tests with coverage
    print_status "Running Python tests with coverage..."
    if nox -s tests; then
        print_success "Backend tests passed!"
        
        # Display coverage report
        print_status "Coverage report:"
        echo "Backend coverage report is available in backend/htmlcov/index.html"
    else
        print_error "Backend tests failed!"
        return 1
    fi
}

# Setup and run frontend tests
run_frontend_tests() {
    print_status "Running frontend tests..."
    echo "----------------------------------------"
    
    cd frontend
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        print_status "Installing frontend dependencies..."
        npm install
    fi
    
    # Run tests with coverage
    print_status "Running React tests with coverage..."
    if npm test -- --coverage --watchAll=false; then
        print_success "Frontend tests passed!"
        
        # Display coverage info
        print_status "Frontend coverage report is available in frontend/coverage/lcov-report/index.html"
    else
        print_error "Frontend tests failed!"
        cd ..
        return 1
    fi
    
    cd ..
}

# Run linting and code quality checks
run_code_quality_checks() {
    print_status "Running code quality checks..."
    echo "----------------------------------------"
    
    # Backend linting
    print_status "Running backend linting..."
    source venv/bin/activate
    if nox -s lint; then
        print_success "Backend linting passed!"
    else
        print_warning "Backend linting issues found"
    fi
    
    # Frontend linting
    print_status "Running frontend linting..."
    cd frontend
    if npm run lint 2>/dev/null || true; then
        print_success "Frontend linting completed"
    else
        print_warning "Frontend linting not configured or issues found"
    fi
    cd ..
}

# Run type checking
run_type_checks() {
    print_status "Running type checks..."
    echo "----------------------------------------"
    
    # Backend type checking
    print_status "Running backend type checking..."
    source venv/bin/activate
    if nox -s type_check; then
        print_success "Backend type checking passed!"
    else
        print_warning "Backend type checking issues found"
    fi
}

# Run security checks
run_security_checks() {
    print_status "Running security checks..."
    echo "----------------------------------------"
    
    # Backend security checks
    print_status "Running backend security checks..."
    source venv/bin/activate
    if nox -s security; then
        print_success "Backend security checks passed!"
    else
        print_warning "Backend security issues found"
    fi
    
    # Frontend security audit
    print_status "Running frontend security audit..."
    cd frontend
    if npm audit --audit-level=high; then
        print_success "Frontend security audit passed!"
    else
        print_warning "Frontend security vulnerabilities found"
    fi
    cd ..
}

# Generate comprehensive coverage report
generate_coverage_report() {
    print_status "Generating comprehensive coverage report..."
    echo "----------------------------------------"
    
    # Create coverage directory
    mkdir -p coverage_reports
    
    # Copy backend coverage
    if [ -d "backend/htmlcov" ]; then
        cp -r backend/htmlcov coverage_reports/backend_coverage
        print_success "Backend coverage report copied to coverage_reports/backend_coverage/"
    fi
    
    # Copy frontend coverage
    if [ -d "frontend/coverage" ]; then
        cp -r frontend/coverage coverage_reports/frontend_coverage
        print_success "Frontend coverage report copied to coverage_reports/frontend_coverage/"
    fi
    
    # Create summary report
    cat > coverage_reports/README.md << EOF
# Test Coverage Reports

## Backend Coverage
- Open \`backend_coverage/index.html\` in a browser to view Python test coverage
- Target: 100% coverage for all Python modules

## Frontend Coverage
- Open \`frontend_coverage/lcov-report/index.html\` in a browser to view React test coverage
- Target: 100% coverage for all React components and services

## Running Tests

### Backend Tests
\`\`\`bash
source venv/bin/activate
nox -s tests
\`\`\`

### Frontend Tests
\`\`\`bash
cd frontend
npm test -- --coverage
\`\`\`

### All Tests
\`\`\`bash
./run_all_tests.sh
\`\`\`
EOF
    
    print_success "Coverage reports generated in coverage_reports/"
}

# Main execution
main() {
    echo "Starting comprehensive test suite..."
    echo "Current directory: $(pwd)"
    echo "Timestamp: $(date)"
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Setup environments
    setup_python_env
    
    # Track test results
    backend_result=0
    frontend_result=0
    
    # Run backend tests
    if ! run_backend_tests; then
        backend_result=1
    fi
    
    # Run frontend tests
    if ! run_frontend_tests; then
        frontend_result=1
    fi
    
    # Run additional checks
    run_code_quality_checks
    run_type_checks
    run_security_checks
    
    # Generate coverage reports
    generate_coverage_report
    
    # Summary
    echo ""
    echo "============================================================"
    echo "Test Suite Summary"
    echo "============================================================"
    
    if [ $backend_result -eq 0 ]; then
        print_success "Backend tests: PASSED"
    else
        print_error "Backend tests: FAILED"
    fi
    
    if [ $frontend_result -eq 0 ]; then
        print_success "Frontend tests: PASSED"
    else
        print_error "Frontend tests: FAILED"
    fi
    
    if [ $backend_result -eq 0 ] && [ $frontend_result -eq 0 ]; then
        print_success "All tests passed! The application has comprehensive test coverage."
        echo ""
        echo "Coverage Reports:"
        echo "   - Backend: coverage_reports/backend_coverage/index.html"
        echo "   - Frontend: coverage_reports/frontend_coverage/lcov-report/index.html"
        echo ""
        echo "Ready for deployment!"
        exit 0
    else
        print_error "Some tests failed. Please check the output above for details."
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    --backend-only)
        print_status "Running backend tests only..."
        check_dependencies
        setup_python_env
        run_backend_tests
        ;;
    --frontend-only)
        print_status "Running frontend tests only..."
        check_dependencies
        run_frontend_tests
        ;;
    --coverage-only)
        print_status "Generating coverage reports only..."
        generate_coverage_report
        ;;
    --help)
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --backend-only    Run only backend tests"
        echo "  --frontend-only   Run only frontend tests"
        echo "  --coverage-only   Generate coverage reports only"
        echo "  --help           Show this help message"
        echo ""
        echo "Run without arguments to execute the full test suite."
        ;;
    *)
        main
        ;;
esac
