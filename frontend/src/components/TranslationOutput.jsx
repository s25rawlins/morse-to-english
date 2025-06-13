import React, { useState } from 'react';

const TranslationOutput = ({ output, label, mode }) => {
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopy = async (text, index = null) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      
      // Reset the copied state after 2 seconds
      setTimeout(() => {
        setCopiedIndex(null);
      }, 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
      
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        setCopiedIndex(index);
        setTimeout(() => {
          setCopiedIndex(null);
        }, 2000);
      } catch (fallbackErr) {
        console.error('Fallback copy failed:', fallbackErr);
      }
      document.body.removeChild(textArea);
    }
  };

  const renderSingleResult = (result) => {
    const isEmpty = !result || result.trim() === '';
    
    return (
      <div className="output-section">
        <div className="output-label">
          <h3>{label}</h3>
          {!isEmpty && (
            <button
              className={`copy-button ${copiedIndex === 'single' ? 'copied' : ''}`}
              onClick={() => handleCopy(result, 'single')}
              title="Copy to clipboard"
            >
              {copiedIndex === 'single' ? '✓ Copied!' : '📋 Copy'}
            </button>
          )}
        </div>
        
        <div className={`output-content ${isEmpty ? 'empty' : ''}`}>
          {isEmpty ? 'Translation will appear here...' : result}
        </div>
      </div>
    );
  };

  const renderMultipleResults = (results) => {
    const validResults = results.filter(result => result && result.trim() !== '');
    
    if (validResults.length === 0) {
      return renderSingleResult('');
    }

    if (validResults.length === 1) {
      return renderSingleResult(validResults[0]);
    }

    return (
      <div className="output-section">
        <div className="output-label">
          <h3>{label} ({validResults.length} interpretations)</h3>
        </div>
        
        <div className="output-content">
          <div className="multiple-results">
            {validResults.map((result, index) => (
              <div 
                key={index} 
                className="result-item" 
                data-index={index + 1}
              >
                <div style={{ paddingRight: '60px' }}>
                  {result}
                </div>
                <button
                  className={`copy-button ${copiedIndex === index ? 'copied' : ''}`}
                  onClick={() => handleCopy(result, index)}
                  title="Copy this interpretation"
                  style={{
                    position: 'absolute',
                    right: '8px',
                    top: '50%',
                    transform: 'translateY(-50%)'
                  }}
                >
                  {copiedIndex === index ? '✓' : '📋'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Handle empty output
  if (!output) {
    return renderSingleResult('');
  }

  // Handle array output (multiple interpretations)
  if (Array.isArray(output)) {
    return renderMultipleResults(output);
  }

  // Handle single string output
  return renderSingleResult(output);
};

export default TranslationOutput;
