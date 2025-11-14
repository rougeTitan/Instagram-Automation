"""
Test AI Comment Generation with Like Action
Tests both like and AI comment functionality on #car posts
"""
from browser_setup import BrowserManager
from actions import InstagramActions
from safety import SafetyManager
from config import Config
from colorama import init, Fore, Style
from selenium.webdriver.common.by import By

init(autoreset=True)

def test_ai_comments():
    print(f"\n{Fore.CYAN}{'='*60}")
    print("TEST: AI Comment + Like (#car)")
    print("Sequence: Comment FIRST, then Like")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    browser_manager = BrowserManager(headless=False)
    driver = browser_manager.setup_browser()
    safety = SafetyManager()
    safety.start_session()
    
    # Enable AI comments
    actions = InstagramActions(driver, safety, use_ai_comments=True)
    
    try:
        # Login
        print(f"{Fore.YELLOW}Step 1: Logging in...{Style.RESET_ALL}")
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
        
        # Process first 5 posts
        posts_to_process = posts[:5]
        print(f"{Fore.CYAN}{'='*60}")
        print(f"Step 4: Processing {len(posts_to_process)} Posts with AI Comments")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        for post_num, post in enumerate(posts_to_process, 1):
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"POST {post_num}/{len(posts_to_process)}")
            print(f"{'='*60}{Style.RESET_ALL}\n")
        
            # Check limits
            can_like = safety.can_perform_action('like')
            can_comment = safety.can_perform_action('comment')
            
            print(f"{Fore.YELLOW}Current Limits:{Style.RESET_ALL}")
            print(f"  • Can Like: {Fore.GREEN}YES{Style.RESET_ALL}" if can_like else f"  • Can Like: {Fore.RED}NO{Style.RESET_ALL}")
            print(f"  • Can Comment: {Fore.GREEN}YES{Style.RESET_ALL}" if can_comment else f"  • Can Comment: {Fore.RED}NO{Style.RESET_ALL}")
            print()
            
            # Open the post
            print(f"{Fore.YELLOW}→ Opening post {post_num}...{Style.RESET_ALL}")
            actions.human.human_click(post)
            print(f"⏳ Waiting for post to fully load...")
            actions.human.random_delay(5, 7)
            print(f"{Fore.GREEN}✓ Post opened{Style.RESET_ALL}\n")
        
            # Test COMMENT FIRST (before like) - Direct textarea approach with AI
            if can_comment:
                print(f"\n{Fore.YELLOW}→ Testing COMMENT functionality...{Style.RESET_ALL}")
                
                # Generate AI comment by analyzing the image
                comment_text = None
                if actions.use_ai_comments:
                    print(f"{Fore.CYAN}🤖 Analyzing image with AI...{Style.RESET_ALL}")
                    try:
                        comment_text = actions.ai_generator.generate_comment_for_post(driver)
                        if comment_text:
                            print(f"{Fore.GREEN}✓ AI Generated: {comment_text}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️  AI generation failed: {e}{Style.RESET_ALL}")
            
                # Fallback to simple comment if AI fails
                if not comment_text:
                    comment_text = "Nice car"
                    print(f"💬 Using fallback comment: {comment_text}")
                
                # Wait for page elements to stabilize
                print(f"⏳ Waiting for page to stabilize...")
                actions.human.random_delay(3, 5)
                
                # DIRECT APPROACH: Find and click textarea
                print(f"→ Finding textarea...")
                
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                # Find textarea using exact XPath with explicit wait
                textarea = None
                try:
                    print(f"→ Trying exact XPath...")
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…' and @placeholder='Add a comment…']"))
                    )
                    print(f"{Fore.GREEN}✓ Found textarea with exact XPath{Style.RESET_ALL}")
                except:
                    print(f"⚠️  Exact XPath failed, trying fallbacks...")
                    # Fallback selectors
                    selectors = [
                        (By.XPATH, "//textarea[@aria-label='Add a comment…']"),
                        (By.XPATH, "//textarea[@placeholder='Add a comment…']"),
                        (By.CSS_SELECTOR, 'textarea[placeholder*="Add a comment"]'),
                        (By.CSS_SELECTOR, 'textarea'),
                    ]
                    
                    for by, selector in selectors:
                        try:
                            textarea = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((by, selector))
                            )
                            print(f"{Fore.GREEN}✓ Found textarea with: {selector}{Style.RESET_ALL}")
                            break
                        except:
                            continue
                
                if not textarea:
                    print(f"{Fore.RED}✗ Textarea not found{Style.RESET_ALL}")
                    comment_typed = {'success': False, 'error': 'Textarea not found'}
                else:
                    # Type using JavaScript directly (skip element reference to avoid stale element)
                    print(f"→ Typing AI comment: '{comment_text}'")
                    
                    # First, try to type character by character using send_keys
                    type_result = driver.execute_script("""
                        var text = arguments[0];
                        
                        // Find textarea again to avoid stale element
                        var textarea = document.querySelector("textarea[aria-label='Add a comment…']") ||
                                      document.querySelector("textarea[placeholder='Add a comment…']") ||
                                      document.querySelector("textarea");
                        
                        if (!textarea) return {success: false, error: 'Textarea not found'};
                        
                        // Clear any existing text
                        textarea.value = '';
                        
                        // Focus and click multiple times to ensure it's active
                        textarea.focus();
                        textarea.click();
                        textarea.focus();
                        
                        return {success: true, element: true};
                    """, comment_text)
                    
                    if not type_result.get('success'):
                        raise Exception(type_result.get('error', 'Unknown error'))
                    
                    # Wait a moment for focus
                    actions.human.random_delay(1, 2)
                    
                    # Now try typing with Selenium send_keys
                    print(f"→ Typing with send_keys...")
                    textarea = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…' and @placeholder='Add a comment…']"))
                    )
                    textarea.send_keys(comment_text)
                    
                    # Verify it typed
                    type_result = driver.execute_script("""
                        var textarea = document.querySelector("textarea[aria-label='Add a comment…']") ||
                                      document.querySelector("textarea[placeholder='Add a comment…']");
                        return {success: true, value: textarea ? textarea.value : ''};
                    """)
                    
                    if not type_result.get('success'):
                        raise Exception(type_result.get('error', 'Unknown error'))
                    
                    print(f"✓ Typed: '{type_result['value']}'")
                    actions.human.random_delay(2, 3)
                    
                    # Submit by clicking Post button
                    print(f"→ Submitting comment...")
                    actions.human.random_delay(1, 2)
                    
                    # Look for the Post button that appears when text is entered
                    submit_result = driver.execute_script("""
                        // Find Post button - it should be enabled now that text is entered
                        var buttons = Array.from(document.querySelectorAll('div[role="button"]'));
                        var postBtn = buttons.find(btn => btn.innerText.trim() === 'Post');
                        
                        if (postBtn) {
                            postBtn.click();
                            return {success: true, method: 'Post button (div)'};
                        }
                        
                        // Try button element
                        buttons = Array.from(document.querySelectorAll('button'));
                        postBtn = buttons.find(btn => btn.innerText.trim() === 'Post');
                        
                        if (postBtn && !postBtn.disabled) {
                            postBtn.click();
                            return {success: true, method: 'Post button (button)'};
                        }
                        
                        return {success: false, error: 'Post button not found'};
                    """)
                    
                    print(f"✓ Submitted via {submit_result.get('method', 'unknown')}")
                    
                    # Wait for comment to actually post
                    actions.human.random_delay(3, 5)
                    
                    # Verify comment posted by checking if textarea is empty or comment appears
                    verify_result = driver.execute_script("""
                        var textarea = document.querySelector("textarea[aria-label='Add a comment…']");
                        if (textarea) {
                            return {
                                success: true,
                                textareaValue: textarea.value,
                                isEmpty: textarea.value === ''
                            };
                        }
                        return {success: false};
                    """)
                    
                    print(f"→ Verification: textarea value = '{verify_result.get('textareaValue', 'N/A')}'")
                    print(f"→ Textarea is empty: {verify_result.get('isEmpty', False)}")
                    
                    comment_typed = {
                        'success': verify_result.get('isEmpty', False),  # Success if textarea cleared
                        'value': comment_text,
                        'placeholder': 'Add a comment…'
                    }
                    
                except Exception as e:
                    print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
                    comment_typed = {'success': False, 'error': str(e)}
                
                if comment_typed.get('success'):
                    print(f"{Fore.GREEN}✓✓✓ COMMENT POSTED SUCCESSFULLY!{Style.RESET_ALL}")
                    print(f"  Placeholder: '{comment_typed.get('placeholder')}'")
                    print(f"  Comment: '{comment_typed.get('value')}'")
                    safety.record_action('comment', success=True)
                    actions.human.random_delay(3, 5)
                else:
                    print(f"{Fore.RED}✗ Comment failed: {comment_typed.get('error')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️  Skipping comment (limit reached){Style.RESET_ALL}")
            
            # NOW Test LIKE functionality (after comment)
            if can_like:
            print(f"\n{Fore.YELLOW}→ Testing LIKE action...{Style.RESET_ALL}")
            if actions.like_post(post_element=None):
                print(f"{Fore.GREEN}✓✓✓ POST LIKED SUCCESSFULLY!{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.YELLOW}⚠️  Like skipped (may already be liked){Style.RESET_ALL}\n")
                actions.human.random_delay(2, 4)
            else:
                print(f"{Fore.YELLOW}⚠️  Skipping like (limit reached){Style.RESET_ALL}\n")
            
            # Close this post and move to next
            if post_num < len(posts_to_process):
                print(f"{Fore.YELLOW}→ Closing post to move to next...{Style.RESET_ALL}")
                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys('\ue00c')  # ESC key
                    actions.human.random_delay(1, 2)
                except:
                    pass
        
        # Show final statistics
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Session Statistics")
        print(f"{'='*60}{Style.RESET_ALL}")
        safety.print_stats()
        
        print(f"\n{Fore.GREEN}✓✓✓ Completed processing {len(posts_to_process)} posts!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*60}")
        print("Test Complete - Browser will stay open for 10 seconds")
        print(f"{'='*60}{Style.RESET_ALL}")
        actions.human.random_delay(10, 10)
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    finally:
        input(f"\n{Fore.CYAN}Press ENTER to close browser...{Style.RESET_ALL}")
        browser_manager.close()
        print(f"{Fore.GREEN}✓ Done!{Style.RESET_ALL}")


if __name__ == "__main__":
    test_ai_comments()
