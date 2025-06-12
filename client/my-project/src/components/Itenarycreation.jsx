// ItineraryCreation.jsx - Fixed version
import React, { useState } from 'react';
import { useItinerary } from '../contexts/ItenaryContext';

const ItineraryCreation = ({ onNavigate }) => {
  const [destination, setDestination] = useState('');
  const [startDate, setStartDate] = useState('');
  const [duration, setDuration] = useState('');
  const [budget, setBudget] = useState('');
  const [isVegetarian, setIsVegetarian] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { generateItinerary } = useItinerary();

  // Function to calculate end date from start date and duration
  const calculateEndDate = (startDateStr, durationDays) => {
    const startDate = new Date(startDateStr);
    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + parseInt(durationDays) - 1);
    return endDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate required fields
      if (!destination.trim()) {
        throw new Error('Please enter a destination');
      }
      if (!startDate) {
        throw new Error('Please select a start date');
      }
      if (!duration || parseInt(duration) < 1) {
        throw new Error('Please enter a valid duration');
      }
      if (!budget || parseInt(budget) < 1) {
        throw new Error('Please enter a valid budget');
      }

      // Calculate end date
      const endDate = calculateEndDate(startDate, duration);

      // Prepare data for API
      const itineraryData = {
        destination: destination.trim(),
        start_date: startDate,
        end_date: endDate,
        duration: parseInt(duration),
        budget: parseInt(budget),
        isVegetarian: isVegetarian
      };

      console.log('Sending itinerary data:', itineraryData);

      // Call the API
      const result = await generateItinerary(itineraryData);
      
      if (result) {
        console.log('Itinerary generated successfully:', result);
        
        // FIXED: Navigate to view page with the generated itinerary
        if (onNavigate) {
          onNavigate('view', result);
        } else {
          console.error('onNavigate function not provided');
        }
      } else {
        throw new Error('No itinerary data received');
      }

    } catch (error) {
      console.error('Error creating itinerary:', error);
      setError(error.message || 'Failed to create itinerary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Create Your Dream Itinerary</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Destination */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Where do you want to go? *
          </label>
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Enter destination (e.g., Goa, Kerala, Rajasthan)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Start Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Start Date *
          </label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            min={new Date().toISOString().split('T')[0]}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Duration */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Duration (days) *
          </label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            placeholder="Number of days"
            min="1"
            max="30"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Budget */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Total Budget (₹) *
          </label>
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            placeholder="Total budget in rupees"
            min="1000"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Vegetarian Preference */}
        <div className="flex items-center">
          <input
            type="checkbox"
            id="vegetarian"
            checked={isVegetarian}
            onChange={(e) => setIsVegetarian(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="vegetarian" className="ml-2 block text-sm text-gray-700">
            Vegetarian food only
          </label>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-4 rounded-md text-white font-medium ${
            loading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500'
          }`}
        >
          {loading ? 'Creating Itinerary...' : 'Create Itinerary'}
        </button>
      </form>

      {/* Show calculated end date if both start date and duration are provided */}
      {startDate && duration && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded">
          <p className="text-sm text-blue-700">
            <strong>Trip Duration:</strong> {startDate} to {calculateEndDate(startDate, duration)} 
            ({duration} days)
          </p>
        </div>
      )}
    </div>
  );
};

export default ItineraryCreation;