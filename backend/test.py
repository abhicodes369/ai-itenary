# this file is to check the connection to database
from services.database import DatabaseService
from services.aiservice import AIService
from datetime import datetime
import uuid

def test_complete_flow():
    print("🧪 Testing complete database flow...")
    
    # Initialize services
    db_service = DatabaseService()
    ai_service = AIService()
    
    # Test connection
    if not db_service.test_connection():
        print("❌ Database connection failed")
        return
    
    # Test data
    test_request = {
        'destination': 'Goa',
        'start_date': '2025-07-01',
        'end_date': '2025-07-03',
        'travelers': 2,
        'budget': 10000,
        'isVegetarian': True,
        'special_requirements': 'Beach activities'
    }
    
    test_user_id = str(uuid.uuid4())
    # Insert user into users table
    db_service.supabase.table('users').insert({
        'id': test_user_id,
        'email': 'test@example.com'
    }).execute()
    
    # Generate and save itinerary
    print("🤖 Generating AI itinerary...")
    ai_response = ai_service.generate_itinerary(test_request)
    
    print("💾 Saving to database...")
    saved = db_service.save_itinerary(test_request, ai_response, test_user_id)
    
    if saved:
        print(f"✅ Test successful! Itinerary ID: {saved['id']}")
        
        # Test retrieval
        retrieved = db_service.get_itinerary_by_id(saved['id'])
        if retrieved:
            print("✅ Retrieval test successful!")
            print(f"Destination: {retrieved['destination']}")
            print(f"Activities stored: {len(retrieved.get('structured_activities', []))}")
        else:
            print("❌ Retrieval test failed")
    else:
        print("❌ Test failed - could not save itinerary")

if __name__ == "__main__":
    test_complete_flow()