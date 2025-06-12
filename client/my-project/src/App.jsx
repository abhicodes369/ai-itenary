import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ItineraryProvider } from './contexts/ItenaryContext';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import ItineraryCreation from './components/Itenarycreation';
import ItineraryDisplay from './components/Itenarydisplay';

const AppContent = () => {
  const { user, isLoading } = useAuth();
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedItinerary, setSelectedItinerary] = useState(null);

  const handleNavigate = (page, data = null) => {
    console.log('Navigation called:', { page, data: data ? 'Data provided' : 'No data' });
    
    setCurrentPage(page);
    
    if (data) {
      console.log('Setting itinerary data:', data);
      setSelectedItinerary(data);
    }
    
    // Clear selected itinerary when navigating away from view page
    if (page !== 'view') {
      setSelectedItinerary(null);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LandingPage />;
  }

  console.log('Current page:', currentPage);
  console.log('Selected itinerary:', selectedItinerary ? 'Available' : 'Not available');

  switch (currentPage) {
    case 'create':
      return <ItineraryCreation onNavigate={handleNavigate} />;
    case 'view':
      return (
        <ItineraryDisplay 
          onNavigate={handleNavigate} 
          itinerary={selectedItinerary} 
        />
      );
    default:
      return <Dashboard onNavigate={handleNavigate} />;
  }
};

function App() {
  return (
    <AuthProvider>
      <ItineraryProvider>
        <AppContent />
      </ItineraryProvider>
    </AuthProvider>
  );
}

export default App;