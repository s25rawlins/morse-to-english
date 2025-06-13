import React from 'react';
import MorseTranslator from './components/MorseTranslator';
import Header from './components/Header';
import MorseReference from './components/MorseReference';
import { ToastContainer } from './components/Toast';
import './styles/App.css';

function App() {
  return (
    <div className="app">
      <div className="container">
        <Header />
        <main className="main-content">
          <div className="translator-section">
            <MorseTranslator />
            <MorseReference />
          </div>
        </main>
        <footer className="footer">
          <div className="footer-content">
            <p>
              Built with React and FastAPI • Supports A-Z, 0-9, and punctuation • 
              Handles ambiguous Morse code patterns
            </p>
            <div className="footer-links">
              <a href="https://github.com" target="_blank" rel="noopener noreferrer">
                GitHub
              </a>
              <span>•</span>
              <a href="#" onClick={(e) => e.preventDefault()}>
                About
              </a>
              <span>•</span>
              <a href="#" onClick={(e) => e.preventDefault()}>
                Help
              </a>
            </div>
          </div>
        </footer>
      </div>
      <ToastContainer />
    </div>
  );
}

export default App;
