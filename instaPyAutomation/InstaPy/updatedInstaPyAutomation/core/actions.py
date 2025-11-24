"""
Instagram Actions
Core functionality for liking, commenting, following, etc.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
from .humanize import HumanBehavior
from .safety import SafetyManager
from .config import Config
from .ai_comments import AICommentGenerator


class InstagramActions:
    """Instagram action handlers"""
    
    def __init__(self, driver, safety_manager, use_ai_comments=False):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.human = HumanBehavior(driver)
        self.safety = safety_manager
        self.use_ai_comments = use_ai_comments
        
        # Initialize AI comment generator if enabled
        if self.use_ai_comments:
            try:
                # Use model from config (defaults to 'gemini' which is FREE!)
                ai_model = Config.AI_MODEL if hasattr(Config, 'AI_MODEL') else 'gemini'
                self.ai_generator = AICommentGenerator(model=ai_model)
                print(f"✓ AI comment generation enabled (using {ai_model.upper()})")
            except Exception as e:
                print(f"⚠️  Could not initialize AI comments: {e}")
                self.use_ai_comments = False
    
    def login(self, username, password, max_retries=3):
        """Login to Instagram with retry logic"""
        for attempt in range(1, max_retries + 1):
            print(f"🔐 Logging in as {username}... (Attempt {attempt}/{max_retries})")
            try:
                self.driver.get(Config.LOGIN_URL)
                print("→ Waiting for page to load...")
                self.human.random_delay(3, 5)

                # Find username field
                print("→ Finding username field...")

                username_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )

                # Type username with human-like speed
                print("→ Typing username...")
                username_input.clear()
                self.human.human_type(username_input, username, 'normal')
                self.human.random_delay(1, 2)

                # Type password
                print("→ Typing password...")
                password_input = self.driver.find_element(By.NAME, "password")
                password_input.clear()
                self.human.human_type(password_input, password, 'normal')
                self.human.random_delay(2, 3)

                # Wait for login button to be enabled - try multiple selectors
                print("→ Waiting for login button...")
                login_button = None
                button_selectors = [
                    "//button[@type='submit']",
                    "//button[contains(text(), 'Log in')]",
                    "//button[contains(text(), 'Log In')]",
                    "//*[@id='loginForm']//button",
                    "//div[contains(@class, 'x9f619')]//button[@type='submit']"
                ]

                for selector in button_selectors:
                    try:
                        login_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"✓ Found login button with selector: {selector}")
                        break
                    except:
                        continue

                if not login_button:
                    print("✗ Could not find login button")
                    continue

                self.human.random_delay(1, 2)

                # Click login button
                print("→ Clicking login button...")
                try:
                    login_button.click()
                except:
                    # Fallback: use JavaScript click
                    print("→ Using JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", login_button)

                # Wait for login to complete
                print("→ Waiting for login to complete...")
                self.human.random_delay(5, 8)

                # Check if we're logged in
                current_url = self.driver.current_url
                if 'login' in current_url.lower():
                    print("✗ Still on login page - credentials may be incorrect")
                    continue

                # Dismiss all dialogs (Save Login, Notifications, etc.)
                print("→ Handling post-login dialogs...")
                self.human.random_delay(2, 3)

                # Try multiple times to catch all dialogs
                for i in range(3):
                    self.dismiss_all_dialogs()
                    self.human.random_delay(1, 2)

                print("✓ Login successful")
                return True
            except Exception as e:
                print(f"✗ Login attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    print("↻ Retrying login...")
                self.human.random_delay(2, 4)
                continue
        print(f"✗ All login attempts failed after {max_retries} retries.")
        return False
    
    def handle_save_login_prompt(self):
        """Handle 'Save Your Login Info' prompt"""
        selectors = [
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'Not Now')]",
            "//button[contains(text(), 'not now')]",
            "//div[contains(text(), 'Not Now')]",
            "//*[contains(@class, '_acan')]//button",
        ]
        
        for selector in selectors:
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                not_now_button.click()
                print("✓ Dismissed save login prompt")
                self.human.random_delay(1, 2)
                return True
            except TimeoutException:
                continue
        return False
    
    def handle_notifications_prompt(self):
        """Handle 'Turn on Notifications' prompt"""
        selectors = [
            "//button[contains(text(), 'Not Now')]",
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'NOT NOW')]",
            "//button[text()='Not Now']",
            "//*[contains(@role, 'button')][contains(text(), 'Not Now')]",
        ]
        
        for selector in selectors:
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                not_now_button.click()
                print("✓ Dismissed notifications prompt")
                self.human.random_delay(1, 2)
                return True
            except TimeoutException:
                continue
        return False
    
    def dismiss_all_dialogs(self):
        """Dismiss all common Instagram dialogs/popups"""
        print("→ Checking for dialogs...")
        
        # List of common dialog dismissal buttons
        dialog_selectors = [
            "//button[contains(text(), 'Not Now')]",
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'Dismiss')]",
            "//button[contains(text(), 'Cancel')]",
            "//button[contains(text(), 'Skip')]",
            "//button[@aria-label='Close']",
            "//*[name()='svg'][@aria-label='Close']/..",
            "//button[contains(@class, 'aOOlW')]",  # Common close button class
        ]
        
        dismissed_count = 0
        for selector in dialog_selectors:
            try:
                # Short wait for each dialog
                buttons = self.driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    try:
                        if button.is_displayed():
                            button.click()
                            dismissed_count += 1
                            print(f"✓ Dismissed dialog ({dismissed_count})")
                            self.human.random_delay(0.5, 1)
                    except:
                        continue
            except:
                continue
        
        if dismissed_count > 0:
            print(f"✓ Dismissed {dismissed_count} dialog(s)")
        
        return dismissed_count > 0
    
    def search_hashtag(self, hashtag):
        """Navigate to hashtag page"""
        print(f"🔍 Searching for #{hashtag}...")
        
        # Remove # if provided
        hashtag = hashtag.lstrip('#')
        
        url = f"{Config.EXPLORE_TAGS_URL}{hashtag}/"
        self.driver.get(url)
        self.human.random_delay(3, 5)
        
        # Dismiss any dialogs that might appear
        self.dismiss_all_dialogs()
        
        # Scroll to load posts
        self.human.human_scroll(scrolls=2)
        
        return True
    
    def get_posts_from_page(self, max_posts=9):
        """Get post elements from current page"""
        try:
            # Try multiple XPath selectors for posts
            selectors = [
                "//article//a[contains(@href, '/p/')]",
                "//a[contains(@href, '/p/')]",
                "//div[contains(@class, '_aagw')]//a",
                "//div[@role='button']//a[contains(@href, '/p/')]"
            ]
            
            posts = []
            for selector in selectors:
                try:
                    found_posts = self.driver.find_elements(By.XPATH, selector)
                    if found_posts:
                        posts = found_posts
                        break
                except:
                    continue
            
            # Limit number of posts
            posts = posts[:max_posts]
            
            print(f"✓ Found {len(posts)} posts")
            return posts
            
        except Exception as e:
            print(f"✗ Failed to get posts: {e}")
            return []
    
    def like_post(self, post_element=None):
        """Like a post - Uses both JavaScript and Selenium clicks"""
        if not self.safety.can_perform_action('like'):
            return False
        
        try:
            # If post element provided, click it first
            if post_element:
                print("→ Opening post...")
                self.human.human_click(post_element)
                self.human.random_delay(4, 6)  # Wait longer for post to fully load
            
            print("→ Searching for like button...")
            
            # Strategy 1: JavaScript click (most reliable for Instagram)
            # Like button: Find FIRST span containing SVG with aria-label="Like"
            js_selectors = [
                # Best: Find first span with Like SVG (handles duplicates)
                """(function() {
                    var section = document.querySelector('article section:first-of-type');
                    if (!section) return null;
                    var spans = section.querySelectorAll('span');
                    for (var i = 0; i < spans.length; i++) {
                        var svg = spans[i].querySelector('svg[aria-label="Like"]');
                        if (svg) return spans[i];
                    }
                    return null;
                })()""",
                # Fallback: First span in section
                "document.querySelector('article section:first-of-type span:first-child')",
                "document.querySelector('div[role=\"dialog\"] article section:first-of-type span:first-child')",
            ]
            
            for js_selector in js_selectors:
                try:
                    # Check if element exists and is not already liked
                    js_code = f"""
                        var btn = {js_selector};
                        if (btn) {{
                            var label = btn.getAttribute('aria-label');
                            if (label && (label.includes('Unlike') || label.includes('Dislike'))) {{
                                return 'already_liked';
                            }}
                            btn.click();
                            return 'clicked';
                        }}
                        return null;
                    """
                    
                    result = self.driver.execute_script(js_code)
                    
                    if result == 'already_liked':
                        print("ℹ️  Post already liked, skipping")
                        self.close_post_modal()
                        return False
                    
                    if result == 'clicked':
                        print(f"✓ Like button clicked (JavaScript)")
                        self.human.random_delay(2, 3)
                        
                        # Verify like worked
                        verify_js = """
                            var btn = document.querySelector('article button[aria-label="Unlike"]') || 
                                      document.querySelector('div[role="dialog"] button[aria-label="Unlike"]');
                            return btn !== null;
                        """
                        is_liked = self.driver.execute_script(verify_js)
                        
                        if is_liked:
                            print("✓✓✓ LIKE VERIFIED - Button changed to 'Unlike'!")
                            self.safety.record_action('like', success=True)
                            print("❤️  Post liked successfully!")
                            self.human.random_delay(2, 4)
                            self.close_post_modal()
                            return True
                        else:
                            print("⚠️  Click executed but verification unclear")
                            # Continue to next strategy
                    
                except Exception as e:
                    continue
            
            # Strategy 2: Selenium click with WebDriverWait (fallback)
            print("→ Trying Selenium click method...")
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            selectors = [
                # User's NEW exact XPath - section[1] span[1] (THIS IS THE ONE!)
                (By.XPATH, "/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]"),
                # Simplified - section 1, span 1
                (By.XPATH, "//article//section[1]//span[1]"),
                (By.XPATH, "//div[@role='dialog']//article//section[1]//span[1]"),
                (By.XPATH, "//article//section[1]//span[1]//div"),
                (By.XPATH, "//article//section[1]//span[1]//button"),
                # CSS versions
                (By.CSS_SELECTOR, "article section:first-of-type span:first-child"),
                (By.CSS_SELECTOR, "div[role='dialog'] article section:first-of-type span:first-child"),
                # Original fallbacks
                (By.XPATH, "//article//button[@aria-label='Like']"),
            ]
            
            for by, selector in selectors:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    like_button = wait.until(EC.element_to_be_clickable((by, selector)))
                    
                    # Check if already liked
                    aria_label = like_button.get_attribute('aria-label')
                    if aria_label and ('Unlike' in aria_label or 'Dislike' in aria_label):
                        print("ℹ️  Post already liked, skipping")
                        self.close_post_modal()
                        return False
                    
                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_button)
                    self.human.random_delay(0.5, 1)
                    
                    # Try regular click
                    like_button.click()
                    print("✓ Like button clicked (Selenium)")
                    
                    self.human.random_delay(2, 3)
                    
                    # Verify
                    try:
                        self.driver.find_element(By.XPATH, "//button[@aria-label='Unlike']")
                        print("✓✓✓ LIKE VERIFIED!")
                        self.safety.record_action('like', success=True)
                        print("❤️  Post liked successfully!")
                        self.human.random_delay(2, 4)
                        self.close_post_modal()
                        return True
                    except:
                        # Assume it worked even if we can't verify
                        self.safety.record_action('like', success=True)
                        print("❤️  Post liked (assumed)!")
                        self.human.random_delay(2, 4)
                        self.close_post_modal()
                        return True
                        
                except Exception as e:
                    continue
            
            # Strategy 3: Double-tap (Instagram native gesture simulation)
            print("→ Trying double-tap method...")
            try:
                # Find the post image and double-click it
                image_selectors = [
                    "//article//img[@alt]",
                    "//div[@role='dialog']//img",
                ]
                
                for img_selector in image_selectors:
                    try:
                        image = self.driver.find_element(By.XPATH, img_selector)
                        # JavaScript double-click
                        self.driver.execute_script("""
                            var img = arguments[0];
                            var event = new MouseEvent('dblclick', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            img.dispatchEvent(event);
                        """, image)
                        
                        print("✓ Double-tap executed")
                        self.human.random_delay(2, 3)
                        
                        # Verify
                        verify_js = """
                            return document.querySelector('button[aria-label="Unlike"]') !== null;
                        """
                        is_liked = self.driver.execute_script(verify_js)
                        
                        if is_liked:
                            print("✓✓✓ LIKE VERIFIED (double-tap)!")
                            self.safety.record_action('like', success=True)
                            print("❤️  Post liked successfully!")
                            self.human.random_delay(2, 4)
                            self.close_post_modal()
                            return True
                            
                    except:
                        continue
                        
            except Exception as e:
                pass
            
            print("✗ All like strategies failed")
            print("   Instagram may have changed their layout or post is already liked")
            self.close_post_modal()
            return False
            
        except Exception as e:
            print(f"✗ Failed to like post: {e}")
            import traceback
            traceback.print_exc()
            self.close_post_modal()
            return False
    
    def comment_on_post(self, comment_text=None, post_element=None):
        """
        Comment on a post
        IMPORTANT: Must be called BEFORE like_post() for textarea to remain accessible!
        
        Args:
            comment_text: Comment to post (if None and AI enabled, will generate)
            post_element: Post element to click (optional if post already open)
            
        Returns:
            bool: Success status
        """
        if not self.safety.can_perform_action('comment'):
            return False
        
        try:
            # If post element provided, click it first
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    # If post element provided, click it first
                    if post_element:
                        self.human.human_click(post_element)
                        self.human.random_delay(2, 4)

                    # Generate AI comment if enabled and no comment provided
                    if comment_text is None and self.use_ai_comments:
                        print("🤖 Generating AI comment...")
                        comment_text = self.ai_generator.generate_comment_for_post(self.driver)
                        if not comment_text:
                            print("✗ Could not generate comment")
                            return False
                        print(f"✓ Generated: {comment_text}")
                    elif comment_text is None:
                        # Fallback to generic comments (BMP-compatible emojis only)
                        comment_text = random.choice([
                            "Love this!",
                            "Amazing!",
                            "Beautiful!",
                            "So good!",
                            "Great shot!",
                            "Incredible!",
                            "Nice!",
                            "Awesome!",
                        ])
                        print(f"💬 Using: {comment_text}")

                    # Wait for page to stabilize
                    self.human.random_delay(3, 5)

                    # Find textarea directly - no need to click comment button!
                    print("→ Finding comment textarea...")
                    textarea = None
                    textarea_selectors = [
                        # Standard post
                        "//textarea[@aria-label='Add a comment…' and @placeholder='Add a comment…']",
                        # Sometimes aria-label or placeholder alone
                        "//textarea[@aria-label='Add a comment…']",
                        "//textarea[@placeholder='Add a comment…']",
                        # Reels/Video (Instagram may use different structure)
                        "//form//textarea",
                        "//div[contains(@role, 'dialog')]//textarea",
                        # Fallback: any visible textarea
                        "//textarea"
                    ]
                    for selector in textarea_selectors:
                        try:
                            textarea = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                            if textarea.is_displayed():
                                print(f"✓ Found textarea with selector: {selector}")
                                break
                        except Exception:
                            continue
                    if not textarea:
                        print(f"✗ Textarea not found with any selector")
                        continue  # Retry

                    # Refind textarea to avoid stale element
                    print(f"→ Typing comment: '{comment_text}'")
                    try:
                        textarea = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…' and @placeholder='Add a comment…']"))
                        )
                        textarea.send_keys(comment_text)
                        # Send a space and backspace to trigger Post button enable
                        from selenium.webdriver.common.keys import Keys
                        textarea.send_keys(" " + Keys.BACKSPACE)
                    except Exception as e:
                        print(f"✗ Could not type: {e}")
                        continue  # Retry

                    # Verify it typed
                    verify_result = self.driver.execute_script("""
                        var textarea = document.querySelector("textarea[aria-label='Add a comment…']");
                        return {value: textarea ? textarea.value : ''};
                    """)
                    print(f"✓ Typed: '{verify_result.get('value', '')}'")

                    # Wait before submitting to ensure Post button is enabled
                    self.human.random_delay(2, 3)

                    # Submit by clicking Post button
                    print(f"→ Submitting comment...")
                    self.human.random_delay(1, 2)

                    submit_result = self.driver.execute_script("""
                        // Find Post button
                        var buttons = Array.from(document.querySelectorAll('div[role="button"]'));
                        var postBtn = buttons.find(btn => btn.innerText.trim() === 'Post');

                        if (postBtn && !postBtn.disabled) {
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

                        return {success: false, error: 'Post button not found or disabled'};
                    """)

                    if not submit_result.get('success'):
                        print(f"✗ {submit_result.get('error', 'Could not submit')}")
                        continue  # Retry

                    print(f"✓ Submitted via {submit_result.get('method')}")

                    # Wait longer and verify comment is posted before closing modal
                    import time
                    max_wait = 10  # seconds
                    interval = 1
                    comment_posted = False
                    for _ in range(int(max_wait / interval)):
                        self.human.random_delay(interval, interval)
                        verify_submit = self.driver.execute_script("""
                            var textarea = document.querySelector('textarea[aria-label="Add a comment…"]');
                            return {isEmpty: textarea ? textarea.value === '' : false};
                        """)
                        if verify_submit.get('isEmpty'):
                            comment_posted = True
                            break
                    if comment_posted:
                        print(f"✓ Comment posted successfully!")
                        self.safety.record_action('comment', success=True)
                        return True
                    else:
                        print(f"⚠️  Comment may not have posted (textarea not cleared after waiting)")
                        continue  # Retry
                except Exception as e:
                    print(f"✗ Comment failed: {e}")
                    continue  # Retry
            print(f"✗ All comment attempts failed after {max_retries} retries.")
            return False
            # Wait longer and verify comment is posted before closing modal
            import time
            max_wait = 10  # seconds
            interval = 1
            comment_posted = False
            for _ in range(int(max_wait / interval)):
                self.human.random_delay(interval, interval)
                verify_submit = self.driver.execute_script("""
                    var textarea = document.querySelector('textarea[aria-label="Add a comment…"]');
                    return {isEmpty: textarea ? textarea.value === '' : false};
                """)
                if verify_submit.get('isEmpty'):
                    comment_posted = True
                    break
            if comment_posted:
                print(f"✓ Comment posted successfully!")
                self.safety.record_action('comment', success=True)
                return True
            else:
                print(f"⚠️  Comment may not have posted (textarea not cleared after waiting)")
                return False
                
        except Exception as e:
            print(f"✗ Comment failed: {e}")
            return False
    
    def comment_on_post_OLD_BROKEN(self, comment_text=None, post_element=None):
        """
        Comment on a post
        NOTE: Must be called BEFORE like_post() for textarea to remain accessible!
        
        Args:
            comment_text: Comment to post (if None and AI enabled, will generate)
            post_element: Post element to click
            
        Returns:
            bool: Success status
        """
        if not self.safety.can_perform_action('comment'):
            return False
        
        try:
            # If post element provided, click it first
            if post_element:
                self.human.human_click(post_element)
                self.human.random_delay(2, 4)
            
            # Generate AI comment if enabled and no comment provided
            if comment_text is None and self.use_ai_comments:
                print("🤖 Generating AI comment...")
                comment_text = self.ai_generator.generate_comment_for_post(self.driver)
                
                if not comment_text:
                    print("✗ Could not generate comment")
                    return False
                
                print(f"✓ Generated: {comment_text}")
            elif comment_text is None:
                # Fallback to generic comments
                comment_text = random.choice([
                    "Love this! ❤️",
                    "Amazing! ✨",
                    "Beautiful! 😍",
                    "So good! 🔥",
                ])
                print(f"💬 Using: {comment_text}")
            
            # Find and click comment button - use SVG aria-label="Comment"
            print("→ Finding comment button...")
            
            comment_button = None
            
            # Strategy 1: Find by SVG with aria-label="Comment" and go to clickable parent
            try:
                # Use JavaScript to find and verify the comment button
                comment_button_js = """
                    var svg = document.querySelector('article svg[aria-label="Comment"]') ||
                              document.querySelector('div[role="dialog"] article svg[aria-label="Comment"]');
                    if (svg) {
                        // Find the clickable parent (div with role="button")
                        var clickable = svg.closest('div[role="button"]');
                        if (clickable) {
                            return true;
                        }
                    }
                    return false;
                """
                
                if self.driver.execute_script(comment_button_js):
                    print(f"✓ Found comment button via SVG Comment label")
                    # We'll click it with JavaScript in the next step
                else:
                    print("✗ Could not find comment button with SVG Comment label")
                    return False
                    
            except Exception as e:
                print(f"✗ Error finding comment button: {e}")
                return False
            
            # Click the button to open comment field using MULTIPLE strategies
            print("→ Clicking comment button...")
            
            # Strategy 1: JavaScript with MouseEvent
            try:
                click_js = """
                    var svg = document.querySelector('div[role="dialog"] article svg[aria-label="Comment"]') ||
                              document.querySelector('article svg[aria-label="Comment"]');
                    
                    if (!svg) return {success: false, error: 'SVG not found'};
                    
                    // Find the clickable parent - try all ancestors up to 5 levels
                    var current = svg;
                    for (var i = 0; i < 5; i++) {
                        current = current.parentElement;
                        if (!current) break;
                        
                        // Try clicking this element with MouseEvent
                        var event = new MouseEvent('click', {
                            view: window,
                            bubbles: true,
                            cancelable: true
                        });
                        current.dispatchEvent(event);
                        
                        // Small delay to check if textarea appears
                        return {success: true, method: 'MouseEvent on parent level ' + (i+1)};
                    }
                    
                    return {success: false, error: 'No parent worked'};
                """
                
                result = self.driver.execute_script(click_js)
                if result.get('success'):
                    print(f"✓ Comment button clicked (method: {result.get('method')})")
                    self.human.random_delay(2, 3)
                else:
                    print(f"⚠️  JS click failed: {result.get('error')}, trying Selenium...")
            except Exception as e:
                print(f"⚠️  JS click error: {e}, trying Selenium...")
            
            # Strategy 2: Selenium click on the SVG's parent using ActionChains
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                
                svg_element = self.driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"] article svg[aria-label="Comment"]')
                
                # Get parent element
                parent = self.driver.execute_script("return arguments[0].parentElement.parentElement;", svg_element)
                
                # Move to element and click
                actions = ActionChains(self.driver)
                actions.move_to_element(parent).click().perform()
                
                print(f"✓ Comment button clicked (ActionChains)")
                self.human.random_delay(2, 3)
                
            except Exception as e:
                print(f"⚠️  ActionChains failed: {e}, trying direct click...")
                
                # Strategy 3: Direct Selenium click on parent
                try:
                    svg_element = self.driver.find_element(By.CSS_SELECTOR, 'article svg[aria-label="Comment"]')
                    parent = self.driver.execute_script("return arguments[0].parentElement.parentElement;", svg_element)
                    parent.click()
                    print(f"✓ Comment button clicked (direct parent click)")
                    self.human.random_delay(2, 3)
                except Exception as e2:
                    print(f"✗ All click strategies failed: {e2}")
                    return False
            
            # Now find the textarea that appears
            textarea_selectors = [
                "//textarea[@placeholder='Add a comment…']",
                "//textarea[@aria-label='Add a comment…']",
                "//form//textarea",
                "//textarea",
            ]
            
            comment_area = None
            for selector in textarea_selectors:
                try:
                    comment_area = self.driver.find_element(By.XPATH, selector)
                    print(f"✓ Found textarea: {selector[:60]}...")
                    break
                except:
                    continue
            
            if not comment_area:
                print(f"✗ Textarea did not appear after clicking comment button")
                return False
            
            # Click textarea to focus
            try:
                comment_area.click()
                self.human.random_delay(1, 2)
            except:
                # Element might be stale, try to refind
                pass
            
            # Re-find textarea right before typing (it might have been re-rendered)
            print(f"→ Re-finding textarea before typing...")
            try:
                comment_area = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a comment…']"))
                )
                print(f"✓ Textarea re-located")
            except:
                # Try other selectors
                for selector in textarea_selectors:
                    try:
                        comment_area = self.driver.find_element(By.XPATH, selector)
                        break
                    except:
                        continue
            
            # Type comment - use comprehensive JavaScript that mimics real typing
            print(f"→ Typing comment...")
            try:
                # Method 1: JavaScript with multiple events (best for Instagram)
                type_js = """
                    var textarea = arguments[0];
                    var text = arguments[1];
                    
                    // Clear any existing text
                    textarea.value = '';
                    
                    // Focus the textarea
                    textarea.focus();
                    
                    // Set the value
                    textarea.value = text;
                    
                    // Trigger ALL the events Instagram listens to
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    textarea.dispatchEvent(new Event('change', { bubbles: true }));
                    textarea.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true }));
                    textarea.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                    
                    // Make sure React sees the change
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                    nativeInputValueSetter.call(textarea, text);
                    
                    var event = new Event('input', { bubbles: true });
                    textarea.dispatchEvent(event);
                    
                    return textarea.value === text;
                """
                
                success = self.driver.execute_script(type_js, comment_area, comment_text)
                
                if success:
                    print(f"✓ Comment typed: '{comment_text[:50]}...'")
                else:
                    print(f"⚠️  Text set but verification unclear")
                
            except Exception as e:
                print(f"⚠️  JavaScript typing failed: {e}")
                # Fallback: Try send_keys character by character (slow but reliable)
                try:
                    comment_area.clear()
                    comment_area.click()
                    self.human.random_delay(0.5, 1)
                    
                    # Remove emojis that might cause issues
                    safe_text = ''.join(c for c in comment_text if ord(c) < 0x10000)
                    
                    # Type character by character with small delays
                    for char in safe_text:
                        comment_area.send_keys(char)
                        self.human.random_delay(0.05, 0.1)
                    
                    print(f"✓ Comment typed (character-by-character fallback)")
                except Exception as e2:
                    print(f"✗ Failed to type comment: {e2}")
                    return False
            
            self.human.random_delay(1, 2)
            
            # Verify text is in textarea
            try:
                current_value = comment_area.get_attribute('value')
                if current_value and len(current_value) > 0:
                    print(f"✓ Verified: Textarea contains {len(current_value)} characters")
                else:
                    print(f"⚠️  Warning: Textarea appears empty!")
            except:
                pass
            
            # Post comment - try multiple methods
            print(f"→ Finding Post button...")
            
            # Method 1: Try to find Post button near the textarea
            post_button = None
            post_button_selectors = [
                # Most specific - button with "Post" text in comment form
                "//form//button[contains(text(), 'Post')]",
                "//button[contains(text(), 'Post')]",
                # Enabled submit button
                "//form//button[@type='submit' and not(@disabled)]",
                "//button[@type='submit' and not(@disabled)]",
                # Any form button
                "//form//button[not(@disabled)]",
            ]
            
            for selector in post_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    if buttons:
                        # Get the last one (usually the Post button for comments)
                        post_button = buttons[-1]
                        print(f"✓ Found Post button: {selector[:50]}...")
                        break
                except:
                    continue
            
            if not post_button:
                print(f"⚠️  Could not find Post button, trying Enter key instead...")
                # Fallback: Press Enter in textarea
                try:
                    comment_area.send_keys('\n')
                    print(f"✓ Pressed Enter to post")
                except:
                    print(f"✗ Could not post comment")
                    return False
            else:
                # Click Post button
                print(f"→ Clicking Post button...")
                try:
                    # Try JavaScript click first
                    self.driver.execute_script("arguments[0].click();", post_button)
                    print(f"✓ Post button clicked (JavaScript)")
                except:
                    try:
                        self.human.human_click(post_button)
                        print(f"✓ Post button clicked (Selenium)")
                    except Exception as e:
                        print(f"✗ Failed to click Post button: {e}")
                        return False
            
            # Record action
            self.safety.record_action('comment', success=True)
            print(f"💬 Commented: {comment_text}")
            
            # Random delay
            self.human.random_delay(3, 6)
            
            # Close post modal
            self.close_post_modal()
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to comment: {e}")
            self.close_post_modal()
            return False
    
    def close_post_modal(self):
        """Close post modal/overlay"""
        try:
            # Press ESC key or click close button
            self.driver.find_element(By.TAG_NAME, 'body').send_keys('\ue00c')  # ESC key
            self.human.random_delay(0.5, 1)
        except Exception:
            pass
    
    def like_posts_by_hashtag(self, hashtag, amount=5):
        """Like multiple posts from a hashtag"""
        print(f"\n🎯 Starting to like {amount} posts from #{hashtag}")
        
        if not self.search_hashtag(hashtag):
            return 0
        
        posts = self.get_posts_from_page(max_posts=amount * 2)  # Get extra posts
        
        if not posts:
            print("✗ No posts found")
            return 0
        
        liked_count = 0
        
        for i, post in enumerate(posts):
            if liked_count >= amount:
                break
            
            if not self.safety.can_perform_action('like'):
                print("⚠️  Safety limits reached, stopping")
                break
            
            print(f"\n📸 Processing post {i+1}/{len(posts)}")
            
            if self.like_post(post):
                liked_count += 1
            
            # Take break if needed
            if self.human.should_take_break(liked_count):
                self.human.session_break()
            else:
                self.human.random_delay()
        
        print(f"\n✓ Liked {liked_count} posts from #{hashtag}")
        return liked_count
