# AI Itinerary Generator

An intelligent web application that helps users create personalized travel itineraries using AI technology. The application provides a seamless experience for planning trips with smart suggestions and automated itinerary generation.

## Features

- AI-powered itinerary generation
- User-friendly interface
- Real-time suggestions
- Customizable travel plans
- Secure user authentication
- Database integration for storing itineraries

## Tech Stack

### Backend

- Python 3.x
- Flask (Web Framework)
- Supabase (Database)
- Groq (AI Integration)
- PostgreSQL (Database)
- Gunicorn (WSGI Server)

### Frontend

- React.js
- Modern UI/UX design

## Project Structure

```
ai-itenary/
├── backend/
│   ├── app.py           # Main Flask application
│   ├── config.py        # Configuration settings
│   ├── models.py        # Database models
│   ├── services/        # Business logic services
│   └── requirements.txt # Python dependencies
└── client/
    └── my-project/      # React frontend application
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:

   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the client directory:

   ```bash
   cd client/my-project
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Documentation

The backend provides RESTful APIs for:

- User authentication
- Itinerary generation
- Trip management
- User preferences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please open an issue in the repository.

## User Flow

The following diagram illustrates the user flow of the application:

![User Flow](user-flow.png)

## Database Schema

The following diagram shows the database structure used in the project:

![Database Schema](database-schema.png)
