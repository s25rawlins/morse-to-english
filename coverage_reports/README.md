# Test Coverage Reports

## Backend Coverage
- Open `backend_coverage/index.html` in a browser to view Python test coverage
- Target: 100% coverage for all Python modules

## Frontend Coverage
- Open `frontend_coverage/lcov-report/index.html` in a browser to view React test coverage
- Target: 100% coverage for all React components and services

## Running Tests

### Backend Tests
```bash
source venv/bin/activate
nox -s tests
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
```

### All Tests
```bash
./run_all_tests.sh
```
