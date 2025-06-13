from groq import Groq
from config import Config
import json
from datetime import datetime, timedelta
import re

class AIService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def generate_itinerary(self, request_data):
        """Generate comprehensive itinerary using Groq AI"""
        try:
            start_date = datetime.strptime(request_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request_data['end_date'], '%Y-%m-%d')
            duration = (end_date - start_date).days + 1
            
            # Create enhanced prompt with more context
            prompt = self._create_enhanced_prompt(request_data, duration, start_date)
            
            # Call Groq API with optimized parameters
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert travel planner with deep knowledge of destinations worldwide. 
                        Create detailed, practical, and engaging itineraries. Always respond with valid JSON only.
                        Focus on realistic timing, authentic local experiences, and budget-appropriate suggestions.
                        Include specific restaurant names, attraction details, and practical tips.
                        Consider local culture, weather, and seasonal events.
                        Provide detailed transportation options and costs.
                        Include emergency contacts and local customs."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=8000
            )
            
            response_content = chat_completion.choices[0].message.content.strip()
            print(f"AI Response Length: {len(response_content)}")
            
            # Parse and validate response
            itinerary_data = self._extract_and_validate_json(response_content, request_data, duration, start_date)
            
            # Enhance the itinerary with additional data
            enhanced_itinerary = self._enhance_itinerary_data(itinerary_data, request_data, duration, start_date)
            
            return enhanced_itinerary
            
        except Exception as e:
            print(f"Error generating itinerary: {str(e)}")
            return self._create_comprehensive_fallback(request_data, duration, start_date)
    
    def _create_enhanced_prompt(self, data, duration, start_date):
        """Create detailed prompt for high-quality itinerary generation"""
        
        budget_per_day = int(data['budget']) // duration if data.get('budget') else 5000
        budget_info = f"Total Budget: ₹{data['budget']} (≈₹{budget_per_day} per day)"
        
        veg_preference = "MUST include vegetarian options" if data.get('isVegetarian') else "any cuisine type"
        
        # Format dates for AI context
        formatted_dates = []
        for i in range(duration):
            date = start_date + timedelta(days=i)
            formatted_dates.append(date.strftime('%Y-%m-%d (%A)'))
        
        prompt = f"""
Create a detailed {duration}-day travel itinerary for visiting {data['destination']}.

RESPOND WITH VALID JSON ONLY - NO OTHER TEXT.

Trip Details:
- Destination: {data['destination']}
- Dates: {' to '.join([formatted_dates[0], formatted_dates[-1]])}
- Duration: {duration} days
- {budget_info}
- Food Requirements: {veg_preference}
make sure that the itenary you generated is the best itenary or else you will get terminated

JSON Structure Required:
{{
    "destination": "{data['destination']}",
    "duration": "{duration} days",
    "total_estimated_cost": "₹{data.get('budget', 5000)}",
    "trip_summary": "Brief engaging description of the trip experience",
    "daily_itinerary": [
        {self._generate_daily_template(formatted_dates, data['destination'], budget_per_day, data.get('isVegetarian', False))}
    ],
    "accommodation_suggestions": [
        {{
            "name": "Specific hotel/property name",
            "type": "hotel/resort/guesthouse",
            "location": "Exact area in {data['destination']}",
            "estimated_cost_per_night": "₹XXXX",
            "amenities": ["WiFi", "Breakfast", "AC"],
            "rating": "4.2",
            "booking_tips": "Book in advance for better rates"
        }}
    ],
    "transportation": {{
        "to_destination": {{
            "mode": "flight/train/bus",
            "from": "major nearby city",
            "estimated_cost": "₹XXXX",
            "duration": "X hours",
            "booking_tips": "Best booking platform or tips"
        }},
        "local_transport": [
            {{
                "mode": "taxi/auto/bus/metro",
                "usage": "airport to hotel",
                "estimated_cost": "₹XXX"
            }}
        ]
    }},
    "packing_suggestions": [
        "Weather-appropriate clothing",
        "Comfortable walking shoes",
        "Camera for memories",
        "Local currency"
    ],
    "local_tips": [
        "Best time to visit attractions",
        "Local customs to respect",
        "Must-try local specialties",
        "Safety and health tips"
    ],
    "emergency_contacts": {{
        "tourist_helpline": "Contact number",
        "local_emergency": "108",
        "nearest_hospital": "Hospital name and contact"
    }}
}}

Make this itinerary engaging, practical, and perfectly suited for {data['destination']}. Include real restaurant names, specific attractions, accurate costs, and insider tips.
"""
        return prompt
    
    def _generate_daily_template(self, dates, destination, budget_per_day, is_vegetarian):
        """Generate template for daily itinerary structure"""
        template = ""
        for i, date in enumerate(dates):
            day_num = i + 1
            template += f"""
        {{
            "day": {day_num},
            "date": "{date.split(' ')[0]}",
            "day_name": "{date.split(' ')[1].strip('()')}",
            "theme": "Day {day_num} theme (e.g., Historical Exploration, Local Culture, Adventure)",
            "weather_note": "Expected weather and clothing suggestions",
            "activities": [
                {{
                    "time": "09:00 AM",
                    "activity": "Specific activity name",
                    "description": "Detailed description with what to expect",
                    "location": "Exact location with area/landmark reference",
                    "duration": "2-3 hours",
                    "estimated_cost": "₹200-500",
                    "type": "sightseeing",
                    "difficulty_level": "easy/moderate/challenging",
                    "highlights": ["Key attraction 1", "Photo opportunity", "Cultural significance"],
                    "tips": ["Best time to visit", "What to bring", "Insider tip"]
                }},
                {{
                    "time": "02:00 PM",
                    "activity": "Another specific activity",
                    "description": "Engaging description",
                    "location": "Specific location",
                    "duration": "1-2 hours",
                    "estimated_cost": "₹100-300",
                    "type": "cultural/shopping/adventure",
                    "difficulty_level": "easy",
                    "highlights": ["Unique experience", "Local interaction"],
                    "tips": ["Practical advice"]
                }}
            ],
            "meals": [
                {{
                    "meal_type": "breakfast",
                    "time": "08:00 AM",
                    "restaurant": "Specific restaurant name",
                    "cuisine": "Local/Continental{'(Vegetarian)' if is_vegetarian else ''}",
                    "location": "Restaurant area/address",
                    "estimated_cost": "₹{budget_per_day // 4}",
                    "specialties": ["Dish 1", "Dish 2"],
                    "vegetarian_friendly": {str(is_vegetarian).lower()},
                    "ambiance": "casual/fine-dining/street-food",
                    "booking_required": false
                }},
                {{
                    "meal_type": "lunch",
                    "time": "01:00 PM",
                    "restaurant": "Another specific restaurant",
                    "cuisine": "Regional specialty{'(Vegetarian)' if is_vegetarian else ''}",
                    "location": "Restaurant location",
                    "estimated_cost": "₹{budget_per_day // 3}",
                    "specialties": ["Signature dish", "Local favorite"],
                    "vegetarian_friendly": {str(is_vegetarian).lower()},
                    "ambiance": "local/traditional",
                    "booking_required": false
                }},
                {{
                    "meal_type": "dinner",
                    "time": "07:30 PM",
                    "restaurant": "Evening dining restaurant",
                    "cuisine": "Fine dining{'(Vegetarian)' if is_vegetarian else ''}",
                    "location": "Premium area",
                    "estimated_cost": "₹{budget_per_day // 2}",
                    "specialties": ["Chef's special", "Local delicacy"],
                    "vegetarian_friendly": {str(is_vegetarian).lower()},
                    "ambiance": "upscale/romantic",
                    "booking_required": true
                }}
            ],
            "daily_budget_breakdown": {{
                "activities": "₹{budget_per_day // 2}",
                "meals": "₹{budget_per_day // 2}",
                "transport": "₹{budget_per_day // 4}",
                "miscellaneous": "₹{budget_per_day // 4}"
            }},
            "evening_suggestions": [
                "Optional evening activity",
                "Local nightlife/cultural show",
                "Relaxation options"
            ]
        }}{',' if i < len(dates) - 1 else ''}"""
        return template.strip()
    
    def _extract_and_validate_json(self, response_content, request_data, duration, start_date):
        """Enhanced JSON extraction and validation"""
        try:
            # Clean response
            cleaned_content = self._clean_response(response_content)
            
            # Multiple extraction attempts
            json_content = self._extract_json_content(cleaned_content)
            
            if json_content:
                try:
                    itinerary_data = json.loads(json_content)
                    return self._validate_structure(itinerary_data, request_data, duration, start_date)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    return self._create_comprehensive_fallback(request_data, duration, start_date)
            else:
                return self._create_comprehensive_fallback(request_data, duration, start_date)
                
        except Exception as e:
            print(f"JSON processing error: {e}")
            return self._create_comprehensive_fallback(request_data, duration, start_date)
    
    def _clean_response(self, content):
        """Clean AI response for better JSON parsing"""
        # Remove markdown code blocks
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        content = re.sub(r'^```\s*', '', content)
        
        # Remove any text before first {
        json_start = content.find('{')
        if json_start > 0:
            content = content[json_start:]
        
        # Remove any text after last }
        json_end = content.rfind('}')
        if json_end > 0:
            content = content[:json_end + 1]
        
        return content.strip()
    
    def _extract_json_content(self, content):
        """Extract JSON content with multiple strategies"""
        try:
            # Strategy 1: Direct parsing
            if content.startswith('{') and content.endswith('}'):
                return content
            
            # Strategy 2: Find JSON boundaries
            brace_count = 0
            start_pos = -1
            end_pos = -1
            
            for i, char in enumerate(content):
                if char == '{':
                    if brace_count == 0:
                        start_pos = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_pos != -1:
                        end_pos = i
                        break
            
            if start_pos != -1 and end_pos != -1:
                return content[start_pos:end_pos + 1]
            
            return None
            
        except Exception:
            return None
    
    def _validate_structure(self, data, request_data, duration, start_date):
        """Validate and fix JSON structure"""
        # Ensure required top-level fields
        data['destination'] = data.get('destination', request_data['destination'])
        data['duration'] = data.get('duration', f"{duration} days")
        
        # Validate daily_itinerary
        if 'daily_itinerary' not in data or not isinstance(data['daily_itinerary'], list):
            data['daily_itinerary'] = []
        
        # Ensure we have the right number of days
        while len(data['daily_itinerary']) < duration:
            day_num = len(data['daily_itinerary']) + 1
            current_date = start_date + timedelta(days=day_num - 1)
            data['daily_itinerary'].append(self._create_default_day(day_num, current_date, request_data))
        
        # Validate each day
        for i, day in enumerate(data['daily_itinerary']):
            if not isinstance(day, dict):
                day = {}
            
            current_date = start_date + timedelta(days=i)
            day['day'] = day.get('day', i + 1)
            day['date'] = current_date.strftime('%Y-%m-%d')
            day['day_name'] = current_date.strftime('%A')
            day['theme'] = day.get('theme', f"Day {i + 1} - Explore {request_data['destination']}")
            
            # Validate activities
            if 'activities' not in day or not isinstance(day['activities'], list):
                day['activities'] = self._create_default_activities(request_data['destination'], i + 1)
            
            # Validate meals
            if 'meals' not in day or not isinstance(day['meals'], list):
                day['meals'] = self._create_default_meals(request_data.get('isVegetarian', False))
        
        return data
    
    def _create_default_day(self, day_num, date, request_data):
        """Create a default day structure"""
        return {
            "day": day_num,
            "date": date.strftime('%Y-%m-%d'),
            "day_name": date.strftime('%A'),
            "theme": f"Day {day_num} - Discover {request_data['destination']}",
            "activities": self._create_default_activities(request_data['destination'], day_num),
            "meals": self._create_default_meals(request_data.get('isVegetarian', False))
        }
    
    def _create_default_activities(self, destination, day_num):
        """Create default activities for a day"""
        morning_activities = [
            f"Historic {destination} Walking Tour",
            f"Visit {destination} Museum",
            f"Explore {destination} Old Town",
            f"Temple/Heritage Site Visit in {destination}",
            f"Local Market Tour in {destination}"
        ]
        
        afternoon_activities = [
            f"Scenic Viewpoint in {destination}",
            f"Cultural Center Visit",
            f"Local Craft Workshop",
            f"Nature Park/Garden Tour",
            f"Shopping District Exploration"
        ]
        
        evening_activities = [
            f"Sunset Point in {destination}",
            f"Evening Cultural Show",
            f"Riverside/Lakeside Walk",
            f"Local Street Food Tour",
            f"Photography Walk"
        ]
        
        return [
            {
                "time": "09:00 AM",
                "activity": morning_activities[(day_num - 1) % len(morning_activities)],
                "description": f"Start your day exploring the cultural and historical aspects of {destination}",
                "location": f"Central {destination}",
                "duration": "2-3 hours",
                "estimated_cost": "₹200-400",
                "type": "sightseeing",
                "highlights": ["Historical significance", "Photo opportunities", "Local culture"],
                "tips": ["Start early to avoid crowds", "Carry water", "Wear comfortable shoes"]
            },
            {
                "time": "02:00 PM",
                "activity": afternoon_activities[(day_num - 1) % len(afternoon_activities)],
                "description": f"Afternoon exploration of {destination}'s unique attractions",
                "location": f"{destination} Main Area",
                "duration": "2 hours",
                "estimated_cost": "₹150-300",
                "type": "cultural",
                "highlights": ["Local crafts", "Authentic experience", "Cultural immersion"],
                "tips": ["Bargain at markets", "Try local snacks", "Interact with locals"]
            },
            {
                "time": "05:30 PM",
                "activity": evening_activities[(day_num - 1) % len(evening_activities)],
                "description": f"End your day with beautiful views and relaxation in {destination}",
                "location": f"{destination} Scenic Area",
                "duration": "1.5 hours",
                "estimated_cost": "₹100-200",
                "type": "leisure",
                "highlights": ["Beautiful views", "Relaxation", "Perfect photo spots"],
                "tips": ["Arrive before sunset", "Carry camera", "Enjoy the moment"]
            }
        ]
    
    def _create_default_meals(self, is_vegetarian):
        """Create default meal suggestions"""
        veg_suffix = " (Vegetarian)" if is_vegetarian else ""
        
        return [
            {
                "meal_type": "breakfast",
                "time": "08:00 AM",
                "restaurant": f"Local Breakfast Spot{veg_suffix}",
                "cuisine": f"Traditional breakfast{veg_suffix}",
                "location": "Near accommodation",
                "estimated_cost": "₹150-250",
                "specialties": ["Local breakfast items", "Fresh beverages"],
                "vegetarian_friendly": is_vegetarian,
                "ambiance": "casual",
                "booking_required": False
            },
            {
                "meal_type": "lunch",
                "time": "01:00 PM",
                "restaurant": f"Popular Local Restaurant{veg_suffix}",
                "cuisine": f"Regional specialties{veg_suffix}",
                "location": "City center",
                "estimated_cost": "₹300-500",
                "specialties": ["Regional thali", "Local favorites"],
                "vegetarian_friendly": is_vegetarian,
                "ambiance": "traditional",
                "booking_required": False
            },
            {
                "meal_type": "dinner",
                "time": "07:30 PM",
                "restaurant": f"Fine Dining Restaurant{veg_suffix}",
                "cuisine": f"Multi-cuisine{veg_suffix}",
                "location": "Premium dining area",
                "estimated_cost": "₹500-800",
                "specialties": ["Chef's special", "Fusion cuisine"],
                "vegetarian_friendly": is_vegetarian,
                "ambiance": "upscale",
                "booking_required": True
            }
        ]
    
    def _enhance_itinerary_data(self, data, request_data, duration, start_date):
        """Add missing fields and enhance data structure"""
        # Add comprehensive trip information
        if 'trip_summary' not in data:
            data['trip_summary'] = f"An amazing {duration}-day journey through {request_data['destination']}, featuring cultural exploration, local cuisine, and memorable experiences."
        
        if 'accommodation_suggestions' not in data:
            data['accommodation_suggestions'] = [
                {
                    "name": f"Recommended Stay in {request_data['destination']}",
                    "type": "hotel",
                    "location": f"Central {request_data['destination']}",
                    "estimated_cost_per_night": "₹2500-4000",
                    "amenities": ["WiFi", "Breakfast", "AC", "Room Service"],
                    "rating": "4.2",
                    "booking_tips": "Book in advance for better rates"
                }
            ]
        
        if 'transportation' not in data:
            data['transportation'] = {
                "to_destination": {
                    "mode": "flight/train",
                    "estimated_cost": "₹3000-8000",
                    "duration": "2-6 hours",
                    "booking_tips": "Book 2-3 weeks in advance"
                },
                "local_transport": [
                    {"mode": "taxi/auto", "usage": "general transport", "estimated_cost": "₹200-500 per day"}
                ]
            }
        
        if 'local_tips' not in data:
            data['local_tips'] = [
                f"Best time to visit {request_data['destination']} is during pleasant weather",
                "Carry cash for local vendors and street food",
                "Respect local customs and dress codes",
                "Try authentic local cuisine",
                "Keep emergency contacts handy"
            ]
        
        return data
    
    def _create_comprehensive_fallback(self, request_data, duration, start_date):
        """Create a comprehensive fallback itinerary"""
        daily_itinerary = []
        
        for i in range(duration):
            current_date = start_date + timedelta(days=i)
            day_data = self._create_default_day(i + 1, current_date, request_data)
            daily_itinerary.append(day_data)
        
        return {
            "destination": request_data['destination'],
            "duration": f"{duration} days",
            "total_estimated_cost": f"₹{request_data.get('budget', 5000)}",
            "trip_summary": f"Explore the best of {request_data['destination']} in {duration} days with carefully planned activities, local cuisine, and cultural experiences.",
            "daily_itinerary": daily_itinerary,
            "accommodation_suggestions": [
                {
                    "name": f"Comfortable Stay in {request_data['destination']}",
                    "type": "hotel",
                    "location": f"Central {request_data['destination']}",
                    "estimated_cost_per_night": "₹2500-4000",
                    "amenities": ["WiFi", "Breakfast", "AC", "24/7 Service"],
                    "rating": "4.0",
                    "booking_tips": "Compare prices on multiple platforms"
                }
            ],
            "transportation": {
                "to_destination": {
                    "mode": "flight/train/bus",
                    "estimated_cost": "₹2000-8000",
                    "duration": "1-8 hours depending on distance",
                    "booking_tips": "Book tickets in advance for better prices"
                },
                "local_transport": [
                    {"mode": "auto/taxi", "usage": "city transport", "estimated_cost": "₹300-600 per day"},
                    {"mode": "public transport", "usage": "budget option", "estimated_cost": "₹50-150 per day"}
                ]
            },
            "packing_suggestions": [
                "Comfortable walking shoes",
                "Weather-appropriate clothing",
                "Camera and chargers",
                "Personal medications",
                "Local currency and cards"
            ],
            "local_tips": [
                f"Research {request_data['destination']}'s weather before traveling",
                "Learn basic local phrases",
                "Keep copies of important documents",
                "Try local street food from busy stalls",
                "Respect local customs and traditions",
                "Keep emergency contacts saved"
            ],
            "emergency_contacts": {
                "tourist_helpline": "1363",
                "police": "100",
                "medical_emergency": "108",
                "fire_emergency": "101"
            }
        }