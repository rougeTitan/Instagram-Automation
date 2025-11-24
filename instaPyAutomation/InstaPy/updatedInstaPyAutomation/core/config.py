"""
Configuration Management
===================================
Centralized configuration management for the Instagram automation bot.

This module:
- Loads all settings from .env file or environment variables
- Defines Instagram API credentials
- Sets safety limits to avoid detection
- Configures browser behavior and delays
- Manages file paths for data storage

IMPORTANT: Copy .env.example to .env and fill in your credentials before running!
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
# The .env file is in the updatedInstaPyAutomation directory (one level up)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)

# Debug: Warn if .env file not found
if not env_path.exists():
    print(f"Warning: .env file not found at {env_path}")
    print("Please copy .env.example to .env and add your Instagram credentials")


class Config:
    """
    Configuration class for Instagram bot
    
    This class stores all bot settings loaded from environment variables.
    All settings can be customized in the .env file.
    """
    
    # ==================== INSTAGRAM CREDENTIALS ====================
    # Your Instagram login credentials
    # REQUIRED: These must be set in .env file for the bot to work
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')
    
    # ==================== AI COMMENT GENERATION ====================
    # Optional AI-powered comment generation for more authentic engagement
    # Gemini API is FREE (1500 requests/day) - recommended!
    # OpenAI requires paid API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    USE_AI_COMMENTS = os.getenv('USE_AI_COMMENTS', 'False').lower() == 'true'
    AI_MODEL = os.getenv('AI_MODEL', 'gemini')  # 'gemini' (free) or 'openai' (paid)
    
    # ==================== SAFETY LIMITS ====================
    # These limits prevent Instagram from detecting automated behavior
    # Adjust these based on your account age and history
    # Newer accounts should use lower limits to avoid bans
    
    # Daily action limits (per 24 hours)
    MAX_LIKES_PER_DAY = int(os.getenv('MAX_LIKES_PER_DAY', 1000))
    MAX_FOLLOWS_PER_DAY = int(os.getenv('MAX_FOLLOWS_PER_DAY', 1000))
    MAX_COMMENTS_PER_DAY = int(os.getenv('MAX_COMMENTS_PER_DAY', 1000))
    MAX_UNFOLLOWS_PER_DAY = int(os.getenv('MAX_UNFOLLOWS_PER_DAY', 1000))
    
    # Hourly action limits - prevents rate limiting
    MAX_ACTIONS_PER_HOUR = int(os.getenv('MAX_ACTIONS_PER_HOUR', 1000))
    
    # ==================== TIMING SETTINGS ====================
    # Delays between actions - randomized to mimic human behavior
    # Longer delays = more human-like = safer from detection
    MIN_ACTION_DELAY = int(os.getenv('MIN_ACTION_DELAY', 3))  # Minimum seconds between actions
    MAX_ACTION_DELAY = int(os.getenv('MAX_ACTION_DELAY', 10))  # Maximum seconds between actions
    
    # Session breaks - longer pauses after every 10-15 actions
    # Mimics real users taking breaks to browse
    MIN_SESSION_BREAK = int(os.getenv('MIN_SESSION_BREAK', 300))  # 5 minutes
    MAX_SESSION_BREAK = int(os.getenv('MAX_SESSION_BREAK', 600))  # 10 minutes
    
    # ==================== BROWSER SETTINGS ====================
    # Configure Chrome browser behavior
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'  # Run without visible browser window (GCP/cloud deployment)
    WINDOW_SIZE = os.getenv('WINDOW_SIZE', '1920,1080')  # Browser window dimensions
    
    # ==================== INSTAGRAM URLS ====================
    # Instagram endpoints used by the bot
    BASE_URL = 'https://www.instagram.com'
    LOGIN_URL = f'{BASE_URL}/accounts/login/'  # Login page
    EXPLORE_TAGS_URL = f'{BASE_URL}/explore/tags/'  # Hashtag exploration
    
    # ==================== LOGGING ====================
    # Control console output and log files
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = 'instagram_bot.log'  # Log file name
    
    # ==================== DATA STORAGE ====================
    # Directories for persistent data (cookies, statistics, analytics)
    DATA_DIR = Path(__file__).parent.parent / 'data'  # data/ folder in project root
    COOKIES_FILE = DATA_DIR / 'cookies.json'  # Saved login session
    STATS_FILE = DATA_DIR / 'statistics.json'  # Action history
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.INSTAGRAM_USERNAME or not cls.INSTAGRAM_PASSWORD:
            raise ValueError(
                "Instagram credentials not found! "
                "Please copy .env.example to .env and add your credentials."
            )
        
        # Create data directory if it doesn't exist
        cls.DATA_DIR.mkdir(exist_ok=True)
        
        return True
