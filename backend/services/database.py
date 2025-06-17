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
    
    def upsert_user(self, user_data):
        """Upsert user data - insert if new, update if exists"""
        try:
            print(f"🔄 Upserting user data...")
            
            # Prepare user data with required fields
            user_record = {
                'id': user_data.get('id'),
                'email': user_data.get('email'),
                'google_id': user_data.get('google_id'),
                'created_at': user_data.get('created_at', datetime.now().isoformat())
            }
            
            # Remove None values
            user_record = {k: v for k, v in user_record.items() if v is not None}
            
            # Upsert user with conflict resolution on email or google_id
            result = self.supabase.table('users').upsert(
                user_record,
                on_conflict='email'  # or 'google_id' depending on your unique constraint
            ).execute()
            
            if result.data:
                print(f"✅ User upserted successfully: {result.data[0]['id']}")
                return result.data[0]
            else:
                print("❌ Failed to upsert user")
                return None
                
        except Exception as e:
            print(f"❌ Error upserting user: {str(e)}")
            return None
    
    def upsert_itinerary(self, request_data, ai_response, user_id, itinerary_id=None):
        """Upsert complete itinerary - update if exists, insert if new"""
        try:
            print(f"🔄 Upserting complete itinerary to database...")
            print(f"User ID: {user_id}")
            print(f"Itinerary ID: {itinerary_id}")
            print(f"Destination: {request_data.get('destination')}")
            
            # Generate new ID if not provided
            if not itinerary_id:
                itinerary_id = str(uuid.uuid4())
            
            # Prepare main itinerary data
            itinerary_data = {
                'id': itinerary_id,  # Include ID for upsert
                'user_id': user_id,
                'destination': request_data['destination'],
                'start_date': request_data['start_date'],
                'end_date': request_data['end_date'],
                'budget': float(request_data.get('budget', 0)) if request_data.get('budget') else None,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Add AI-generated content as JSONB
            if ai_response:
                itinerary_data['title'] = ai_response.get('destination', request_data['destination'])
                itinerary_data['description'] = ai_response.get('trip_summary', f"Trip to {request_data['destination']}")
            
            print(f"[DEBUG] Itinerary data to upsert: {itinerary_data}")
            
            # Upsert main itinerary
            result = self.supabase.table('itineraries').upsert(
                itinerary_data,
                on_conflict='id'  # Use ID as the conflict resolution field
            ).execute()
            
            print(f"[DEBUG] Supabase upsert result: {getattr(result, 'data', None)}")
            if hasattr(result, 'error') and getattr(result, 'error', None):
                print(f"[DEBUG] Supabase upsert error: {result.error}")
            
            if not result.data:
                print("❌ Failed to upsert itinerary - no data returned")
                return None
                
            saved_itinerary = result.data[0]
            print(f"✅ Main itinerary upserted with ID: {saved_itinerary['id']}")
            
            # Upsert itinerary items (daily activities)
            if ai_response and 'daily_itinerary' in ai_response:
                self._upsert_itinerary_items(saved_itinerary['id'], ai_response['daily_itinerary'])
            
            # Return the complete saved itinerary with AI response
            return {
                **saved_itinerary,
                'ai_response': ai_response
            }
            
        except Exception as e:
            print(f"❌ Error upserting itinerary: {str(e)}")
            print(f"Request data: {request_data}")
            print(f"AI Response type: {type(ai_response)}")
            return None
    
    def _upsert_itinerary_items(self, itinerary_id, daily_itinerary):
        """Upsert daily itinerary items"""
        try:
            print(f"💾 Upserting itinerary items for {itinerary_id}")
            
            # First, delete existing items for this itinerary to avoid duplicates
            delete_result = self.supabase.table('itinerary_items').delete().eq('itinerary_id', itinerary_id).execute()
            print(f"🗑️ Deleted existing items: {len(delete_result.data) if delete_result.data else 0}")
            
            items_to_upsert = []
            
            for day_data in daily_itinerary:
                if not isinstance(day_data, dict):
                    continue
                    
                day_number = day_data.get('day', 1)
                activities = day_data.get('activities', [])
                meals = day_data.get('meals', [])
                
                print(f"Processing day {day_number}: {len(activities)} activities, {len(meals)} meals")
                
                # Process activities
                for idx, activity in enumerate(activities):
                    if isinstance(activity, dict):
                        item_data = {
                            'id': str(uuid.uuid4()),  # Generate unique ID for each item
                            'itinerary_id': itinerary_id,
                            'day_number': day_number,
                            'activity_type': activity.get('type', 'activity'),
                            'title': activity.get('activity', activity.get('title', 'Activity')),
                            'description': activity.get('description', ''),
                            'location': activity.get('location', ''),
                            'start_time': self._extract_time(activity.get('time')),
                            'end_time': None,  # Could be calculated from duration
                            'cost': self._extract_cost(activity.get('estimated_cost')),
                            'notes': json.dumps(activity.get('tips', [])) if activity.get('tips') else None,
                            'created_at': datetime.now().isoformat()
                        }
                        items_to_upsert.append(item_data)
                
                # Process meals
                for idx, meal in enumerate(meals):
                    if isinstance(meal, dict):
                        item_data = {
                            'id': str(uuid.uuid4()),
                            'itinerary_id': itinerary_id,
                            'day_number': day_number,
                            'activity_type': 'meal',
                            'title': f"{meal.get('meal_type', 'Meal').title()} at {meal.get('restaurant', 'Restaurant')}",
                            'description': f"{meal.get('cuisine', '')} cuisine",
                            'location': meal.get('location', ''),
                            'start_time': self._extract_time(meal.get('time')),
                            'end_time': None,
                            'cost': self._extract_cost(meal.get('estimated_cost')),
                            'notes': json.dumps(meal.get('specialties', [])) if meal.get('specialties') else None,
                            'created_at': datetime.now().isoformat()
                        }
                        items_to_upsert.append(item_data)
            
            if items_to_upsert:
                print(f"💾 Upserting {len(items_to_upsert)} itinerary items...")
                
                # Insert new items (we deleted existing ones above)
                result = self.supabase.table('itinerary_items').insert(items_to_upsert).execute()
                
                if result.data:
                    print(f"✅ {len(result.data)} itinerary items upserted successfully")
                else:
                    print("⚠️ No items data returned from upsert")
            else:
                print("⚠️ No items to upsert")
                    
        except Exception as e:
            print(f"❌ Error upserting itinerary items: {str(e)}")
    
    def save_itinerary(self, request_data, ai_response, user_id=None):
        """Legacy method - now uses upsert internally"""
        return self.upsert_itinerary(request_data, ai_response, user_id)
    
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
            
            # Enhance each itinerary with items
            for itinerary in result.data:
                try:
                    items_result = self.supabase.table('itinerary_items')\
                        .select('*')\
                        .eq('itinerary_id', itinerary['id'])\
                        .order('day_number', desc=False)\
                        .order('start_time', desc=False)\
                        .execute()
                    
                    if items_result.data:
                        itinerary['items'] = items_result.data
                        print(f"Added {len(items_result.data)} items to itinerary {itinerary['id']}")
                except Exception as e:
                    print(f"⚠️ Could not fetch items for itinerary {itinerary['id']}: {str(e)}")
            
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
            
            # Get related items
            try:
                items_result = self.supabase.table('itinerary_items')\
                    .select('*')\
                    .eq('itinerary_id', itinerary_id)\
                    .order('day_number', desc=False)\
                    .order('start_time', desc=False)\
                    .execute()
                
                if items_result.data:
                    itinerary['items'] = items_result.data
                    print(f"✅ Found {len(items_result.data)} related items")
            except Exception as e:
                print(f"⚠️ Could not fetch related items: {str(e)}")
            
            print(f"✅ Complete itinerary fetched successfully")
            return itinerary
            
        except Exception as e:
            print(f"❌ Error fetching itinerary: {str(e)}")
            return None
    
    def delete_itinerary(self, itinerary_id):
        """Delete itinerary and all related items"""
        try:
            print(f"🗑️ Deleting itinerary and related data: {itinerary_id}")
            
            # Delete related items first
            items_result = self.supabase.table('itinerary_items').delete().eq('itinerary_id', itinerary_id).execute()
            print(f"🗑️ Deleted {len(items_result.data) if items_result.data else 0} related items")
            
            # Delete main itinerary
            result = self.supabase.table('itineraries').delete().eq('id', itinerary_id).execute()
            
            if result.data:
                print(f"✅ Itinerary {itinerary_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No itinerary found with ID {itinerary_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting itinerary: {str(e)}")
            return False
    
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
            
            # Test itinerary_items table
            items_result = self.supabase.table('itinerary_items').select('id').limit(1).execute()
            print(f"✅ Itinerary items table accessible: {len(items_result.data)} records found")
            
            print("✅ Database connection test successful")
            return True
        except Exception as e:
            print(f"❌ Database connection test failed: {str(e)}")
            return False