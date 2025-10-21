"""Witty weather message generator."""
import random
from typing import Dict, List

# Weather messages organized by condition
WEATHER_MESSAGES: Dict[str, List[str]] = {
    "Rain": [
        "You'll regret not wearing a coat!",
        "Pack an umbrella unless you enjoy looking like a drowned rat",
        "Time to test if your shoes are really waterproof",
        "Mother Nature's way of saying 'stay inside'",
    ],
    "Clear": [
        "Time to blind everyone with your pale legs!",
        "Don't forget sunscreen unless you want to look like a lobster",
        "Perfect weather for pretending to be productive outside",
        "The sun is shining, no excuses to stay in bed",
    ],
    "Clouds": [
        "Perfect weather for brooding dramatically",
        "Nature's soft lighting - Instagram ready!",
        "Fifty shades of grey... in the sky",
        "The sky is being moody today",
    ],
    "Snow": [
        "Winter wonderland or frozen nightmare? You decide!",
        "Time to build a snowman or stay inside forever",
        "Let it snow, let it snow, let it... actually, please stop",
        "Mother Nature's way of saying 'cancel your plans'",
    ],
    "Thunderstorm": [
        "Thor is angry today",
        "Maybe stay inside and catch up on Netflix?",
        "Nature's fireworks display (from a safe distance)",
        "The universe is having a temper tantrum",
    ],
    "Drizzle": [
        "It's not really raining, but you'll still get wet",
        "Half-hearted rain for half-hearted plans",
        "Nature can't decide if it wants to rain or not",
        "Meh weather for meh days",
    ],
    "Mist": [
        "Mysterious vibes only",
        "Perfect weather for a dramatic entrance",
        "Nature's Instagram filter",
        "Can't see much, but make it fashion",
    ],
    "Hot": [
        "It's so hot, eggs are frying on the sidewalk",
        "Sweat is just your body crying",
        "Hell called, they want their weather back",
        "Surface of the sun called, it's jealous",
    ],
    "Cold": [
        "Colder than your ex's heart",
        "All the layers! ALL OF THEM!",
        "Penguins would complain about this weather",
        "Time to hibernate until spring",
    ],
    "Windy": [
        "Bad hair day guaranteed",
        "Your umbrella doesn't stand a chance",
        "Nature's blow dryer is on full blast",
        "Hold onto your hats... literally",
    ],
}


def get_witty_message(
    condition: str,
    temperature: float,
    wind_speed: float,
    units: str = "metric",
) -> str:
    """Get a witty weather message based on conditions.

    Args:
        condition: Main weather condition (e.g., 'Rain', 'Clear', 'Snow')
        temperature: Current temperature
        wind_speed: Wind speed
        units: Temperature units (metric or imperial)

    Returns:
        A humorous weather message
    """
    # Determine temperature thresholds based on units
    if units == "metric":
        hot_threshold = 30  # 30°C
        cold_threshold = 5  # 5°C
        windy_threshold = 10  # 10 m/s
    else:  # imperial
        hot_threshold = 86  # 86°F
        cold_threshold = 41  # 41°F
        windy_threshold = 22  # 22 mph (approximately 10 m/s)

    # Check for special conditions
    if temperature > hot_threshold:
        messages = WEATHER_MESSAGES.get("Hot", [])
    elif temperature < cold_threshold:
        messages = WEATHER_MESSAGES.get("Cold", [])
    elif wind_speed > windy_threshold:
        messages = WEATHER_MESSAGES.get("Windy", [])
    else:
        # Use condition-based messages
        # Map similar conditions
        condition_map = {
            "Rain": "Rain",
            "Clear": "Clear",
            "Clouds": "Clouds",
            "Snow": "Snow",
            "Thunderstorm": "Thunderstorm",
            "Drizzle": "Drizzle",
            "Mist": "Mist",
            "Fog": "Mist",
            "Haze": "Mist",
        }
        
        mapped_condition = condition_map.get(condition, "Clouds")
        messages = WEATHER_MESSAGES.get(mapped_condition, WEATHER_MESSAGES["Clouds"])

    # Return a random message from the appropriate list
    return random.choice(messages) if messages else "Weather is weather, what can you do? 🤷"