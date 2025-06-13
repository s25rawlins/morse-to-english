import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api/v1' 
  : 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    
    if (error.response?.status === 422) {
      // Validation error
      const detail = error.response.data?.detail;
      if (Array.isArray(detail)) {
        const messages = detail.map(err => err.msg).join(', ');
        throw new Error(`Validation error: ${messages}`);
      }
    }
    
    throw error;
  }
);

export const translateEnglishToMorse = async (text) => {
  try {
    const response = await api.post('/translate/english-to-morse', {
      text: text.trim()
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('Failed to translate English to Morse code');
  }
};

export const translateMorseToEnglish = async (morseCode) => {
  try {
    const response = await api.post('/translate/morse-to-english', {
      morse_code: morseCode.trim()
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('Failed to translate Morse code to English');
  }
};

export const getHealthStatus = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Failed to get health status');
  }
};

export const getSupportedCharacters = async () => {
  try {
    const response = await api.get('/supported-characters');
    return response.data;
  } catch (error) {
    throw new Error('Failed to get supported characters');
  }
};

export default api;
