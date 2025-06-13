import React, { useRef, useEffect, useCallback, useMemo } from 'react';

const TranslationInput = ({ 
  value, 
  onChange, 
  placeholder, 
  label, 
  hint, 
  disabled = false 
}) => {
  const textareaRef = useRef(null);
  const cursorPositionRef = useRef(0);
  const wasFocusedRef = useRef(false);
  const isRestoringFocusRef = useRef(false);

  const handleFocus = useCallback(() => {
    wasFocusedRef.current = true;
    isRestoringFocusRef.current = false;
  }, []);

  const handleBlur = useCallback((e) => {
    if (!isRestoringFocusRef.current) {
      wasFocusedRef.current = false;
    }
  }, []);

  const handleChange = useCallback((e) => {
    const newCursorPosition = e.target.selectionStart;
    cursorPositionRef.current = newCursorPosition;
    onChange(e.target.value);
  }, [onChange]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea && wasFocusedRef.current && !disabled) {
      if (document.activeElement !== textarea) {
        isRestoringFocusRef.current = true;
        textarea.focus();
        textarea.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
      }

      const timeoutId = setTimeout(() => {
        if (textarea && wasFocusedRef.current && document.activeElement !== textarea) {
          isRestoringFocusRef.current = true;
          textarea.focus();
          textarea.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
        }
        isRestoringFocusRef.current = false;
      }, 0);

      const rafId = requestAnimationFrame(() => {
        if (textarea && wasFocusedRef.current && document.activeElement !== textarea) {
          isRestoringFocusRef.current = true;
          textarea.focus();
          textarea.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
        }
        isRestoringFocusRef.current = false;
      });

      return () => {
        clearTimeout(timeoutId);
        cancelAnimationFrame(rafId);
      };
    }
  });

  const characterCount = useMemo(() => value.length, [value.length]);
  const maxLength = 1000;

  return (
    <div className="input-section">
      <label className="input-label" htmlFor="translation-input">
        {label}
      </label>
      
      <textarea
        ref={textareaRef}
        id="translation-input"
        className="input-textarea"
        value={value}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder={placeholder}
        disabled={disabled}
        maxLength={maxLength}
        rows={4}
        autoComplete="off"
        spellCheck="false"
      />
      
      <div className="input-info">
        <span className="input-hint">{hint}</span>
        <span className="character-count">
          {characterCount}/{maxLength}
        </span>
      </div>
    </div>
  );
};

export default TranslationInput;
