import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # AI service configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Flask configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL')  # Fallback for PostgreSQL
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'GROQ_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def print_config_status(cls):
        """Print configuration status for debugging"""
        print("📋 Configuration Status:")
        print(f"  SUPABASE_URL: {'✅ Set' if cls.SUPABASE_URL else '❌ Missing'}")
        print(f"  SUPABASE_KEY: {'✅ Set' if cls.SUPABASE_KEY else '❌ Missing'}")
        print(f"  GROQ_API_KEY: {'✅ Set' if cls.GROQ_API_KEY else '❌ Missing'}")
        print(f"  SECRET_KEY: {'✅ Set' if cls.SECRET_KEY else '❌ Missing'}")

# Validate configuration on import
try:
    Config.validate_config()
    print("✅ All required configuration variables are set")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set")