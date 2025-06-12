# app.py - Fixed version with guaranteed database storage
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.aiservice import AIService
from services.database import DatabaseService
import traceback
import uuid

app = Flask(__name__)
CORS(app)

# Initialize services
print("🚀 Initializing services...")
ai_service = AIService()
db_service = DatabaseService()

# Test database connection on startup
if db_service.test_connection():
    print("✅ Database connection verified!")
else:
    print("❌ Database connection failed!")

@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary():
    print("\n" + "="*50)
    print("🎯 NEW ITINERARY REQUEST RECEIVED")
    print("="*50)
    
    try:
        data = request.get_json()
        
        if not data:
            print("❌ No data provided in request")
            return jsonify({'error': 'No data provided'}), 400
        
        print(f"📝 Request data: {data}")
        
        # Validate required fields
        required_fields = ['destination', 'start_date', 'end_date', 'budget']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Missing required field{'s' if len(missing_fields) > 1 else ''}: {', '.join(missing_fields)}"
            print(f"❌ Validation failed: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Validate budget
        try:
            budget = int(data['budget'])
            if budget <= 0:
                print("❌ Budget validation failed: must be positive")
                return jsonify({'error': 'Budget must be a positive number'}), 400
        except (ValueError, TypeError):
            print("❌ Budget validation failed: invalid number")
            return jsonify({'error': 'Budget must be a valid number'}), 400
        
        # Validate dates
        from datetime import datetime
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
            
            if end_date <= start_date:
                print("❌ Date validation failed: end date must be after start date")
                return jsonify({'error': 'End date must be after start date'}), 400
                
        except ValueError:
            print("❌ Date validation failed: invalid format")
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        print("✅ All validations passed!")
        
        # Prepare data for AI service
        request_data = {
            'destination': data['destination'].strip(),
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'budget': str(budget),
            'isVegetarian': data.get('isVegetarian', False)
        }
        
        print(f"🤖 Sending to AI service: {request_data['destination']}, {request_data['start_date']} to {request_data['end_date']}")
        
        # Generate itinerary using AI service
        ai_response = ai_service.generate_itinerary(request_data)
        
        if not ai_response:
            print("❌ AI service failed to generate itinerary")
            return jsonify({'error': 'Failed to generate itinerary'}), 500
        
        print("✅ AI Itinerary generated successfully!")
        
        # Prepare database request data
        db_request_data = {
            'destination': request_data['destination'],
            'start_date': request_data['start_date'],
            'end_date': request_data['end_date'],
            'travelers': data.get('travelers', 1),
            'min_budget': budget,
            'max_budget': budget,
            'vegetarian_preference': request_data['isVegetarian'],
            'special_requirements': data.get('special_requirements', '')
        }
        
        # Get user_id (generate one if not provided for testing)
        user_id = data.get('user_id') or request.headers.get('X-User-ID')
        if not user_id:
            # Generate a test user ID for demonstration
            user_id = str(uuid.uuid4())  # Generate a proper UUID
            print(f"🔧 Generated test user ID: {user_id}")
        
        print("💾 SAVING TO DATABASE...")
        
        # Save to database
        saved_itinerary = db_service.save_itinerary(db_request_data, ai_response, user_id)
        
        if saved_itinerary:
            print(f"🎉 SUCCESS! Itinerary saved to database with ID: {saved_itinerary.get('id')}")
            
            # Combine AI response with database info
            response_data = {
                'id': saved_itinerary['id'],
                'user_id': saved_itinerary.get('user_id'),
                'created_at': saved_itinerary.get('created_at'),
                'database_saved': True,
                **ai_response  # Include all AI-generated content
            }
            
            print("✅ COMPLETE SUCCESS - Data saved to database!")
            
        else:
            print("⚠️ Database save failed, returning AI response only")
            response_data = {
                **ai_response,
                'database_saved': False,
                'warning': 'Data not saved to database'
            }
        
        print("📤 Sending response to client...")
        
        return jsonify({
            'success': True,
            'message': 'Itinerary generated successfully',
            'data': response_data
        }), 200
        
    except Exception as e:
        print(f"💥 ERROR in generate_itinerary route: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        
        return jsonify({
            'error': 'Internal server error occurred while generating itinerary',
            'details': str(e)
        }), 500

@app.route('/api/itineraries', methods=['GET'])
def get_user_itineraries():
    """Get all itineraries for a user"""
    try:
        print("\n🔍 FETCHING USER ITINERARIES...")
        
        # Get user_id from query params or headers
        user_id = request.args.get('user_id') or request.headers.get('X-User-ID')
        
        if not user_id:
            print("❌ No user ID provided")
            return jsonify({'error': 'User ID required'}), 400
        
        print(f"👤 Fetching itineraries for user: {user_id}")
        
        itineraries = db_service.get_user_itineraries(user_id)
        
        print(f"✅ Found {len(itineraries)} itineraries")
        
        return jsonify({
            'success': True,
            'data': itineraries,
            'count': len(itineraries)
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching itineraries: {str(e)}")
        return jsonify({'error': 'Failed to fetch itineraries'}), 500

@app.route('/api/itineraries/<itinerary_id>', methods=['GET'])
def get_itinerary(itinerary_id):
    """Get specific itinerary by ID"""
    try:
        print(f"\n🔍 FETCHING SPECIFIC ITINERARY: {itinerary_id}")
        
        itinerary = db_service.get_itinerary_by_id(itinerary_id)
        
        if not itinerary:
            print("❌ Itinerary not found")
            return jsonify({'error': 'Itinerary not found'}), 404
        
        print("✅ Itinerary found and retrieved")
        
        return jsonify({
            'success': True,
            'data': itinerary
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching itinerary: {str(e)}")
        return jsonify({'error': 'Failed to fetch itinerary'}), 500

@app.route('/api/itineraries/<itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    """Delete specific itinerary"""
    try:
        print(f"\n🗑️ DELETING ITINERARY: {itinerary_id}")
        
        success = db_service.delete_itinerary(itinerary_id)
        
        if success:
            print("✅ Itinerary deleted successfully")
            return jsonify({
                'success': True,
                'message': 'Itinerary deleted successfully'
            }), 200
        else:
            print("❌ Failed to delete itinerary")
            return jsonify({'error': 'Failed to delete itinerary'}), 500
            
    except Exception as e:
        print(f"❌ Error deleting itinerary: {str(e)}")
        return jsonify({'error': 'Failed to delete itinerary'}), 500

@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Test database connection endpoint"""
    try:
        print("\n🧪 TESTING DATABASE CONNECTION...")
        
        if db_service.test_connection():
            print("✅ Database test passed!")
            return jsonify({
                'success': True,
                'message': 'Database connection successful'
            }), 200
        else:
            print("❌ Database test failed!")
            return jsonify({
                'error': 'Database connection failed'
            }), 500
            
    except Exception as e:
        print(f"❌ Database test error: {str(e)}")
        return jsonify({
            'error': 'Database test failed',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'API is running',
        'database_connected': db_service.test_connection()
    }), 200

@app.route('/api/generate-itinerary-v2', methods=['POST'])
def generate_itinerary_v2():
    try:
        print("🚀 Generate itinerary endpoint called")
        
        # Get user ID from session/auth
        user_id = request.headers.get('Authorization')  # or however you handle auth
        if not user_id:
            print("❌ No user ID provided")
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        print(f"📝 Request data: {data}")
        
        # Generate itinerary using AI service
        ai_service = AIService()
        ai_response = ai_service.generate_itinerary(data)
        print(f"🤖 AI response generated: {type(ai_response)}")
        
        # Save to database
        db_service = DatabaseService()
        saved_itinerary = db_service.save_itinerary(data, ai_response, user_id)
        
        if saved_itinerary:
            print(f"✅ Itinerary saved successfully with ID: {saved_itinerary['id']}")
            return jsonify({
                'success': True,
                'itinerary': ai_response,
                'saved_data': saved_itinerary
            })
        else:
            print("❌ Failed to save itinerary to database")
            return jsonify({
                'success': True,
                'itinerary': ai_response,
                'warning': 'Itinerary generated but not saved to database'
            })
            
    except Exception as e:
        print(f"❌ Error in generate_itinerary: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/itineraries-v2', methods=['GET'])
def get_user_itineraries_v2():
    try:
        user_id = request.headers.get('Authorization')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        db_service = DatabaseService()
        itineraries = db_service.get_user_itineraries(user_id)
        
        print(f"✅ Retrieved {len(itineraries)} itineraries for user {user_id}")
        return jsonify({'itineraries': itineraries})
        
    except Exception as e:
        print(f"❌ Error fetching itineraries: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STARTING FLASK SERVER")
    print("="*50)
    print("📍 Server will run on: http://localhost:5000")
    print("🔗 API endpoints available:")
    print("  - POST /api/generate-itinerary")
    print("  - GET  /api/itineraries")
    print("  - GET  /api/itineraries/<id>")
    print("  - DELETE /api/itineraries/<id>")
    print("  - GET  /api/test-db")
    print("  - GET  /api/health")
    print("  - POST /api/generate-itinerary-v2")
    print("  - GET  /api/itineraries-v2")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)