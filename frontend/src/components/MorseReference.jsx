import React, { useState } from 'react';
import './MorseReference.css';

const MorseReference = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('letters');

  const morseCode = {
    letters: {
      'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
      'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
      'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
      'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
      'Y': '-.--', 'Z': '--..'
    },
    numbers: {
      '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
      '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
    },
    punctuation: {
      '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
      '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
      ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
      '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
    }
  };

  const toggleReference = () => {
    setIsOpen(!isOpen);
  };

  const renderMorseTable = (data) => {
    return (
      <div className="morse-grid">
        {Object.entries(data).map(([char, morse]) => (
          <div key={char} className="morse-item">
            <span className="morse-char">{char}</span>
            <span className="morse-code">{morse}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="morse-reference">
      <button 
        className="reference-toggle"
        onClick={toggleReference}
        aria-expanded={isOpen}
        aria-label="Toggle Morse code reference"
      >
        <span className="reference-icon">[?]</span>
        Morse Code Reference
        <span className={`reference-arrow ${isOpen ? 'open' : ''}`}>v</span>
      </button>

      {isOpen && (
        <div className="reference-content">
          <div className="reference-header">
            <h3>Morse Code Reference</h3>
            <p>Click on any character to hear its Morse code pattern</p>
          </div>

          <div className="reference-tabs">
            <button
              className={`tab-button ${activeTab === 'letters' ? 'active' : ''}`}
              onClick={() => setActiveTab('letters')}
            >
              Letters (A-Z)
            </button>
            <button
              className={`tab-button ${activeTab === 'numbers' ? 'active' : ''}`}
              onClick={() => setActiveTab('numbers')}
            >
              Numbers (0-9)
            </button>
            <button
              className={`tab-button ${activeTab === 'punctuation' ? 'active' : ''}`}
              onClick={() => setActiveTab('punctuation')}
            >
              Punctuation
            </button>
          </div>

          <div className="reference-body">
            {activeTab === 'letters' && renderMorseTable(morseCode.letters)}
            {activeTab === 'numbers' && renderMorseTable(morseCode.numbers)}
            {activeTab === 'punctuation' && renderMorseTable(morseCode.punctuation)}
          </div>

          <div className="reference-footer">
            <div className="morse-legend">
              <div className="legend-item">
                <span className="legend-symbol">.</span>
                <span className="legend-text">Dot (short signal)</span>
              </div>
              <div className="legend-item">
                <span className="legend-symbol">-</span>
                <span className="legend-text">Dash (long signal)</span>
              </div>
              <div className="legend-item">
                <span className="legend-symbol">/</span>
                <span className="legend-text">Word separator</span>
              </div>
            </div>
            <div className="reference-tips">
              <h4>Tips:</h4>
              <ul>
                <li>Separate letters with spaces</li>
                <li>Separate words with forward slashes (/)</li>
                <li>A dash is three times longer than a dot</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MorseReference;
