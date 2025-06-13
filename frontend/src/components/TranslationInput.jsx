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

  // Track focus state and cursor position
  const handleFocus = useCallback(() => {
    wasFocusedRef.current = true;
    isRestoringFocusRef.current = false;
  }, []);

  const handleBlur = useCallback((e) => {
    // Don't mark as unfocused if we're programmatically restoring focus
    if (!isRestoringFocusRef.current) {
      wasFocusedRef.current = false;
    }
  }, []);

  const handleChange = useCallback((e) => {
    // Store cursor position before state update
    const newCursorPosition = e.target.selectionStart;
    cursorPositionRef.current = newCursorPosition;
    onChange(e.target.value);
  }, [onChange]);

  // Aggressive focus preservation
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea && wasFocusedRef.current && !disabled) {
      // Multiple strategies to maintain focus
      
      // Strategy 1: Immediate restoration
      if (document.activeElement !== textarea) {
        isRestoringFocusRef.current = true;
        textarea.focus();
        textarea.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
      }

      // Strategy 2: Delayed restoration (for async updates)
      const timeoutId = setTimeout(() => {
        if (textarea && wasFocusedRef.current && document.activeElement !== textarea) {
          isRestoringFocusRef.current = true;
          textarea.focus();
          textarea.setSelectionRange(cursorPositionRef.current, cursorPositionRef.current);
        }
        isRestoringFocusRef.current = false;
      }, 0);

      // Strategy 3: Animation frame restoration (for render cycles)
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
  }); // Run on every render to catch all state changes

  // Memoize computed values to prevent unnecessary re-renders
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
