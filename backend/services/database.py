from supabase import create_client
from config import Config
from datetime import datetime
import json
import uuid

class DatabaseService:
    def __init__(self):
        try:
            self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            print("✅ Database connection initialized successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            raise
    
    def save_itinerary(self, request_data, ai_response, user_id=None):
        """Save complete itinerary to database with enhanced data structure"""
        try:
            print(f"🔄 Saving complete itinerary to database...")
            print(f"User ID: {user_id}")
            print(f"Destination: {request_data.get('destination')}")
            
            # Prepare main itinerary data
            itinerary_data = {
                'user_id': user_id,
                'destination': request_data['destination'],
                'start_date': request_data['start_date'],
                'end_date': request_data['end_date'],
                'travelers': request_data.get('travelers', 1),
                'min_budget': float(request_data.get('min_budget', 0)) if request_data.get('min_budget') else None,
                'max_budget': float(request_data.get('max_budget', 0)) if request_data.get('max_budget') else None,
                'vegetarian_preference': request_data.get('vegetarian_preference', False),
                'special_requirements': request_data.get('special_requirements', ''),
                'ai_generated_itinerary': ai_response,  # Store complete AI response as JSONB
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            print(f"💾 Inserting main itinerary data...")
            print(f"AI Response Keys: {list(ai_response.keys()) if isinstance(ai_response, dict) else 'Not a dict'}")
            
            # Save main itinerary
            result = self.supabase.table('itineraries').insert(itinerary_data).execute()
            
            if not result.data:
                print("❌ Failed to insert itinerary - no data returned")
                return None
                
            itinerary_id = result.data[0]['id']
            print(f"✅ Main itinerary saved with ID: {itinerary_id}")
            
            # Save additional structured data
            try:
                self._save_additional_data(itinerary_id, ai_response)
            except Exception as e:
                print(f"⚠️ Warning: Failed to save additional data: {str(e)}")
                # Continue even if additional data fails
            
            print(f"✅ Complete itinerary {itinerary_id} saved successfully!")
            return result.data[0]
            
        except Exception as e:
            print(f"❌ Error saving itinerary: {str(e)}")
            print(f"Request data: {request_data}")
            print(f"AI Response type: {type(ai_response)}")
            return None
    
    def _save_additional_data(self, itinerary_id, ai_response):
        """Save additional itinerary data to related tables"""
        try:
            print(f"💾 Saving additional data for itinerary {itinerary_id}")
            
            # Save daily activities if available
            daily_activities = ai_response.get('daily_itinerary', [])
            if daily_activities and isinstance(daily_activities, list):
                print(f"Found {len(daily_activities)} days of activities")
                self._save_itinerary_activities(itinerary_id, daily_activities)
            else:
                print("No daily activities found in AI response")
                
            # Save accommodation suggestions
            accommodations = ai_response.get('accommodation_suggestions', [])
            if accommodations:
                print(f"Found {len(accommodations)} accommodation suggestions")
                # You can add accommodation table if needed
                
            # Save transportation info
            transportation = ai_response.get('transportation', {})
            if transportation:
                print("Found transportation information")
                # You can add transportation table if needed
                
        except Exception as e:
            print(f"⚠️ Additional data save error: {str(e)}")
    
    def _save_itinerary_activities(self, itinerary_id, daily_activities):
        """Save daily activities to itinerary_activities table"""
        try:
            activities_to_insert = []
            
            for day_data in daily_activities:
                if not isinstance(day_data, dict):
                    continue
                    
                day_number = day_data.get('day', 1)
                activities = day_data.get('activities', [])
                
                print(f"Processing day {day_number} with {len(activities)} activities")
                
                if isinstance(activities, list):
                    for activity in activities:
                        if isinstance(activity, dict):
                            activity_data = {
                                'itinerary_id': itinerary_id,
                                'day_number': day_number,
                                'activity_type': activity.get('type', 'sightseeing'),
                                'title': activity.get('activity', activity.get('title', 'Activity')),
                                'description': activity.get('description', ''),
                                'location': activity.get('location', ''),
                                'estimated_cost': self._extract_cost(activity.get('estimated_cost')),
                                'start_time': self._extract_time(activity.get('time')),
                                'end_time': None,
                                'created_at': datetime.now().isoformat()
                            }
                            activities_to_insert.append(activity_data)
            
            if activities_to_insert:
                print(f"💾 Inserting {len(activities_to_insert)} activities...")
                result = self.supabase.table('itinerary_activities').insert(activities_to_insert).execute()
                if result.data:
                    print(f"✅ {len(result.data)} activities saved successfully")
                else:
                    print("⚠️ No activities data returned from insert")
            else:
                print("⚠️ No activities to insert")
                    
        except Exception as e:
            print(f"❌ Error saving activities: {str(e)}")
    
    def _extract_cost(self, cost_string):
        """Extract numeric cost from string like '₹200-400' or '₹300'"""
        if not cost_string:
            return None
            
        try:
            import re
            numbers = re.findall(r'\d+', str(cost_string))
            if numbers:
                return float(numbers[0])
        except:
            pass
        return None
    
    def _extract_time(self, time_string):
        """Extract time from string like '09:00 AM'"""
        if not time_string:
            return None
            
        try:
            import re
            # Extract time pattern like "09:00 AM" or "14:30"
            time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', str(time_string))
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                period = time_match.group(3)
                
                if period == 'PM' and hour != 12:
                    hour += 12
                elif period == 'AM' and hour == 12:
                    hour = 0
                    
                return f"{hour:02d}:{minute:02d}:00"
        except:
            pass
        return None
    
    def get_user_itineraries(self, user_id):
        """Get all itineraries for a user with complete data"""
        try:
            print(f"🔍 Fetching complete itineraries for user: {user_id}")
            
            result = self.supabase.table('itineraries')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            print(f"✅ Found {len(result.data)} itineraries")
            
            # Enhance each itinerary with activities
            for itinerary in result.data:
                try:
                    activities_result = self.supabase.table('itinerary_activities')\
                        .select('*')\
                        .eq('itinerary_id', itinerary['id'])\
                        .order('day_number', desc=False)\
                        .execute()
                    
                    if activities_result.data:
                        itinerary['structured_activities'] = activities_result.data
                        print(f"Added {len(activities_result.data)} activities to itinerary {itinerary['id']}")
                except Exception as e:
                    print(f"⚠️ Could not fetch activities for itinerary {itinerary['id']}: {str(e)}")
            
            return result.data
            
        except Exception as e:
            print(f"❌ Error fetching user itineraries: {str(e)}")
            return []
    
    def get_itinerary_by_id(self, itinerary_id):
        """Get specific itinerary by ID with all related data"""
        try:
            print(f"🔍 Fetching complete itinerary: {itinerary_id}")
            
            # Get main itinerary
            result = self.supabase.table('itineraries')\
                .select('*')\
                .eq('id', itinerary_id)\
                .execute()
            
            if not result.data:
                return None
                
            itinerary = result.data[0]
            
            # Get related activities
            try:
                activities_result = self.supabase.table('itinerary_activities')\
                    .select('*')\
                    .eq('itinerary_id', itinerary_id)\
                    .order('day_number', desc=False)\
                    .execute()
                
                if activities_result.data:
                    itinerary['structured_activities'] = activities_result.data
                    print(f"✅ Found {len(activities_result.data)} related activities")
            except Exception as e:
                print(f"⚠️ Could not fetch related activities: {str(e)}")
            
            print(f"✅ Complete itinerary fetched successfully")
            return itinerary
            
        except Exception as e:
            print(f"❌ Error fetching itinerary: {str(e)}")
            return None
    
    def test_connection(self):
        """Test database connection and table access"""
        try:
            print("🔄 Testing database connection...")
            
            # Test users table
            users_result = self.supabase.table('users').select('id').limit(1).execute()
            print(f"✅ Users table accessible: {len(users_result.data)} records found")
            
            # Test itineraries table
            itineraries_result = self.supabase.table('itineraries').select('id').limit(1).execute()
            print(f"✅ Itineraries table accessible: {len(itineraries_result.data)} records found")
            
            # Test activities table
            activities_result = self.supabase.table('itinerary_activities').select('id').limit(1).execute()
            print(f"✅ Activities table accessible: {len(activities_result.data)} records found")
            
            print("✅ Database connection test successful")
            return True
        except Exception as e:
            print(f"❌ Database connection test failed: {str(e)}")
            return False