"""
Modern Instagram Automation Bot
Main entry point for the application
"""
import sys
from colorama import init, Fore, Style
from core.config import Config
from core.browser_setup import BrowserManager
from core.actions import InstagramActions
from core.safety import SafetyManager

# Initialize colorama for colored output
init(autoreset=True)


def print_banner():
    """Print welcome banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         MODERN INSTAGRAM AUTOMATION BOT                  ║
║         Safe, Stealth, Human-like                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_warning():
    """Print safety warning"""
    warning = f"""
{Fore.YELLOW}⚠️  WARNING ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This bot automates Instagram actions which violates Instagram's ToS.

RISKS:
  • Account suspension or permanent ban
  • Temporary action blocks
  • Shadowban (reduced visibility)
  
RECOMMENDATIONS:
  • Use a test account first
  • Start with very low limits (5-10 actions/day)
  • Never use on important accounts
  
Built-in Safety Features:
  ✓ Rate limiting (max 40 likes/day by default)
  ✓ Human-like delays and patterns
  ✓ Undetected Chrome driver
  ✓ Session breaks every 10-20 actions

USE AT YOUR OWN RISK!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
"""
    print(warning)
    
    response = input(f"\n{Fore.CYAN}Do you accept the risks and want to continue? (yes/no): {Style.RESET_ALL}")
    return response.lower() in ['yes', 'y']


def main():
    """Main function"""
    print_banner()
    
    try:
        # Validate configuration
        Config.validate()
    except ValueError as e:
        print(f"\n{Fore.RED}✗ Configuration Error: {e}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your Instagram credentials")
        print(f"3. Run the bot again{Style.RESET_ALL}\n")
        return
    
    # Show warning
    if not print_warning():
        print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}✓ Starting bot...{Style.RESET_ALL}\n")
    
    # Initialize components
    browser_manager = None
    
    try:
        # Setup browser
        browser_manager = BrowserManager(headless=Config.HEADLESS)
        driver = browser_manager.setup_browser()
        
        # Initialize safety manager
        safety = SafetyManager()
        safety.start_session()
        
        # Initialize actions with AI comments (set to False if you don't want AI)
        use_ai = Config.USE_AI_COMMENTS if hasattr(Config, 'USE_AI_COMMENTS') else False
        actions = InstagramActions(driver, safety, use_ai_comments=use_ai)
        
        # Always perform fresh login for now (cookies disabled for testing)
        print(f"\n{Fore.CYAN}{'='*60}")
        print("STEP 1: LOGIN")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        success = actions.login(
            Config.INSTAGRAM_USERNAME,
            Config.INSTAGRAM_PASSWORD
        )
        
        if not success:
            print(f"\n{Fore.RED}✗ Login failed. Please check your credentials.{Style.RESET_ALL}")
            return
        
        # Main automation
        print(f"\n{Fore.CYAN}{'='*60}")
        print("STEP 2: AUTOMATION")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        # Configuration
        hashtags = ['travel', 'nature', 'photography']
        posts_per_hashtag = 5
        comment_percentage = 30  # Comment on 30% of liked posts
        
        print(f"{Fore.CYAN}Configuration:")
        print(f"  • Hashtags: {', '.join('#' + h for h in hashtags)}")
        print(f"  • Posts per hashtag: {posts_per_hashtag}")
        print(f"  • Comment rate: {comment_percentage}%")
        if use_ai:
            print(f"  • AI Comments: {Fore.GREEN}ENABLED ✓{Style.RESET_ALL}")
        else:
            print(f"  • AI Comments: {Fore.YELLOW}DISABLED{Style.RESET_ALL}")
        print()
        
        import random
        from analytics import InstagramAnalytics
        analytics = InstagramAnalytics()
        
        for hashtag in hashtags:
            print(f"\n{Fore.MAGENTA}━━━ Processing #{hashtag} ━━━{Style.RESET_ALL}")
            
            # Search hashtag
            if not actions.search_hashtag(hashtag):
                print(f"{Fore.YELLOW}⚠️  Could not search hashtag, skipping{Style.RESET_ALL}")
                continue
            
            # Get posts
            posts = actions.get_posts_from_page(max_posts=posts_per_hashtag * 2)
            if not posts:
                print(f"{Fore.YELLOW}⚠️  No posts found, moving to next hashtag{Style.RESET_ALL}")
                continue
            
            processed = 0
            for i, post in enumerate(posts):
                if processed >= posts_per_hashtag:
                    break
                
                if not safety.can_perform_action('like'):
                    print(f"\n{Fore.YELLOW}⚠️  Daily like limit reached. Stopping.{Style.RESET_ALL}")
                    break
                
                print(f"\n  📸 Post {processed + 1}/{posts_per_hashtag}")
                
                # Open post first (don't pass to like_post, we'll handle it)
                print(f"  → Opening post...")
                actions.human.human_click(post)
                actions.human.random_delay(3, 5)
                
                # Like the post (already open, so pass None)
                if actions.like_post(post_element=None):
                    processed += 1
                    analytics.record_action('like', {'hashtag': hashtag})
                    
                    # Decide if we should comment
                    should_comment = random.randint(0, 100) <= comment_percentage
                    
                    if should_comment and safety.can_perform_action('comment'):
                        print(f"  💬 Commenting on this post...")
                        
                        # Post is already open, AI will analyze and comment
                        # comment_text=None means use AI if enabled
                        if actions.comment_on_post(comment_text=None, post_element=None):
                            analytics.record_action('comment', {
                                'hashtag': hashtag,
                                'ai_generated': use_ai
                            })
                        else:
                            print(f"  {Fore.YELLOW}⚠️  Comment skipped{Style.RESET_ALL}")
                    
                    # Close post modal
                    actions.close_post_modal()
                    
                    # Human-like delay
                    actions.human.random_delay(3, 7)
                else:
                    # Failed to like, close and continue
                    actions.close_post_modal()
                    actions.human.random_delay(2, 4)
            
            print(f"\n{Fore.GREEN}✓ Completed #{hashtag}: {processed} posts processed{Style.RESET_ALL}")
            
            # Check if we should continue to next hashtag
            if not safety.can_perform_action('like'):
                print(f"\n{Fore.YELLOW}⚠️  Daily limit reached. Stopping automation.{Style.RESET_ALL}")
                break
        
        # Show final statistics
        print(f"\n{Fore.CYAN}{'='*60}")
        print("SESSION COMPLETE")
        print(f"{'='*60}{Style.RESET_ALL}")
        safety.print_stats()
        
        input(f"\n{Fore.CYAN}Press ENTER to close browser...{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Bot stopped by user (Ctrl+C){Style.RESET_ALL}")
    
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if browser_manager:
            browser_manager.close()
        
        print(f"\n{Fore.GREEN}✓ Session ended. Goodbye!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
