// API Service for Chandas Identifier

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async healthCheck() {
    const response = await fetch(`${this.baseURL}/`);
    if (!response.ok) {
      throw new Error('Backend is not accessible');
    }
    return response.json();
  }

  async analyzeVerse(verse) {
    const response = await fetch(`${this.baseURL}/analyze-verse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ verse }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Analysis failed');
    }

    return response.json();
  }

  async analyzeVerses(verses) {
    const response = await fetch(`${this.baseURL}/analyze-verses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ verses }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Bulk analysis failed');
    }

    return response.json();
  }

  getDocsUrl() {
    return `${this.baseURL}/docs`;
  }

  getReDocUrl() {
    return `${this.baseURL}/redoc`;
  }
}

export default new ApiService();
