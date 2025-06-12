// Dashboard.jsx - Updated to use context correctly
import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useItinerary } from '../contexts/ItenaryContext';
import { Plus, MapPin, Calendar, Users, LogOut, Trash2 } from 'lucide-react';

const Dashboard = ({ onNavigate }) => {
  const { user, logout } = useAuth();
  const { 
    itineraries, 
    loading, 
    error, 
    deleteItinerary, 
    refreshItineraries 
  } = useItinerary();

  // Refresh itineraries when component mounts
  useEffect(() => {
    if (user) {
      refreshItineraries();
    }
  }, [user, refreshItineraries]);

  const handleCreateItinerary = () => {
    if (onNavigate) {
      onNavigate('create');
    }
  };

  const handleViewItinerary = (itinerary) => {
    if (onNavigate) {
      onNavigate('view', itinerary);
    }
  };

  const handleDeleteItinerary = async (e, itineraryId) => {
    e.stopPropagation(); // Prevent triggering view
    
    if (window.confirm('Are you sure you want to delete this itinerary?')) {
      try {
        await deleteItinerary(itineraryId);
      } catch (error) {
        alert('Failed to delete itinerary. Please try again.');
      }
    }
  };

  const formatDate = (dateString) => {
    try {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Invalid Date';
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: '2-digit',
        year: 'numeric'
      });
    } catch (error) {
      return 'Invalid Date';
    }
  };

  const calculateStats = () => {
    if (!Array.isArray(itineraries)) {
      return { totalTrips: 0, upcomingTrips: 0, totalBudget: 0 };
    }

    const now = new Date();
    const totalTrips = itineraries.length;
    
    const upcomingTrips = itineraries.filter(it => {
      try {
        return it?.start_date && new Date(it.start_date) > now;
      } catch {
        return false;
      }
    }).length;
    
    const totalBudget = itineraries.reduce((acc, it) => {
      return acc + (it?.max_budget || 0);
    }, 0);

    return { totalTrips, upcomingTrips, totalBudget };
  };

  const stats = calculateStats();

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <MapPin className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-gray-900">TravelPlan</span>
            </div>
            <div className="flex items-center space-x-4">
              {user?.picture && (
                <img 
                  src={user.picture} 
                  alt={user?.name || 'User'}
                  className="w-10 h-10 rounded-full"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              )}
              <div className="hidden md:block">
                <p className="text-sm font-medium text-gray-900">{user?.name || 'User'}</p>
                <p className="text-xs text-gray-500">{user?.email || ''}</p>
              </div>
              <button
                onClick={logout}
                className="p-2 text-gray-400 hover:text-gray-950 transition-colors"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name?.split(' ')[0] || 'there'}! 👋
          </h1>
          <p className="text-gray-600">
            Ready to plan your next adventure? Let's make it unforgettable.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Trips</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalTrips}</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-full">
                <MapPin className="h-6 w-6 text-blue-500" />
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Upcoming</p>
                <p className="text-3xl font-bold text-gray-900">{stats.upcomingTrips}</p>
              </div>
              <div className="p-3 bg-green-50 rounded-full">
                <Calendar className="h-6 w-6 text-green-500" />
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Budget</p>
                <p className="text-3xl font-bold text-gray-900">₹{stats.totalBudget.toLocaleString()}</p>
              </div>
              <div className="p-3 bg-purple-50 rounded-full">
                <Users className="h-6 w-6 text-purple-500" />
              </div>
            </div>
          </div>
        </div>

        {/* Create New Trip */}
        <div className="mb-8">
          <button
            onClick={handleCreateItinerary}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-xl transition-all duration-200 w-full md:w-auto border-dashed hover:border-blue-500 cursor-pointer group"
          >
            <div className="flex items-center justify-center space-x-3 text-blue-500 group-hover:text-blue-600">
              <Plus className="h-8 w-8" />
              <div className="text-left">
                <p className="text-lg font-semibold">Create New Itinerary</p>
                <p className="text-sm text-gray-500">Plan your next adventure</p>
              </div>
            </div>
          </button>
        </div>

        {/* Recent Itineraries */}
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Itineraries</h2>
            {loading && (
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            )}
          </div>
          
          {!Array.isArray(itineraries) || itineraries.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center py-12">
              <MapPin className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No itineraries yet
              </h3>
              <p className="text-gray-600 mb-6">
                Create your first travel itinerary to get started
              </p>
              <button 
                onClick={handleCreateItinerary} 
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create Itinerary
              </button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {itineraries.map((itinerary, index) => {
                if (!itinerary) return null;
                
                return (
                  <div
                    key={itinerary.id || index}
                    className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-xl transition-all duration-200 cursor-pointer group relative"
                    onClick={() => handleViewItinerary(itinerary)}
                  >
                    {/* Delete Button */}
                    {itinerary.id && (
                      <button
                        onClick={(e) => handleDeleteItinerary(e, itinerary.id)}
                        className="absolute top-4 right-4 p-2 text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                    
                    <div className="mb-4">
                      <div className="w-full h-32 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg mb-4 flex items-center justify-center">
                        <MapPin className="h-12 w-12 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                        {itinerary.destination || 'Unknown Destination'}
                      </h3>
                      <div className="space-y-2 text-sm text-gray-600">
                        {itinerary.start_date && itinerary.end_date && (
                          <div className="flex items-center space-x-2">
                            <Calendar className="h-4 w-4" />
                            <span>
                              {formatDate(itinerary.start_date)} - {formatDate(itinerary.end_date)}
                            </span>
                          </div>
                        )}
                        {itinerary.travelers && (
                          <div className="flex items-center space-x-2">
                            <Users className="h-4 w-4" />
                            <span>{itinerary.travelers} travelers</span>
                          </div>
                        )}
                        {(itinerary.min_budget || itinerary.max_budget) && (
                          <div className="flex items-center space-x-2">
                            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                              Budget: ₹{(itinerary.max_budget || itinerary.min_budget || 0).toLocaleString()}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                      <span className="text-xs text-gray-500">
                        Created: {formatDate(itinerary.created_at)}
                      </span>
                      <span className="text-xs text-blue-600 font-medium group-hover:text-blue-700">
                        View Details →
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;