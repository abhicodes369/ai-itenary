// ItineraryContext.jsx - Updated with database operations
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import ApiService from '../services/api';
import { useAuth } from './AuthContext';

const ItineraryContext = createContext();

export const useItinerary = () => {
  const context = useContext(ItineraryContext);
  if (!context) {
    throw new Error('useItinerary must be used within an ItineraryProvider');
  }
  return context;
};

export const ItineraryProvider = ({ children }) => {
  const [currentItinerary, setCurrentItinerary] = useState(null);
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const loadUserItineraries = useCallback(async () => {
    try {
      setLoading(true);
      const userId = user?.sub || ApiService.getUserId();
      const userItineraries = await ApiService.getUserItineraries(userId);
      setItineraries(userItineraries);
      console.log('Loaded user itineraries:', userItineraries);
    } catch (error) {
      console.error('Error loading itineraries:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }, [user?.sub]);

  // Load user itineraries only once when the component mounts
  useEffect(() => {
    if (user?.sub) {
      loadUserItineraries();
    }
  }, []); // Empty dependency array means this runs once on mount

  const generateItinerary = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Context: Generating itinerary with data:', formData);
      
      const requestData = {
        destination: formData.destination,
        start_date: formData.start_date,
        end_date: formData.end_date,
        duration: formData.duration,
        budget: formData.budget,
        isVegetarian: formData.isVegetarian || false,
        travelers: formData.travelers || 1,
        user_id: user?.sub || ApiService.getUserId()
      };

      if (!requestData.end_date) {
        throw new Error('End date is required but not provided');
      }

      const result = await ApiService.generateItinerary(requestData);
      
      if (result && result.data) {
        const newItinerary = result.data;
        
        // Update current itinerary
        setCurrentItinerary(newItinerary);
        
        // Add to itineraries list (if it has an ID, meaning it was saved)
        if (newItinerary.id) {
          setItineraries(prev => [newItinerary, ...prev]);
        }
        
        console.log('Context: Itinerary generated and saved successfully');
        return newItinerary;
      } else {
        throw new Error('Invalid response format from server');
      }
      
    } catch (error) {
      console.error('Context: Error generating itinerary:', error);
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const deleteItinerary = async (itineraryId) => {
    try {
      setLoading(true);
      await ApiService.deleteItinerary(itineraryId);
      
      // Remove from local state
      setItineraries(prev => prev.filter(it => it.id !== itineraryId));
      
      // Clear current itinerary if it was deleted
      if (currentItinerary?.id === itineraryId) {
        setCurrentItinerary(null);
      }
      
      return true;
    } catch (error) {
      console.error('Error deleting itinerary:', error);
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const getItinerary = async (itineraryId) => {
    try {
      setLoading(true);
      const itinerary = await ApiService.getItinerary(itineraryId);
      setCurrentItinerary(itinerary);
      return itinerary;
    } catch (error) {
      console.error('Error fetching itinerary:', error);
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const clearCurrentItinerary = () => {
    setCurrentItinerary(null);
    setError(null);
  };

  const refreshItineraries = useCallback(() => {
    loadUserItineraries();
  }, [loadUserItineraries]);

  const value = {
    currentItinerary,
    itineraries,
    loading,
    error,
    generateItinerary,
    deleteItinerary,
    getItinerary,
    clearCurrentItinerary,
    refreshItineraries,
    loadUserItineraries
  };

  return (
    <ItineraryContext.Provider value={value}>
      {children}
    </ItineraryContext.Provider>
  );
};