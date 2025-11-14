"""
Scheduled Instagram Automation
Runs at peak engagement times with 2 categories and 5 posts each
"""
import sys
import os
import random
from datetime import datetime
from colorama import Fore, Style, init

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser_setup import BrowserManager
from core.actions import InstagramActions
from core.safety import SafetyManager
from core.config import Config
from core.categories import POPULAR_CATEGORIES, get_primary_hashtag
from core.engagement_scheduler import EngagementScheduler

# Initialize colorama
init(autoreset=True)


def select_random_categories(count=2):
    """
    Select random categories from popular categories
    
    Args:
        count: Number of categories to select
        
    Returns:
        list: Selected category names
    """
    all_categories = list(POPULAR_CATEGORIES.keys())
    return random.sample(all_categories, min(count, len(all_categories)))


def run_scheduled_automation(categories_count=2, posts_per_category=5):
    """
    Run scheduled automation with selected categories
    
    Args:
        categories_count: Number of categories to process
        posts_per_category: Number of posts to process per category
    """
    
    # Get current time info
    now = datetime.now()
    day_name = now.strftime('%A')
    current_time = now.strftime('%I:%M %p')
    is_peak, _, peak_info = EngagementScheduler.is_peak_time_now(tolerance_minutes=60)
    
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"SCHEDULED INSTAGRAM AUTOMATION")
    print(f"{'=' * 80}{Style.RESET_ALL}")
    print(f"📅 Day: {day_name}")
    print(f"⏰ Time: {current_time}")
    if is_peak:
        print(f"🔥 Peak Time: {peak_info['reason']} ({peak_info['engagement_level'].replace('_', ' ').title()})")
    else:
        print(f"⚠️  Not peak time (running anyway)")
    print(f"\n📊 Configuration:")
    print(f"   Categories: {categories_count}")
    print(f"   Posts per category: {posts_per_category}")
    print(f"   Total posts: {categories_count * posts_per_category}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
    
    # Select random categories
    selected_categories = select_random_categories(categories_count)
    print(f"{Fore.YELLOW}🎲 Randomly selected categories:{Style.RESET_ALL}")
    for i, cat in enumerate(selected_categories, 1):
        cat_info = POPULAR_CATEGORIES[cat]
        print(f"   {i}. {cat.title()} - {cat_info['description']}")
        print(f"      Hashtag: #{get_primary_hashtag(cat)}")
        print(f"      Engagement: {cat_info['engagement_rate']}")
    print()
    
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
        print(f"\n{Fore.YELLOW}🔐 Logging in...{Style.RESET_ALL}")
        if not actions.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD):
            print(f"{Fore.RED}✗ Login failed{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}✓ Login successful{Style.RESET_ALL}\n")
        
        # Statistics
        total_processed = 0
        total_commented = 0
        total_liked = 0
        
        # Process each selected category
        for i, category in enumerate(selected_categories, 1):
            primary_hashtag = get_primary_hashtag(category)
            category_info = POPULAR_CATEGORIES[category]
            
            print(f"\n{Fore.CYAN}{'=' * 80}")
            print(f"CATEGORY {i}/{len(selected_categories)}: {category.upper()}")
            print(f"Description: {category_info['description']}")
            print(f"Primary Hashtag: #{primary_hashtag}")
            print(f"Target: {posts_per_category} posts")
            print(f"{'=' * 80}{Style.RESET_ALL}\n")
            
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
                print(f"{Fore.YELLOW}Post {j}/{len(posts)} in {category} (Overall: {total_processed}/{categories_count * posts_per_category}){Style.RESET_ALL}")
                print(f"{Fore.CYAN}─────────────────────────────────────────────{Style.RESET_ALL}")
                
                # Open post
                print(f"{Fore.YELLOW}→ Opening post...{Style.RESET_ALL}")
                if not actions.open_post(post):
                    print(f"{Fore.RED}✗ Failed to open post{Style.RESET_ALL}")
                    continue
                
                # COMMENT FIRST (required for Instagram's comment system)
                print(f"\n{Fore.YELLOW}💬 Step A: Adding AI-generated comment...{Style.RESET_ALL}")
                comment_success = actions.comment_on_post(
                    f"Great {category} content!",
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
            print(f"\n{Fore.CYAN}{'─' * 80}")
            print(f"Progress: {i}/{len(selected_categories)} categories completed")
            print(f"Posts: {total_processed}/{categories_count * posts_per_category} | Comments: {total_commented} | Likes: {total_liked}")
            print(f"{'─' * 80}{Style.RESET_ALL}\n")
        
        # Final summary
        print(f"\n{Fore.GREEN}{'=' * 80}")
        print(f"FINAL RESULTS")
        print(f"{'=' * 80}")
        print(f"Day: {day_name} at {current_time}")
        print(f"Categories processed: {len(selected_categories)}/{categories_count}")
        print(f"Total posts processed: {total_processed}/{categories_count * posts_per_category}")
        print(f"Comments posted: {total_commented}")
        print(f"Posts liked: {total_liked}")
        if total_processed > 0:
            print(f"Success rate: {(total_commented/total_processed*100):.1f}%")
        print(f"{'=' * 80}{Style.RESET_ALL}\n")
        
        # Next peak time info
        next_day, next_peak, next_datetime = EngagementScheduler.get_next_peak_time()
        if next_day:
            print(f"{Fore.CYAN}⏭️  Next scheduled run:{Style.RESET_ALL}")
            print(f"   {next_day} at {EngagementScheduler.format_time_12h(next_peak['hour'], next_peak['minute'])}")
            print(f"   {next_peak['reason']}")
            print()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Automation interrupted by user{Style.RESET_ALL}")
    
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
    import argparse
    
    parser = argparse.ArgumentParser(description='Run scheduled Instagram automation')
    parser.add_argument('--categories', type=int, default=2, 
                       help='Number of categories to process (default: 2)')
    parser.add_argument('--posts', type=int, default=5,
                       help='Number of posts per category (default: 5)')
    parser.add_argument('--show-schedule', action='store_true',
                       help='Show weekly schedule and exit')
    
    args = parser.parse_args()
    
    if args.show_schedule:
        # Just show the schedule
        EngagementScheduler.print_weekly_schedule()
        print("\nTo run automation: python scheduled_automation.py")
        print("To set categories: python scheduled_automation.py --categories 3")
        print("To set posts: python scheduled_automation.py --posts 10")
    else:
        # Run the automation
        run_scheduled_automation(
            categories_count=args.categories,
            posts_per_category=args.posts
        )
