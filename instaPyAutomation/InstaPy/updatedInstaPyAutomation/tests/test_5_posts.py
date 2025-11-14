"""
Test AI Comments on 5 Posts from #car hashtag
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from colorama import Fore, Style, init
from core.browser_setup import BrowserManager
from core.actions import InstagramActions
from core.safety import SafetyManager
from core.config import Config
from selenium.webdriver.common.by import By

init(autoreset=True)

def test_5_posts():
    """Test AI commenting and liking on 5 car posts"""
    browser_manager = None
    
    try:
        print(f"{Fore.CYAN}{'='*60}")
        print("TEST: AI Comment + Like on 5 Posts (#car)")
        print("Sequence: Comment FIRST, then Like")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        # Setup
        browser_manager = BrowserManager()
        driver = browser_manager.setup_browser()
        print(f"{Fore.GREEN}✓ Browser initialized successfully{Style.RESET_ALL}")
        
        # Initialize safety and actions
        safety = SafetyManager()
        actions = InstagramActions(driver, safety, use_ai_comments=True)
        print(f"{Fore.GREEN}✓ AI comment generation enabled (using GEMINI){Style.RESET_ALL}")
        
        # Login
        print(f"{Fore.YELLOW}Step 1: Logging in...{Style.RESET_ALL}")
        from core.config import Config
        if not actions.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD):
            print(f"{Fore.RED}✗ Login failed{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}✓ Login successful{Style.RESET_ALL}\n")
        
        # Search hashtag
        print(f"{Fore.YELLOW}Step 2: Searching #car...{Style.RESET_ALL}")
        actions.search_hashtag('car')
        
        # Get posts
        print(f"{Fore.YELLOW}Step 3: Getting posts...{Style.RESET_ALL}")
        posts = actions.get_posts_from_page(max_posts=9)
        
        if not posts:
            print(f"{Fore.RED}✗ No posts found{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}✓ Found {len(posts)} posts{Style.RESET_ALL}\n")
        
        # Process 5 posts
        posts_to_process = posts[:5]
        print(f"{Fore.CYAN}{'='*60}")
        print(f"Processing {len(posts_to_process)} Posts")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        for i, post in enumerate(posts_to_process, 1):
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"POST {i}/{len(posts_to_process)}")
            print(f"{'='*60}{Style.RESET_ALL}\n")
            
            # Open post
            print(f"{Fore.YELLOW}→ Opening post {i}...{Style.RESET_ALL}")
            actions.human.human_click(post)
            actions.human.random_delay(5, 7)
            print(f"{Fore.GREEN}✓ Post opened{Style.RESET_ALL}\n")
            
            # COMMENT FIRST (must be before like!)
            can_comment = safety.can_perform_action('comment')
            if can_comment:
                print(f"{Fore.YELLOW}→ Adding AI comment...{Style.RESET_ALL}")
                if actions.comment_on_post():
                    print(f"{Fore.GREEN}✓ Comment posted!{Style.RESET_ALL}\n")
                else:
                    print(f"{Fore.YELLOW}⚠️  Comment skipped{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}⚠️  Comment limit reached{Style.RESET_ALL}\n")
            
            # LIKE SECOND
            can_like = safety.can_perform_action('like')
            if can_like:
                print(f"{Fore.YELLOW}→ Liking post...{Style.RESET_ALL}")
                if actions.like_post():
                    print(f"{Fore.GREEN}✓ Post liked!{Style.RESET_ALL}\n")
                else:
                    print(f"{Fore.YELLOW}⚠️  Like skipped{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}⚠️  Like limit reached{Style.RESET_ALL}\n")
            
            # Close post modal for next post
            if i < len(posts_to_process):
                print(f"{Fore.YELLOW}→ Moving to next post...{Style.RESET_ALL}")
                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys('\ue00c')  # ESC
                    actions.human.random_delay(1, 2)
                except:
                    pass
        
        # Final statistics
        print(f"\n{Fore.CYAN}{'='*60}")
        print("FINAL STATISTICS")
        print(f"{'='*60}{Style.RESET_ALL}")
        safety.print_stats()
        
        print(f"\n{Fore.GREEN}✓✓✓ Completed processing {len(posts_to_process)} posts!{Style.RESET_ALL}")
        actions.human.random_delay(10, 10)
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    finally:
        input(f"\n{Fore.CYAN}Press ENTER to close browser...{Style.RESET_ALL}")
        if browser_manager:
            browser_manager.close()
        print(f"{Fore.GREEN}✓ Done!{Style.RESET_ALL}")


if __name__ == "__main__":
    test_5_posts()
