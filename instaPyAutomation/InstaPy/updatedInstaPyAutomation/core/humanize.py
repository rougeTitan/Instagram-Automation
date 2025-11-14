"""
Human-like Behavior Simulation
Adds randomness and natural patterns to actions
"""
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from .config import Config


class HumanBehavior:
    """Simulates human-like behavior in browser"""
    
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
    
    def random_delay(self, min_seconds=None, max_seconds=None):
        """Random delay between actions"""
        min_sec = min_seconds or Config.MIN_ACTION_DELAY
        max_sec = max_seconds or Config.MAX_ACTION_DELAY
        
        delay = random.uniform(min_sec, max_sec)
        print(f"⏳ Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def human_type(self, element, text, typing_speed='normal'):
        """Type text with human-like speed variations"""
        speeds = {
            'slow': (0.1, 0.3),
            'normal': (0.05, 0.15),
            'fast': (0.02, 0.08)
        }
        
        min_delay, max_delay = speeds.get(typing_speed, speeds['normal'])
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
    
    def human_scroll(self, scroll_pause_time=0.5, scrolls=3):
        """Scroll page with human-like patterns"""
        print("📜 Scrolling page...")
        
        for i in range(scrolls):
            # Random scroll amount
            scroll_amount = random.randint(300, 700)
            
            # Execute scroll
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Random pause
            time.sleep(random.uniform(scroll_pause_time, scroll_pause_time * 2))
            
            # Sometimes scroll back up a bit (human-like)
            if random.random() < 0.3:  # 30% chance
                scroll_back = random.randint(50, 150)
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_back});")
                time.sleep(random.uniform(0.2, 0.5))
    
    def mouse_move_to_element(self, element):
        """Move mouse to element before clicking"""
        try:
            # Move to element with offset for more natural movement
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            
            self.actions.move_to_element_with_offset(
                element, offset_x, offset_y
            ).perform()
            
            # Small pause after movement
            time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"✗ Mouse movement failed: {e}")
    
    def human_click(self, element):
        """Click element with human-like behavior"""
        try:
            # Move mouse to element first
            self.mouse_move_to_element(element)
            
            # Small delay before click
            time.sleep(random.uniform(0.1, 0.3))
            
            # Click
            element.click()
            
            # Small delay after click
            time.sleep(random.uniform(0.2, 0.5))
            
        except Exception as e:
            print(f"✗ Click failed: {e}")
            raise
    
    def random_page_interaction(self):
        """Perform random page interactions (more human-like)"""
        interaction_type = random.choice(['scroll', 'pause', 'small_scroll'])
        
        if interaction_type == 'scroll':
            self.human_scroll(scrolls=random.randint(1, 2))
        elif interaction_type == 'pause':
            time.sleep(random.uniform(1, 3))
        elif interaction_type == 'small_scroll':
            scroll_amount = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
    
    def session_break(self):
        """Take a longer break to simulate human session patterns"""
        break_time = random.uniform(
            Config.MIN_SESSION_BREAK,
            Config.MAX_SESSION_BREAK
        )
        
        minutes = break_time / 60
        print(f"☕ Taking a {minutes:.1f} minute break (human-like behavior)...")
        time.sleep(break_time)
    
    def should_take_break(self, actions_count):
        """Determine if bot should take a break"""
        # Take break after 10-20 actions
        break_threshold = random.randint(10, 20)
        return actions_count >= break_threshold and actions_count % break_threshold == 0
