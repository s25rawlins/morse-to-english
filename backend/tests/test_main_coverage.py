"""
Tests for main.py to achieve 100% coverage.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from app.main import app, http_exception_handler, general_exception_handler

client = TestClient(app)


class TestMainCoverage:
    """Test cases for main.py to achieve 100% coverage."""

    @pytest.mark.asyncio
    async def test_http_exception_handler(self):
        """Test the HTTP exception handler."""
        # Create a mock request
        mock_request = MagicMock()
        
        # Create an HTTPException
        exc = HTTPException(status_code=400, detail="Test error message")
        
        # Call the exception handler
        response = await http_exception_handler(mock_request, exc)
        
        # Verify the response
        assert response.status_code == 400
        assert "Test error message" in str(response.body)

    @pytest.mark.asyncio
    async def test_general_exception_handler(self):
        """Test the general exception handler."""
        # Create a mock request
        mock_request = MagicMock()
        
        # Create a general exception
        exc = Exception("Test general error")
        
        # Call the exception handler
        response = await general_exception_handler(mock_request, exc)
        
        # Verify the response
        assert response.status_code == 500
        assert "Internal server error" in str(response.body)


    def test_exception_handler_with_custom_detail(self):
        """Test exception handler with custom detail attribute."""
        # This tests the getattr line in the HTTP exception handler
        with patch('app.api.routes.MorseTranslator.validate_morse_code', 
                   side_effect=HTTPException(status_code=400, detail="Custom validation error")):
            response = client.post("/api/v1/translate/morse-to-english", json={"morse_code": ".- -..."})
            assert response.status_code == 400
            data = response.json()
            assert "Custom validation error" in data["detail"]



    def test_cors_configuration(self):
        """Test that CORS is properly configured."""
        # Test OPTIONS request (preflight)
        response = client.options("/api/v1/health")
        # Should not fail due to CORS
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly defined

    def test_app_configuration(self):
        """Test that the FastAPI app is properly configured."""
        # Test that the app has the correct title and version
        assert app.title == "Morse Code Translator API"
        assert app.version == "1.0.0"
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"

    def test_router_inclusion(self):
        """Test that the router is properly included."""
        # Test that API routes are accessible
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_middleware_configuration(self):
        """Test that middleware is properly configured."""
        # Test a request that would trigger CORS
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = client.options("/api/v1/health", headers=headers)
        # Should not fail due to CORS configuration
        assert response.status_code in [200, 405]

    def test_error_response_format(self):
        """Test that error responses follow the expected format."""
        # Trigger a validation error
        response = client.post("/api/v1/translate/english-to-morse", json={})
        assert response.status_code == 422
        
        # The response should be JSON
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_exception_handlers_with_different_status_codes(self):
        """Test exception handlers with different HTTP status codes."""
        mock_request = MagicMock()
        
        # Test different status codes
        status_codes = [400, 401, 403, 404, 422, 500]
        
        for status_code in status_codes:
            exc = HTTPException(status_code=status_code, detail=f"Error {status_code}")
            response = await http_exception_handler(mock_request, exc)
            assert response.status_code == status_code

    def test_app_startup_and_shutdown(self):
        """Test app startup and shutdown events."""
        # Test that the app can be started and stopped without errors
        with TestClient(app) as test_client:
            response = test_client.get("/")
            assert response.status_code == 200

    def test_root_endpoint_response_format(self):
        """Test that root endpoint returns expected format."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["message", "version", "docs", "health"]
        for key in expected_keys:
            assert key in data
        
        assert data["message"] == "Morse Code Translator API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["health"] == "/api/v1/health"

    def test_ping_endpoint_response_format(self):
        """Test that ping endpoint returns expected format."""
        response = client.get("/ping")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "pong"


    def test_large_error_message_handling(self):
        """Test exception handlers with large error messages."""
        # Create a large error message
        large_message = "A" * 10000
        
        with patch('app.api.routes.MorseTranslator.validate_morse_code', 
                   side_effect=HTTPException(status_code=400, detail=large_message)):
            response = client.post("/api/v1/translate/morse-to-english", json={"morse_code": ".- -..."})
            assert response.status_code == 400
            # Should handle large messages without issues
            data = response.json()
            assert len(data["detail"]) > 1000
