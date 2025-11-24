"""
Browser Setup with Undetected ChromeDriver
Configures Chrome to avoid detection as automation
"""
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from pathlib import Path
from .config import Config


class BrowserManager:
    """Manages browser instance with stealth features"""
    
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.wait = None
        
    def setup_browser(self):
        """Initialize Chrome with undetected-chromedriver"""
        print("🌐 Setting up Chrome browser...")
        
        options = uc.ChromeOptions()
        
        # Stealth settings
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        
        # Window size and position (looks more human-like and fully visible)
        width, height = Config.WINDOW_SIZE.split(',')
        options.add_argument(f'--window-size={width},{height}')
        options.add_argument('--window-position=0,0')
        
        # User agent (real Chrome user agent)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable automation flags (commented out for compatibility)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        
        # Preferences
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        if self.headless:
            options.add_argument('--headless=new')
        
        try:
            # Initialize undetected Chrome
            self.driver = uc.Chrome(options=options, version_main=None)
            self.wait = WebDriverWait(self.driver, 10)

            # Maximize window to ensure all elements are visible
            self.driver.maximize_window()

            # Execute stealth scripts
            self.apply_stealth()

            print("✓ Browser initialized successfully")
            return self.driver
            
        except Exception as e:
            print(f"✗ Failed to initialize browser: {e}")
            raise
    
    def apply_stealth(self):
        """Apply additional stealth JavaScript"""
        if not self.driver:
            return
            
        # Override webdriver property
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        # Override plugins length
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        # Override languages
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
    
    def save_cookies(self):
        """Save cookies to file for session persistence"""
        if not self.driver:
            return
            
        try:
            cookies = self.driver.get_cookies()
            with open(Config.COOKIES_FILE, 'w') as f:
                json.dump(cookies, f, indent=2)
            print("✓ Cookies saved")
        except Exception as e:
            print(f"✗ Failed to save cookies: {e}")
    
    def load_cookies(self):
        """Load cookies from file"""
        if not self.driver:
            return False
            
        if not Config.COOKIES_FILE.exists():
            return False
            
        try:
            with open(Config.COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
            
            # Navigate to Instagram first
            self.driver.get(Config.BASE_URL)
            
            # Add cookies
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            print("✓ Cookies loaded")
            return True
        except Exception as e:
            print(f"✗ Failed to load cookies: {e}")
            return False
    
    def close(self):
        """Close browser and cleanup"""
        if self.driver:
            try:
                self.save_cookies()
                self.driver.quit()
                print("✓ Browser closed")
            except Exception as e:
                print(f"✗ Error closing browser: {e}")
