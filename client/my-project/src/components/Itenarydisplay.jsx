import React from 'react';
import { MapPin, Calendar, Clock, DollarSign, Utensils, Star, Phone, AlertCircle, ArrowLeft } from 'lucide-react';

const ItineraryDisplay = ({ itinerary, onNavigate }) => {
  // Debug logging
  console.log('ItineraryDisplay received itinerary:', itinerary);

  if (!itinerary) {
    return (
      <div className="max-w-4xl mx-auto p-4 sm:p-6">
        <div className="text-center py-8 sm:py-12">
          <AlertCircle className="h-12 w-12 sm:h-16 sm:w-16 text-gray-300 mx-auto mb-4" />
          <p className="text-base sm:text-lg text-gray-500">No itinerary to display</p>
          <button 
            onClick={() => onNavigate && onNavigate('dashboard')}
            className="mt-4 bg-blue-600 text-white px-4 sm:px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  // Group items by day_number if items exist
  let groupedItems = [];
  if (Array.isArray(itinerary.items) && itinerary.items.length > 0) {
    const daysMap = {};
    itinerary.items.forEach(item => {
      const day = item.day_number || 1;
      if (!daysMap[day]) daysMap[day] = [];
      daysMap[day].push(item);
    });
    groupedItems = Object.entries(daysMap)
      .sort((a, b) => Number(a[0]) - Number(b[0]))
      .map(([day, items]) => ({ day, items }));
  }

  const DayCard = ({ day, index, items }) => {
    // If items are provided (from saved itinerary), render them as activities
    if (items) {
      return (
        <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 mb-4 sm:mb-6">
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <h3 className="text-lg sm:text-xl font-bold text-blue-600">
              Day {day || index + 1}
            </h3>
          </div>
          <div className="mb-4 sm:mb-6">
            <h4 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 flex items-center">
              <MapPin className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              Activities
            </h4>
            <div className="space-y-3 sm:space-y-4">
              {items.map((activity, idx) => (
                <div key={activity.id || idx} className="border-l-4 border-blue-500 pl-3 sm:pl-4">
                  <div className="flex items-center justify-between mb-1 sm:mb-2">
                    <h5 className="font-semibold text-gray-800 text-sm sm:text-base">
                      {activity.title || activity.activity || activity.name || `Activity ${idx + 1}`}
                    </h5>
                    {activity.start_time && (
                      <div className="flex items-center text-xs sm:text-sm text-gray-600">
                        <Clock className="w-3 h-3 sm:w-4 sm:h-4 mr-1" />
                        {activity.start_time}
                      </div>
                    )}
                  </div>
                  {activity.description && (
                    <p className="text-xs sm:text-sm text-gray-600 mb-1 sm:mb-2">{activity.description}</p>
                  )}
                  <div className="flex flex-wrap gap-2 sm:gap-4 text-xs sm:text-sm text-gray-500">
                    {activity.location && <span>📍 {activity.location}</span>}
                    {activity.duration && <span>⏱️ {activity.duration}</span>}
                    {activity.estimated_cost && <span>💰 {activity.estimated_cost}</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }
    if (!day) return null;

    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 mb-4 sm:mb-6">
        <div className="flex items-center justify-between mb-3 sm:mb-4">
          <h3 className="text-lg sm:text-xl font-bold text-blue-600">
            Day {day.day || index + 1}
          </h3>
          {day.date && (
            <div className="flex items-center text-xs sm:text-sm text-gray-600">
              <Calendar className="w-3 h-3 sm:w-4 sm:h-4 mr-1" />
              <span>{day.date} {day.day_name && `(${day.day_name})`}</span>
            </div>
          )}
        </div>
        
        {day.theme && (
          <p className="text-sm sm:text-base text-gray-700 mb-3 sm:mb-4 italic">{day.theme}</p>
        )}

        {/* Activities */}
        {day.activities && day.activities.length > 0 && (
          <div className="mb-4 sm:mb-6">
            <h4 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 flex items-center">
              <MapPin className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              Activities
            </h4>
            <div className="space-y-3 sm:space-y-4">
              {day.activities.map((activity, idx) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-3 sm:pl-4">
                  <div className="flex items-center justify-between mb-1 sm:mb-2">
                    <h5 className="font-semibold text-gray-800 text-sm sm:text-base">
                      {activity.activity || activity.name || `Activity ${idx + 1}`}
                    </h5>
                    {activity.time && (
                      <div className="flex items-center text-xs sm:text-sm text-gray-600">
                        <Clock className="w-3 h-3 sm:w-4 sm:h-4 mr-1" />
                        {activity.time}
                      </div>
                    )}
                  </div>
                  {activity.description && (
                    <p className="text-xs sm:text-sm text-gray-600 mb-1 sm:mb-2">{activity.description}</p>
                  )}
                  <div className="flex flex-wrap gap-2 sm:gap-4 text-xs sm:text-sm text-gray-500">
                    {activity.location && <span>📍 {activity.location}</span>}
                    {activity.duration && <span>⏱️ {activity.duration}</span>}
                    {activity.estimated_cost && <span>💰 {activity.estimated_cost}</span>}
                  </div>
                  {activity.highlights && Array.isArray(activity.highlights) && (
                    <div className="mt-1 sm:mt-2">
                      <span className="text-xs font-semibold text-blue-600">Highlights: </span>
                      <span className="text-xs text-gray-600">{activity.highlights.join(', ')}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Meals */}
        {day.meals && day.meals.length > 0 && (
          <div className="mb-3 sm:mb-4">
            <h4 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 flex items-center">
              <Utensils className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              Meals
            </h4>
            <div className="grid gap-2 sm:gap-3">
              {day.meals.map((meal, idx) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-2 sm:p-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium capitalize text-sm sm:text-base">
                      {meal.meal_type || meal.type || `Meal ${idx + 1}`}
                    </span>
                    {meal.time && (
                      <span className="text-xs sm:text-sm text-gray-600">{meal.time}</span>
                    )}
                  </div>
                  {meal.restaurant && (
                    <p className="text-xs sm:text-sm font-semibold text-gray-800">{meal.restaurant}</p>
                  )}
                  <div className="flex items-center justify-between text-xs text-gray-600">
                    {meal.cuisine && <span>{meal.cuisine}</span>}
                    {meal.estimated_cost && <span>{meal.estimated_cost}</span>}
                  </div>
                  {meal.specialties && Array.isArray(meal.specialties) && (
                    <p className="text-xs text-blue-600 mt-1">Try: {meal.specialties.join(', ')}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Daily Budget */}
        {day.daily_budget_breakdown && (
          <div className="bg-blue-50 rounded-lg p-2 sm:p-3">
            <h5 className="font-semibold text-blue-800 mb-1 sm:mb-2 text-sm sm:text-base">Daily Budget Breakdown</h5>
            <div className="grid grid-cols-2 gap-2 text-xs sm:text-sm">
              {Object.entries(day.daily_budget_breakdown).map(([category, amount]) => (
                <div key={category} className="flex justify-between">
                  <span className="capitalize text-gray-700">{category.replace('_', ' ')}:</span>
                  <span className="font-medium">{amount}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6">
      {/* Back Button */}
      <button
        onClick={() => onNavigate && onNavigate('dashboard')}
        className="mb-4 sm:mb-6 flex items-center text-blue-600 hover:text-blue-700 transition-colors text-sm sm:text-base"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Dashboard
      </button>

      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-4 sm:p-6 mb-4 sm:mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold mb-2">
          {itinerary.destination || 'Your Trip'} Itinerary
        </h1>
        {itinerary.trip_summary && (
          <p className="text-sm sm:text-base text-blue-100 mb-3 sm:mb-4">{itinerary.trip_summary}</p>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
          {itinerary.duration && (
            <div className="flex items-center text-sm sm:text-base">
              <Calendar className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              <span>{itinerary.duration}</span>
            </div>
          )}
          {itinerary.total_estimated_cost && (
            <div className="flex items-center text-sm sm:text-base">
              <DollarSign className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              <span>{itinerary.total_estimated_cost}</span>
            </div>
          )}
          {itinerary.destination && (
            <div className="flex items-center text-sm sm:text-base">
              <MapPin className="w-4 h-4 sm:w-5 sm:h-5 mr-2" />
              <span>{itinerary.destination}</span>
            </div>
          )}
        </div>
      </div>

      {/* Daily Itinerary (AI generated) */}
      {itinerary.daily_itinerary && itinerary.daily_itinerary.length > 0 && (
        <div className="mb-6 sm:mb-8">
          <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6">Day-by-Day Itinerary</h2>
          {itinerary.daily_itinerary.map((day, index) => (
            <DayCard key={day.day || index} day={day} index={index} />
          ))}
        </div>
      )}

      {/* Daily Itinerary (Saved items) */}
      {groupedItems.length > 0 && (
        <div className="mb-6 sm:mb-8">
          <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6">Day-by-Day Itinerary</h2>
          {groupedItems.map(({ day, items }) => (
            <DayCard key={day} day={day} items={items} />
          ))}
        </div>
      )}

      {/* If no itinerary details available */}
      {(!itinerary.daily_itinerary || itinerary.daily_itinerary.length === 0) && groupedItems.length === 0 && (
        <div className="text-center text-gray-500 my-12">
          <p>No detailed itinerary available for this trip.</p>
        </div>
      )}

      {/* Additional Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Accommodation */}
        {itinerary.accommodation_suggestions && itinerary.accommodation_suggestions.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">Accommodation Suggestions</h3>
            {itinerary.accommodation_suggestions.map((hotel, idx) => (
              <div key={idx} className="border-b pb-4 mb-4 last:border-b-0 last:mb-0">
                <h4 className="font-semibold">{hotel.name || `Hotel ${idx + 1}`}</h4>
                {hotel.location && (
                  <p className="text-sm text-gray-600 mb-2">{hotel.location}</p>
                )}
                <div className="flex items-center gap-4 text-sm">
                  {hotel.rating && (
                    <span className="flex items-center">
                      <Star className="w-4 h-4 mr-1 text-yellow-500" />
                      {hotel.rating}
                    </span>
                  )}
                  {hotel.estimated_cost_per_night && (
                    <span>{hotel.estimated_cost_per_night}</span>
                  )}
                </div>
                {hotel.booking_tips && (
                  <p className="text-xs text-gray-500 mt-2">{hotel.booking_tips}</p>
                )}
                {hotel.amenities && Array.isArray(hotel.amenities) && (
                  <p className="text-xs text-green-600 mt-1">
                    Amenities: {hotel.amenities.join(', ')}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Transportation */}
        {itinerary.transportation && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">Transportation</h3>
            
            {itinerary.transportation.to_destination && (
              <div className="mb-4">
                <h4 className="font-semibold mb-2">To Destination</h4>
                <p className="text-sm text-gray-600">
                  Mode: {itinerary.transportation.to_destination.mode}
                </p>
                <p className="text-sm text-gray-600">
                  Cost: {itinerary.transportation.to_destination.estimated_cost}
                </p>
                {itinerary.transportation.to_destination.booking_tips && (
                  <p className="text-xs text-gray-500 mt-1">
                    {itinerary.transportation.to_destination.booking_tips}
                  </p>
                )}
              </div>
            )}

            {itinerary.transportation.local_transport && Array.isArray(itinerary.transportation.local_transport) && (
              <div>
                <h4 className="font-semibold mb-2">Local Transport</h4>
                {itinerary.transportation.local_transport.map((transport, idx) => (
                  <div key={idx} className="text-sm mb-2">
                    <span className="font-medium">{transport.mode}</span>
                    {transport.usage && (
                      <span className="text-gray-600"> - {transport.usage}</span>
                    )}
                    {transport.estimated_cost && (
                      <span className="text-gray-500"> ({transport.estimated_cost})</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Local Tips */}
        {itinerary.local_tips && Array.isArray(itinerary.local_tips) && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">Local Tips</h3>
            <ul className="space-y-2">
              {itinerary.local_tips.map((tip, idx) => (
                <li key={idx} className="text-sm text-gray-700 flex items-start">
                  <span className="text-blue-500 mr-2">•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Emergency Contacts */}
        {itinerary.emergency_contacts && (
          <div className="bg-red-50 rounded-lg p-6">
            <h3 className="text-xl font-bold mb-4 flex items-center text-red-700">
              <AlertCircle className="w-5 h-5 mr-2" />
              Emergency Contacts
            </h3>
            <div className="space-y-2">
              {Object.entries(itinerary.emergency_contacts).map(([type, contact]) => (
                <div key={type} className="flex items-center text-sm">
                  <Phone className="w-4 h-4 mr-2 text-red-600" />
                  <span className="capitalize font-medium mr-2">
                    {type.replace('_', ' ')}:
                  </span>
                  <span>{contact}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Packing Suggestions */}
      {itinerary.packing_suggestions && Array.isArray(itinerary.packing_suggestions) && (
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h3 className="text-xl font-bold mb-4">Packing Suggestions</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {itinerary.packing_suggestions.map((item, idx) => (
              <div key={idx} className="text-sm text-gray-700 flex items-center">
                <span className="text-green-500 mr-2">✓</span>
                {item}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ItineraryDisplay;