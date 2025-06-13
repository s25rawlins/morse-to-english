"""
Pydantic models for request and response validation.
"""

from typing import List, Union
from pydantic import BaseModel, Field, validator


class EnglishToMorseRequest(BaseModel):
    """Request model for English to Morse code translation."""
    
    text: str = Field(
        ..., 
        min_length=1,
        max_length=1000,
        description="English text to convert to Morse code"
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()


class MorseToEnglishRequest(BaseModel):
    """Request model for Morse code to English translation."""
    
    morse_code: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Morse code to convert to English"
    )
    
    @validator('morse_code')
    def validate_morse_code(cls, v):
        if not v.strip():
            raise ValueError('Morse code cannot be empty or only whitespace')
        
        # Validate that only valid morse characters are used
        valid_chars = set('.- /')
        if not all(char in valid_chars for char in v.strip()):
            raise ValueError(
                'Invalid characters in Morse code. '
                'Only dots (.), dashes (-), spaces, and slashes (/) are allowed.'
            )
        
        return v.strip()


class TranslationResponse(BaseModel):
    """Response model for translation results."""
    
    input: str = Field(..., description="Original input text")
    output: Union[str, List[str]] = Field(
        ..., 
        description="Translation result(s)"
    )
    translation_type: str = Field(
        ..., 
        description="Type of translation performed"
    )
    character_count: int = Field(
        ..., 
        description="Number of characters in input"
    )
    success: bool = Field(
        default=True, 
        description="Whether translation was successful"
    )


class ErrorResponse(BaseModel):
    """Response model for error cases."""
    
    error: str = Field(..., description="Error message")
    detail: str = Field(None, description="Detailed error information")
    success: bool = Field(default=False, description="Always false for errors")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(default="healthy", description="Service status")
    version: str = Field(default="1.0.0", description="API version")
    supported_characters: List[str] = Field(
        ..., 
        description="List of characters supported for translation"
    )
