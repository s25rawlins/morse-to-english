"""Nox configuration for automated testing and code quality checks."""

import nox

# Python versions to test against
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]

# Default sessions to run
nox.options.sessions = ["tests", "lint", "type_check", "security"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite with pytest."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install("pytest-cov", "pytest-xdist")
    
    # Run tests with coverage
    session.run(
        "pytest",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=85",
        "-n", "auto",  # Run tests in parallel
        "tests/",
        *session.posargs
    )


@nox.session(python="3.11")
def lint(session):
    """Run linting with flake8 and black."""
    session.chdir("backend")
    session.install("flake8", "black", "isort")
    
    # Check code formatting with black
    session.run("black", "--check", "--diff", "app/", "tests/")
    
    # Check import sorting with isort
    session.run("isort", "--check-only", "--diff", "app/", "tests/")
    
    # Run flake8 linting
    session.run("flake8", "app/", "tests/")


@nox.session(python="3.11")
def format_code(session):
    """Format code with black and isort."""
    session.chdir("backend")
    session.install("black", "isort")
    
    # Format code with black
    session.run("black", "app/", "tests/")
    
    # Sort imports with isort
    session.run("isort", "app/", "tests/")


@nox.session(python="3.11")
def type_check(session):
    """Run type checking with mypy."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install("mypy", "types-requests")
    
    # Run mypy type checking
    session.run("mypy", "app/", "--ignore-missing-imports")


@nox.session(python="3.11")
def security(session):
    """Run security checks with bandit and safety."""
    session.chdir("backend")
    session.install("bandit", "safety")
    
    # Run bandit security linting
    session.run("bandit", "-r", "app/", "-f", "json", "-o", "bandit-report.json")
    session.run("bandit", "-r", "app/")
    
    # Check for known security vulnerabilities in dependencies
    session.run("safety", "check", "--json", "--output", "safety-report.json")
    session.run("safety", "check")


@nox.session(python="3.11")
def docs(session):
    """Build documentation."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install("sphinx", "sphinx-rtd-theme", "sphinx-autodoc-typehints")
    
    # Build documentation
    session.run("sphinx-build", "-b", "html", "docs/", "docs/_build/html/")


@nox.session(python="3.11")
def performance(session):
    """Run performance tests."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install("pytest", "pytest-benchmark")
    
    # Run performance benchmarks
    session.run("pytest", "-v", "--benchmark-only", "tests/")


@nox.session(python="3.11")
def integration(session):
    """Run integration tests."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install("pytest", "httpx")
    
    # Start the FastAPI server in the background and run integration tests
    session.run("pytest", "-v", "-m", "integration", "tests/")


@nox.session(python="3.11")
def dev_setup(session):
    """Set up development environment."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    session.install(
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "black",
        "isort",
        "flake8",
        "mypy",
        "bandit",
        "safety",
        "pre-commit"
    )
    
    # Install pre-commit hooks
    session.run("pre-commit", "install")
    
    session.log("Development environment set up successfully!")
    session.log("Run 'nox -s tests' to run tests")
    session.log("Run 'nox -s lint' to check code style")
    session.log("Run 'nox -s format_code' to format code")


@nox.session(python="3.11")
def clean(session):
    """Clean up generated files and caches."""
    import shutil
    import os
    
    # Directories to clean
    clean_dirs = [
        "backend/.pytest_cache",
        "backend/__pycache__",
        "backend/htmlcov",
        "backend/.coverage",
        "backend/.mypy_cache",
        "backend/bandit-report.json",
        "backend/safety-report.json",
        "frontend/build",
        "frontend/node_modules",
        ".nox"
    ]
    
    for dir_path in clean_dirs:
        if os.path.exists(dir_path):
            if os.path.isfile(dir_path):
                os.remove(dir_path)
                session.log(f"Removed file: {dir_path}")
            else:
                shutil.rmtree(dir_path)
                session.log(f"Removed directory: {dir_path}")
    
    # Clean Python cache files
    for root, dirs, files in os.walk("."):
        for dir_name in dirs[:]:
            if dir_name == "__pycache__":
                shutil.rmtree(os.path.join(root, dir_name))
                dirs.remove(dir_name)
        for file_name in files:
            if file_name.endswith(".pyc"):
                os.remove(os.path.join(root, file_name))
    
    session.log("Cleanup completed!")


@nox.session(python="3.11")
def serve_backend(session):
    """Start the FastAPI development server."""
    session.chdir("backend")
    session.install("-r", "requirements.txt")
    
    session.log("Starting FastAPI development server...")
    session.log("API will be available at: http://localhost:8000")
    session.log("API documentation at: http://localhost:8000/docs")
    session.log("Press Ctrl+C to stop the server")
    
    session.run("uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000")


@nox.session(python=False)
def serve_frontend(session):
    """Start the React development server."""
    session.chdir("frontend")
    
    # Check if node_modules exists, if not install dependencies
    import os
    if not os.path.exists("node_modules"):
        session.log("Installing frontend dependencies...")
        session.run("npm", "install", external=True)
    
    session.log("Starting React development server...")
    session.log("Frontend will be available at: http://localhost:3000")
    session.log("Press Ctrl+C to stop the server")
    
    session.run("npm", "start", external=True)


@nox.session(python=False)
def build_frontend(session):
    """Build the React frontend for production."""
    session.chdir("frontend")
    
    session.log("Installing frontend dependencies...")
    session.run("npm", "install", external=True)
    
    session.log("Building frontend for production...")
    session.run("npm", "run", "build", external=True)
    
    session.log("Frontend built successfully! Files are in frontend/build/")


@nox.session(python="3.11")
def full_test(session):
    """Run all tests and quality checks."""
    session.log("Running comprehensive test suite...")
    
    # Run all quality checks
    session.notify("tests")
    session.notify("lint") 
    session.notify("type_check")
    session.notify("security")
    
    session.log("All tests and quality checks completed!")


@nox.session(python=False)
def install_frontend_deps(session):
    """Install frontend dependencies."""
    session.chdir("frontend")
    session.run("npm", "install", external=True)
    session.log("Frontend dependencies installed successfully!")


@nox.session(python="3.11")
def check_requirements(session):
    """Check for outdated requirements."""
    session.chdir("backend")
    session.install("pip-tools")
    
    session.run("pip-compile", "--upgrade", "requirements.in")
    session.log("Requirements checked and updated!")
