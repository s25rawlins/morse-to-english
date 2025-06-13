import React, { useState, useCallback, useEffect, useRef } from 'react';
import { translateEnglishToMorse, translateMorseToEnglish } from '../services/api';
import TranslationInput from './TranslationInput';
import TranslationOutput from './TranslationOutput';
import LoadingSpinner from './LoadingSpinner';

const MorseTranslator = () => {
  const [mode, setMode] = useState('english-to-morse');
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Use useRef for debounce timer to avoid unnecessary re-renders
  const debounceTimerRef = useRef(null);

  const clearMessages = useCallback(() => {
    setError('');
    setSuccess('');
  }, []);

  const handleTranslate = useCallback(async (inputText = input) => {
    if (!inputText.trim()) {
      setOutput('');
      clearMessages();
      return;
    }

    setIsLoading(true);
    clearMessages();

    try {
      let result;
      
      if (mode === 'english-to-morse') {
        result = await translateEnglishToMorse(inputText);
        setOutput(result.output);
      } else {
        result = await translateMorseToEnglish(inputText);
        
        // Handle multiple results
        if (Array.isArray(result.output)) {
          setOutput(result.output);
          if (result.output.length > 1) {
            setSuccess(`Found ${result.output.length} possible interpretations`);
          }
        } else {
          setOutput([result.output]);
        }
      }
    } catch (err) {
      setError(err.message || 'Translation failed');
      setOutput('');
    } finally {
      setIsLoading(false);
    }
  }, [input, mode, clearMessages]);

  // Auto-translate with debouncing - optimized to prevent re-renders
  useEffect(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    if (input.trim()) {
      const timer = setTimeout(async () => {
        if (!input.trim()) return;

        // Batch state updates to minimize re-renders
        try {
          let result;
          
          if (mode === 'english-to-morse') {
            result = await translateEnglishToMorse(input);
            // Use functional updates to avoid dependency issues
            setOutput(result.output);
            setError('');
            setSuccess('');
          } else {
            result = await translateMorseToEnglish(input);
            
            // Handle multiple results
            if (Array.isArray(result.output)) {
              setOutput(result.output);
              setError('');
              if (result.output.length > 1) {
                setSuccess(`Found ${result.output.length} possible interpretations`);
              } else {
                setSuccess('');
              }
            } else {
              setOutput([result.output]);
              setError('');
              setSuccess('');
            }
          }
        } catch (err) {
          setError(err.message || 'Translation failed');
          setOutput('');
          setSuccess('');
        }
      }, 500); // 500ms debounce

      debounceTimerRef.current = timer;
    } else {
      setOutput('');
      setError('');
      setSuccess('');
    }

    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [input, mode]); // Minimal dependencies

  const handleModeChange = (newMode) => {
    setMode(newMode);
    setInput('');
    setOutput('');
    clearMessages();
  };

  const handleInputChange = (value) => {
    setInput(value);
  };

  const handleClear = () => {
    setInput('');
    setOutput('');
    clearMessages();
  };

  const handleSwap = () => {
    if (typeof output === 'string' && output.trim()) {
      const newMode = mode === 'english-to-morse' ? 'morse-to-english' : 'english-to-morse';
      setMode(newMode);
      setInput(output);
      setOutput('');
      clearMessages();
    }
  };

  const getPlaceholderText = () => {
    if (mode === 'english-to-morse') {
      return 'Enter English text here... (e.g., "HELLO WORLD")';
    } else {
      return 'Enter Morse code here... (e.g., ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")';
    }
  };

  const getInputLabel = () => {
    return mode === 'english-to-morse' ? 'English Text' : 'Morse Code';
  };

  const getOutputLabel = () => {
    return mode === 'english-to-morse' ? 'Morse Code' : 'English Text';
  };

  const getInputHint = () => {
    if (mode === 'english-to-morse') {
      return 'Supports letters A-Z, numbers 0-9, and spaces';
    } else {
      return 'Use dots (.), dashes (-), spaces between letters, and / for word breaks';
    }
  };

  return (
    <div className="translator-card">
      {/* Mode Toggle */}
      <div className="mode-toggle">
        <button
          className={`mode-button ${mode === 'english-to-morse' ? 'active' : ''}`}
          onClick={() => handleModeChange('english-to-morse')}
          disabled={isLoading}
        >
          English → Morse
        </button>
        <button
          className={`mode-button ${mode === 'morse-to-english' ? 'active' : ''}`}
          onClick={() => handleModeChange('morse-to-english')}
          disabled={isLoading}
        >
          Morse → English
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="message message-error">
          {error}
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="message message-success">
          {success}
        </div>
      )}

      {/* Input Section */}
      <TranslationInput
        value={input}
        onChange={handleInputChange}
        placeholder={getPlaceholderText()}
        label={getInputLabel()}
        hint={getInputHint()}
        disabled={isLoading}
      />

      {/* Action Buttons */}
      <div className="action-buttons">
        <button
          className="btn btn-primary"
          onClick={() => handleTranslate()}
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? (
            <>
              <LoadingSpinner size="small" color="white" />
              Translating...
            </>
          ) : (
            'Translate'
          )}
        </button>
        
        <button
          className="btn btn-secondary"
          onClick={handleSwap}
          disabled={!output || Array.isArray(output) || isLoading}
          title="Swap input and output"
        >
          Swap
        </button>
        
        <button
          className="btn btn-secondary"
          onClick={handleClear}
          disabled={!input && !output}
        >
          Clear
        </button>
      </div>

      {/* Output Section */}
      <TranslationOutput
        output={output}
        label={getOutputLabel()}
        mode={mode}
      />
    </div>
  );
};

export default MorseTranslator;
