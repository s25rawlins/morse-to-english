"""
API routes for the Morse Code Translator service.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..core.morse_translator import MorseTranslator
from ..models.schemas import (
    EnglishToMorseRequest,
    MorseToEnglishRequest,
    TranslationResponse,
    ErrorResponse,
    HealthResponse
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        supported_characters=MorseTranslator.get_supported_characters()
    )


@router.post("/translate/english-to-morse", response_model=TranslationResponse)
async def translate_english_to_morse(request: EnglishToMorseRequest):
    """Convert English text to Morse code."""
    try:
        morse_result = MorseTranslator.english_to_morse(request.text)
        
        if not morse_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No translatable characters found in input text"
            )
        
        return TranslationResponse(
            input=request.text,
            output=morse_result,
            translation_type="english_to_morse",
            character_count=len(request.text),
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.post("/translate/morse-to-english", response_model=TranslationResponse)
async def translate_morse_to_english(request: MorseToEnglishRequest):
    """Convert Morse code to English text."""
    try:
        # Validate morse code format
        if not MorseTranslator.validate_morse_code(request.morse_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Morse code format. Use only dots (.), dashes (-), spaces, and slashes (/)."
            )
        
        english_results = MorseTranslator.morse_to_english(request.morse_code)
        
        if not english_results or (len(english_results) == 1 and not english_results[0]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid English translations found for the provided Morse code"
            )
        
        # Remove empty results and duplicates while preserving order
        filtered_results = []
        seen = set()
        for result in english_results:
            if result and result not in seen:
                filtered_results.append(result)
                seen.add(result)
        
        if not filtered_results:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid English translations found for the provided Morse code"
            )
        
        # Return single string if only one result, otherwise return list
        output = filtered_results[0] if len(filtered_results) == 1 else filtered_results
        
        return TranslationResponse(
            input=request.morse_code,
            output=output,
            translation_type="morse_to_english",
            character_count=len(request.morse_code),
            success=True
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.get("/supported-characters")
async def get_supported_characters():
    """Get supported characters for translation."""
    return {
        "supported_characters": MorseTranslator.get_supported_characters(),
        "total_count": len(MorseTranslator.get_supported_characters())
    }
