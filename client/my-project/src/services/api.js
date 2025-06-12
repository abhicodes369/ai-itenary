// src/services/api.js
const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  static async generateItinerary(data) {
    try {
      console.log('API: Sending request to generate itinerary:', data);
      
      const response = await fetch(`${API_BASE_URL}/generate-itinerary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add user ID header if available
          'X-User-ID': this.getUserId() || 'anonymous'
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || `HTTP error! status: ${response.status}`);
      }

      console.log('API: Itinerary generated successfully:', result);
      return result;
      
    } catch (error) {
      console.error('API: Error generating itinerary:', error);
      throw error;
    }
  }

  static async getUserItineraries(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/itineraries?user_id=${userId || this.getUserId()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': userId || this.getUserId() || 'anonymous'
        },
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || `HTTP error! status: ${response.status}`);
      }

      return result.data || [];
      
    } catch (error) {
      console.error('API: Error fetching itineraries:', error);
      throw error;
    }
  }

  static async getItinerary(itineraryId) {
    try {
      const response = await fetch(`${API_BASE_URL}/itineraries/${itineraryId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || `HTTP error! status: ${response.status}`);
      }

      return result.data;
      
    } catch (error) {
      console.error('API: Error fetching itinerary:', error);
      throw error;
    }
  }

  static async deleteItinerary(itineraryId) {
    try {
      const response = await fetch(`${API_BASE_URL}/itineraries/${itineraryId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || `HTTP error! status: ${response.status}`);
      }

      return true;
      
    } catch (error) {
      console.error('API: Error deleting itinerary:', error);
      throw error;
    }
  }

  // Helper method to get user ID (implement based on your auth system)
  static getUserId() {
    // This should get the user ID from your authentication system
    // For now, return a default or from localStorage
    return localStorage.getItem('userId') || 'user_123';
  }

  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('API: Health check failed:', error);
      throw error;
    }
  }
}

export default ApiService;