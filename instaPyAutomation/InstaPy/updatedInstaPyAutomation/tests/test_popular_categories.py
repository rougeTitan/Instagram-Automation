"""
Test: Like and Comment on Posts from Top 10 Popular Categories
Uses AI to generate contextual comments based on image analysis
"""
import sys
import os
from colorama import Fore, Style, init

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser_setup import BrowserManager
from core.actions import InstagramActions
from core.safety import SafetyManager
from core.categories import POPULAR_CATEGORIES, get_primary_hashtag, print_categories_summary

# Initialize colorama
init(autoreset=True)


def test_popular_categories():
    """Test liking and commenting on posts from top 10 categories"""
    
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"TEST: AI Comment + Like on Top 10 Popular Categories")
    print(f"Categories: travel, fashion, fitness, food, beauty, photography,")
    print(f"           lifestyle, pets, motivation, luxury")
    print(f"Posts per category: 3")
    print(f"Total posts: 30")
    print(f"Sequence: Comment FIRST, then Like")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    browser_manager = None
    driver = None
    
    try:
        # Setup browser
        print(f"{Fore.YELLOW}🌐 Setting up Chrome browser...{Style.RESET_ALL}")
        browser_manager = BrowserManager()
        driver = browser_manager.setup_browser()
        print(f"{Fore.GREEN}✓ Browser initialized successfully{Style.RESET_ALL}")
        
        # Initialize safety and actions
        safety = SafetyManager()
        actions = InstagramActions(driver, safety, use_ai_comments=True)
        print(f"{Fore.GREEN}✓ AI comment generation enabled (using GEMINI){Style.RESET_ALL}")
        
        # Login
        print(f"\n{Fore.YELLOW}Step 1: Logging in...{Style.RESET_ALL}")
        from core.config import Config
        if not actions.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD):
            print(f"{Fore.RED}✗ Login failed{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}✓ Login successful{Style.RESET_ALL}\n")
        
        # Statistics
        total_processed = 0
        total_commented = 0
        total_liked = 0
        posts_per_category = 3
        
        # Process each category
        print(f"{Fore.CYAN}{'=' * 70}")
        print(f"Starting to process {len(POPULAR_CATEGORIES)} categories...")
        print(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        for i, category in enumerate(POPULAR_CATEGORIES.keys(), 1):
            primary_hashtag = get_primary_hashtag(category)
            category_info = POPULAR_CATEGORIES[category]
            
            print(f"\n{Fore.CYAN}{'=' * 70}")
            print(f"CATEGORY {i}/10: {category.upper()}")
            print(f"Description: {category_info['description']}")
            print(f"Primary Hashtag: #{primary_hashtag}")
            print(f"Target: {posts_per_category} posts")
            print(f"{'=' * 70}{Style.RESET_ALL}\n")
            
            # Search hashtag
            print(f"{Fore.YELLOW}→ Searching #{primary_hashtag}...{Style.RESET_ALL}")
            actions.search_hashtag(primary_hashtag)
            
            # Get posts
            print(f"{Fore.YELLOW}→ Getting posts...{Style.RESET_ALL}")
            posts = actions.get_posts(limit=posts_per_category)
            
            if not posts:
                print(f"{Fore.RED}✗ No posts found for #{primary_hashtag}{Style.RESET_ALL}")
                continue
            
            print(f"{Fore.GREEN}✓ Found {len(posts)} posts{Style.RESET_ALL}\n")
            
            # Process posts in this category
            for j, post in enumerate(posts, 1):
                total_processed += 1
                print(f"{Fore.CYAN}─────────────────────────────────────────────{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Post {j}/{len(posts)} in {category} (Overall: {total_processed}/30){Style.RESET_ALL}")
                print(f"{Fore.CYAN}─────────────────────────────────────────────{Style.RESET_ALL}")
                
                # Open post
                print(f"{Fore.YELLOW}→ Opening post...{Style.RESET_ALL}")
                if not actions.open_post(post):
                    print(f"{Fore.RED}✗ Failed to open post{Style.RESET_ALL}")
                    continue
                
                # COMMENT FIRST (required for Instagram's comment system)
                print(f"\n{Fore.YELLOW}💬 Step A: Adding AI-generated comment...{Style.RESET_ALL}")
                comment_success = actions.comment_on_post(
                    f"Amazing {category} content!",
                    use_ai=True
                )
                
                if comment_success:
                    total_commented += 1
                    print(f"{Fore.GREEN}✓ Comment posted ({total_commented} total){Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ Comment failed{Style.RESET_ALL}")
                
                # THEN LIKE
                print(f"\n{Fore.YELLOW}❤️  Step B: Liking post...{Style.RESET_ALL}")
                like_success = actions.like_post()
                
                if like_success:
                    total_liked += 1
                    print(f"{Fore.GREEN}✓ Post liked ({total_liked} total){Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ Like failed{Style.RESET_ALL}")
                
                # Close post
                actions.close_post()
                print(f"{Fore.GREEN}✓ Post closed{Style.RESET_ALL}\n")
            
            # Progress update
            print(f"\n{Fore.CYAN}{'─' * 70}")
            print(f"Progress: {i}/{len(POPULAR_CATEGORIES)} categories completed")
            print(f"Posts: {total_processed}/30 | Comments: {total_commented} | Likes: {total_liked}")
            print(f"{'─' * 70}{Style.RESET_ALL}\n")
        
        # Final summary
        print(f"\n{Fore.GREEN}{'=' * 70}")
        print(f"FINAL RESULTS")
        print(f"{'=' * 70}")
        print(f"Categories processed: {len(POPULAR_CATEGORIES)}/10")
        print(f"Total posts processed: {total_processed}/30")
        print(f"Comments posted: {total_commented}")
        print(f"Posts liked: {total_liked}")
        print(f"Success rate: {(total_commented/total_processed*100):.1f}%")
        print(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        # Keep browser open for verification
        print(f"{Fore.CYAN}Browser will stay open for 10 seconds for verification...{Style.RESET_ALL}")
        import time
        time.sleep(10)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Test interrupted by user{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if browser_manager and driver:
            print(f"\n{Fore.YELLOW}Cleaning up...{Style.RESET_ALL}")
            browser_manager.close_browser()
            print(f"{Fore.GREEN}✓ Browser closed{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✓ Done!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    # Show categories first
    print_categories_summary()
    print(f"\n{Fore.YELLOW}Press ENTER to start the test, or Ctrl+C to cancel...{Style.RESET_ALL}")
    input()
    
    test_popular_categories()
