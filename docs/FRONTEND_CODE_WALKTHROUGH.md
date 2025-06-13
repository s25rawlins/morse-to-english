# Frontend Code Overview

This document provides an overview of the React frontend for the Morse Code Translator.

## Architecture

The frontend is built with React using functional components and hooks. It follows a component-based architecture with clear separation of concerns.

### Key Components

- **App.jsx** - Main application component that handles layout
- **MorseTranslator.jsx** - Core translation logic and state management
- **TranslationInput.jsx** - Input field with validation
- **TranslationOutput.jsx** - Display area for translation results
- **MorseReference.jsx** - Interactive reference table
- **Header.jsx** - Application header and description

### State Management

The application uses React's built-in state management with `useState` hooks. State is managed locally within components where it's needed, keeping the architecture simple and maintainable.

Key state variables in MorseTranslator:
- `mode` - Translation direction (english-to-morse or morse-to-english)
- `input` - User input text
- `output` - Translation result
- `isLoading` - Loading state for API calls
- `error` - Error messages
- `success` - Success messages

### API Communication

The frontend communicates with the backend through a service layer (`services/api.js`) using Axios for HTTP requests. This provides:

- Centralized API configuration
- Consistent error handling
- Request/response interceptors
- Environment-specific base URLs

### Performance Optimizations

- **Debouncing** - API calls are debounced by 500ms to avoid excessive requests while typing
- **useCallback** - Functions are memoized to prevent unnecessary re-renders
- **Conditional rendering** - Components only render when needed

### Styling

The application uses CSS modules for styling, providing:
- Component-scoped styles
- Responsive design
- Clean, modern interface
- Accessibility considerations

## Development Patterns

### Hooks Used

- `useState` - Component state management
- `useEffect` - Side effects and API calls
- `useCallback` - Function memoization
- `useRef` - Persistent references (debounce timers)

### Error Handling

The application implements comprehensive error handling:
- Input validation
- API error responses
- User-friendly error messages
- Graceful fallbacks

### Testing

Components are tested using Jest and React Testing Library, focusing on:
- User interactions
- API integration
- Error scenarios
- Component rendering

## File Structure

```
frontend/src/
├── App.jsx                 # Main application
├── index.js               # Entry point
├── components/            # React components
│   ├── Header.jsx
│   ├── MorseTranslator.jsx
│   ├── TranslationInput.jsx
│   ├── TranslationOutput.jsx
│   ├── MorseReference.jsx
│   ├── LoadingSpinner.jsx
│   └── Toast.jsx
├── services/              # API layer
│   └── api.js
└── styles/               # CSS files
    └── App.css
```

## Getting Started

1. Install dependencies: `npm install`
2. Start development server: `npm start`
3. Run tests: `npm test`
4. Build for production: `npm run build`

The application will be available at `http://localhost:3000` and will automatically proxy API requests to the backend server.
