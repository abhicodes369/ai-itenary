from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any

@dataclass
class ItineraryRequest:
    destination: str
    start_date: date
    end_date: date
    travelers: int
    min_budget: Optional[float]
    max_budget: Optional[float]
    vegetarian_preference: bool
    special_requirements: Optional[str]
    user_id: Optional[str] = None

@dataclass
class ItineraryResponse:
    id: str
    destination: str
    start_date: date
    end_date: date
    travelers: int
    min_budget: Optional[float]
    max_budget: Optional[float]
    vegetarian_preference: bool
    special_requirements: Optional[str]
    ai_generated_itinerary: Dict[Any, Any]
    created_at: str