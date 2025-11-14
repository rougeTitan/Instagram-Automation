"""
AI-Powered Comment Generation
Uses vision AI to analyze images and generate natural, contextual comments
"""
import os
import base64
import requests
from io import BytesIO
from PIL import Image
import random
from selenium.webdriver.common.by import By
from .config import Config


class AICommentGenerator:
    """Generate human-like comments based on image content"""
    
    def __init__(self, model='gemini'):
        """
        Initialize AI comment generator
        
        Args:
            model: 'gemini' (Google Gemini - FREE!), 'openai' (GPT-4 Vision), or 'local' (BLIP)
        """
        self.model = model
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Comment templates for different scenarios
        self.comment_styles = [
            'enthusiastic',  # "Wow! This is amazing!"
            'appreciative',  # "Love this! Great work!"
            'thoughtful',    # "This really captures the moment"
            'curious',       # "Where was this taken?"
            'supportive'     # "Keep creating!"
        ]
        
        # Emoji sets for different contexts
        self.emojis = {
            'nature': ['🌿', '🌸', '🌺', '🌻', '🌲', '🌳', '🍃', '🌾'],
            'travel': ['✈️', '🌍', '🗺️', '🧳', '🏖️', '🏔️', '🌅', '🌄'],
            'food': ['😋', '🤤', '👌', '🔥', '❤️', '✨'],
            'fitness': ['💪', '🔥', '💯', '👏', '⚡', '🏃'],
            'fashion': ['✨', '🔥', '👗', '👠', '💄', '👑', '💫'],
            'pets': ['🐕', '🐶', '🐱', '🐾', '❤️', '😍', '🥰'],
            'art': ['🎨', '✨', '🖼️', '👏', '🔥', '💫'],
            'general': ['❤️', '✨', '🔥', '👍', '😍', '🙌', '💯']
        }
    
    def analyze_image_with_openai(self, image_url):
        """
        Analyze image using OpenAI GPT-4 Vision
        
        Args:
            image_url: URL of the Instagram image
            
        Returns:
            dict: {
                'description': 'what the image shows',
                'mood': 'positive/inspiring/peaceful',
                'subjects': ['sunset', 'beach', 'person'],
                'category': 'travel'
            }
        """
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in .env file")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        
        payload = {
            "model": "gpt-4o-mini",  # Cost-effective vision model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this Instagram image and provide:
1. Brief description (1 sentence)
2. Mood/emotion conveyed
3. Main subjects (list)
4. Category (travel/nature/food/fitness/fashion/pets/art/lifestyle)
5. Is it appropriate for commenting? (yes/no)

Format as JSON:
{
    "description": "...",
    "mood": "...",
    "subjects": [...],
    "category": "...",
    "appropriate": true/false
}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            import json
            analysis = json.loads(content)
            return analysis
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def analyze_image_with_gemini(self, image_url):
        """
        Analyze image using Google Gemini Vision (FREE tier available!)
        
        Args:
            image_url: URL of the Instagram image
            
        Returns:
            dict: Analysis results
        """
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in .env file")
        
        # Gemini 2.5 Flash is fast and free!
        # Using v1beta for vision models
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
        
        try:
            # Download and encode image
            img_response = requests.get(image_url, timeout=10)
            img_response.raise_for_status()
            img_data = base64.b64encode(img_response.content).decode('utf-8')
            
            # Determine mime type
            content_type = img_response.headers.get('content-type', 'image/jpeg')
            
            payload = {
                "contents": [{
                    "parts": [
                        {
                            "text": """Analyze this Instagram image and respond in JSON format:
{
  "description": "brief 1-sentence description",
  "mood": "positive/inspiring/peaceful/energetic/etc",
  "subjects": ["main", "subject", "list"],
  "category": "travel/nature/food/fitness/fashion/pets/art/lifestyle",
  "appropriate": true
}

Only respond with valid JSON, nothing else."""
                        },
                        {
                            "inline_data": {
                                "mime_type": content_type,
                                "data": img_data
                            }
                        }
                    ]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Parse Gemini response
            text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Try to parse as JSON
            import json
            import re
            
            # Extract JSON from response (sometimes has markdown formatting)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback parsing if JSON not found
                analysis = {
                    'description': text[:100],
                    'mood': 'positive',
                    'subjects': self._extract_keywords(text),
                    'category': self._detect_category(text),
                    'appropriate': 'nsfw' not in text.lower() and 'inappropriate' not in text.lower()
                }
            
            return analysis
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    def _extract_keywords(self, text):
        """Extract potential subjects from text"""
        keywords = []
        common_subjects = ['sunset', 'ocean', 'beach', 'mountain', 'food', 'person', 
                          'city', 'nature', 'sky', 'travel', 'landscape', 'portrait']
        text_lower = text.lower()
        for keyword in common_subjects:
            if keyword in text_lower:
                keywords.append(keyword)
        return keywords[:3]  # Return max 3
    
    def _detect_category(self, text):
        """Detect category from text"""
        text_lower = text.lower()
        categories = {
            'travel': ['travel', 'trip', 'vacation', 'destination', 'explore'],
            'nature': ['nature', 'landscape', 'sunset', 'mountain', 'forest', 'ocean'],
            'food': ['food', 'meal', 'dish', 'restaurant', 'cooking', 'delicious'],
            'fitness': ['fitness', 'gym', 'workout', 'exercise', 'training'],
            'fashion': ['fashion', 'outfit', 'style', 'clothing', 'dress'],
            'pets': ['dog', 'cat', 'pet', 'animal', 'puppy', 'kitten'],
            'art': ['art', 'painting', 'drawing', 'creative', 'artwork']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def generate_comment(self, analysis, style=None):
        """
        Generate a natural comment based on image analysis
        
        Args:
            analysis: dict from analyze_image_*
            style: Comment style (or random if None)
            
        Returns:
            str: Generated comment
        """
        if not analysis or not analysis.get('appropriate', True):
            return None
        
        category = analysis.get('category', 'general')
        mood = analysis.get('mood', 'positive')
        subjects = analysis.get('subjects', [])
        is_video = analysis.get('is_video', False)
        is_carousel = analysis.get('is_carousel', False)
        
        # Choose style
        if not style:
            style = random.choice(self.comment_styles)
        
        # Generate comment based on style and content
        comments = []
        
        if style == 'enthusiastic':
            if is_video:
                templates = [
                    "Wow! This reel is incredible! {emoji}",
                    "Absolutely love this! {emoji}{emoji}",
                    "This video is so good! {emoji}",
                    "Can't stop watching! {emoji}{emoji}",
                    "Amazing content! {emoji}"
                ]
            elif is_carousel:
                templates = [
                    "Wow! Love all of these! {emoji}",
                    "Every shot is amazing! {emoji}{emoji}",
                    "This whole set is beautiful! {emoji}",
                    "All of these are stunning! {emoji}{emoji}",
                    "Perfect collection! {emoji}"
                ]
            else:
                templates = [
                    "Wow! This is incredible! {emoji}",
                    "Absolutely amazing! {emoji}{emoji}",
                    "This is so beautiful! {emoji}",
                    "Love this so much! {emoji}{emoji}",
                    "Stunning! {emoji}"
                ]
        elif style == 'appreciative':
            if is_video:
                templates = [
                    "Really love this reel {emoji}",
                    "Great video! {emoji}",
                    "This is so well done {emoji}",
                    "Love the energy here {emoji}",
                    "Perfect! {emoji}"
                ]
            elif is_carousel:
                templates = [
                    "Really love these {emoji}",
                    "Beautiful shots! {emoji}",
                    "These are so well done {emoji}",
                    "Love the collection {emoji}",
                    "Perfect captures! {emoji}"
                ]
            else:
                templates = [
                    "Really love this {emoji}",
                    "Beautiful shot! {emoji}",
                    "This is so well done {emoji}",
                    "Love the vibes here {emoji}",
                    "Perfect capture! {emoji}"
                ]
        elif style == 'thoughtful':
            templates = [
                "This really captures the essence {emoji}",
                "There's something special about this {emoji}",
                "Love the mood here {emoji}",
                "This speaks to me {emoji}",
                "Beautiful perspective {emoji}"
            ]
        elif style == 'curious':
            if is_video:
                templates = [
                    "Where was this filmed? Looks amazing! {emoji}",
                    "Love this! What did you use to edit? {emoji}",
                    "This is beautiful! {emoji}",
                    "How did you do this? Looks incredible! {emoji}",
                    "This is so cool! {emoji}"
                ]
            else:
                templates = [
                    "Where is this? Looks amazing! {emoji}",
                    "This is beautiful! What camera did you use? {emoji}",
                    "Love this! When was this taken? {emoji}",
                    "Gorgeous! I need to visit here {emoji}",
                    "This looks incredible! {emoji}"
                ]
        else:  # supportive
            templates = [
                "Keep up the great work! {emoji}",
                "Love your content! {emoji}",
                "Always inspiring! {emoji}",
                "You're so talented! {emoji}",
                "Love following your journey {emoji}"
            ]
        
        # Select template and add emojis
        template = random.choice(templates)
        # No emojis - BMP compatibility for ChromeDriver
        emoji = ""
        
        comment = template.format(emoji=emoji).strip()
        
        # Append custom message
        comment = f"{comment}. Please check my instagram page"
        
        # Occasionally add subject-specific mention
        if subjects and random.random() < 0.3:
            subject = random.choice(subjects)
            if is_carousel:
                prefixes = [
                    f"Love all the {subject}s! ",
                    f"Those {subject}s are perfect! ",
                    f"Beautiful {subject}s! "
                ]
            else:
                prefixes = [
                    f"Love the {subject}! ",
                    f"That {subject} is perfect! ",
                    f"Beautiful {subject}! "
                ]
            comment = random.choice(prefixes) + comment
        
        return comment
    
    def detect_post_type(self, driver):
        """
        Detect if post is image, video/reel, or carousel
        
        Returns:
            str: 'image', 'video', 'carousel', or 'unknown'
        """
        try:
            # Check for video/reel indicators
            video_indicators = [
                "//video",
                "//article//div[contains(@class, 'reel')]",
                "//*[@aria-label='Reel']",
                "//*[contains(text(), 'Reels')]"
            ]
            
            for indicator in video_indicators:
                try:
                    if driver.find_elements(By.XPATH, indicator):
                        return 'video'
                except:
                    pass
            
            # Check for carousel (multiple images)
            carousel_indicators = [
                "//button[@aria-label='Next']",
                "//button[@aria-label='Go to next slide']",
                "//div[@role='button'][contains(@aria-label, 'page')]"
            ]
            
            for indicator in carousel_indicators:
                try:
                    if driver.find_elements(By.XPATH, indicator):
                        return 'carousel'
                except:
                    pass
            
            # Default to image
            return 'image'
            
        except:
            return 'unknown'
    
    def get_video_thumbnail(self, driver):
        """
        Extract thumbnail/poster image from video/reel
        
        Returns:
            str: Thumbnail URL or None
        """
        try:
            # Look for video element poster
            video_elements = driver.find_elements(By.TAG_NAME, "video")
            for video in video_elements:
                poster = video.get_attribute('poster')
                if poster and 'scontent' in poster:
                    print(f"✓ Found video thumbnail: {poster[:80]}...")
                    return poster
            
            # Fallback: Find any image (videos often have thumbnail overlay)
            return self.get_image_url_from_post(driver)
            
        except Exception as e:
            print(f"→ Video thumbnail extraction failed, trying image fallback")
            return self.get_image_url_from_post(driver)
    
    def get_carousel_images(self, driver, max_images=3):
        """
        Extract multiple images from carousel post
        
        Args:
            driver: Selenium WebDriver
            max_images: Maximum number of images to extract
            
        Returns:
            list: List of image URLs
        """
        images = []
        
        try:
            # Get first image
            first_img = self.get_image_url_from_post(driver)
            if first_img:
                images.append(first_img)
                print(f"✓ Carousel image 1: {first_img[:60]}...")
            
            # Try to navigate to next images
            for i in range(max_images - 1):
                try:
                    # Find and click next button
                    next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                    next_button.click()
                    
                    # Wait for new image to load
                    import time
                    time.sleep(1)
                    
                    # Get next image
                    next_img = self.get_image_url_from_post(driver)
                    if next_img and next_img not in images:
                        images.append(next_img)
                        print(f"✓ Carousel image {len(images)}: {next_img[:60]}...")
                    else:
                        break  # No more unique images
                        
                except:
                    break  # No more images or button not found
            
            # Navigate back to first image
            try:
                prev_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='Go back']")
                for _ in range(len(images) - 1):
                    if prev_buttons:
                        prev_buttons[0].click()
                        import time
                        time.sleep(0.5)
            except:
                pass
            
            return images
            
        except Exception as e:
            print(f"→ Carousel extraction error: {e}")
            return images if images else None
    
    def get_image_url_from_post(self, driver):
        """
        Extract image URL from current Instagram post
        
        Args:
            driver: Selenium WebDriver
            
        Returns:
            str: Image URL or None
        """
        try:
            # Try multiple strategies to find the image
            selectors = [
                # Main post image (most common)
                "//article//div[@role='button']//img",
                "//article//img[@alt]",
                # Dialog/modal image
                "//div[@role='dialog']//img[@alt]",
                "//div[@role='dialog']//img[contains(@src, 'scontent')]",
                # Any Instagram CDN image
                "//img[contains(@src, 'scontent')]",
                "//img[contains(@src, 'instagram')]",
                # Fallback - any article image
                "//article//img",
            ]
            
            for selector in selectors:
                try:
                    imgs = driver.find_elements(By.XPATH, selector)
                    for img_element in imgs:
                        img_url = img_element.get_attribute('src')
                        # Validate it's a real content image (not profile pic)
                        if img_url and 'scontent' in img_url and len(img_url) > 50:
                            return img_url
                except Exception as e:
                    continue
            
            # Last resort: get all images and pick the largest
            try:
                all_imgs = driver.find_elements(By.TAG_NAME, "img")
                largest_img = None
                largest_size = 0
                
                for img in all_imgs:
                    try:
                        src = img.get_attribute('src')
                        if not src or 'scontent' not in src:
                            continue
                        
                        width = img.get_attribute('naturalWidth')
                        height = img.get_attribute('naturalHeight')
                        
                        if width and height:
                            size = int(width) * int(height)
                            if size > largest_size:
                                largest_size = size
                                largest_img = src
                    except:
                        continue
                
                if largest_img:
                    return largest_img
                    
            except Exception as e:
                pass
            
            return None
            
        except Exception as e:
            print(f"✗ Error extracting image URL: {e}")
            return None
    
    def generate_comment_for_post(self, driver, style=None):
        """
        Main method: Analyze current post and generate comment
        Handles images, videos/reels, and carousels
        
        Args:
            driver: Selenium WebDriver (must be on a post)
            style: Comment style (optional)
            
        Returns:
            str: Generated comment or None
        """
        try:
            # Detect post type
            post_type = self.detect_post_type(driver)
            print(f"📋 Post type: {post_type.upper()}")
            
            img_url = None
            analysis = None
            
            # Handle different post types
            if post_type == 'video':
                print("🎬 Video/Reel detected - analyzing thumbnail...")
                img_url = self.get_video_thumbnail(driver)
                
                if img_url:
                    # Analyze thumbnail
                    if self.model == 'openai':
                        analysis = self.analyze_image_with_openai(img_url)
                    elif self.model == 'gemini':
                        analysis = self.analyze_image_with_gemini(img_url)
                    
                    # Adjust comment style for videos
                    if analysis:
                        analysis['is_video'] = True
                        print(f"✓ Video analysis: {analysis.get('category', 'general')} - {analysis.get('mood', 'positive')}")
                else:
                    print("⚠️  Could not get video thumbnail, using generic video comments")
                    return self._get_video_fallback_comment()
            
            elif post_type == 'carousel':
                print("🎠 Carousel detected - analyzing multiple images...")
                images = self.get_carousel_images(driver, max_images=3)
                
                if images and len(images) > 0:
                    # Analyze first image (primary)
                    print(f"🖼️  Analyzing primary image from {len(images)} total...")
                    
                    if self.model == 'openai':
                        analysis = self.analyze_image_with_openai(images[0])
                    elif self.model == 'gemini':
                        analysis = self.analyze_image_with_gemini(images[0])
                    
                    if analysis:
                        analysis['is_carousel'] = True
                        analysis['image_count'] = len(images)
                        print(f"✓ Carousel analysis: {analysis.get('category', 'general')} - {len(images)} images")
                else:
                    print("⚠️  Could not extract carousel images")
                    return self.get_fallback_comment()
            
            else:  # Single image
                print("🖼️  Single image - analyzing...")
                img_url = self.get_image_url_from_post(driver)
                
                if img_url:
                    if self.model == 'openai':
                        analysis = self.analyze_image_with_openai(img_url)
                    elif self.model == 'gemini':
                        analysis = self.analyze_image_with_gemini(img_url)
                else:
                    print("✗ Could not extract image URL")
                    return self.get_fallback_comment()
            
            # Check if we have analysis
            if not analysis:
                print("✗ Analysis failed, using fallback")
                return self.get_fallback_comment()
            
            # Check if appropriate
            if not analysis.get('appropriate', True):
                print("⚠️  Content flagged as inappropriate for commenting")
                return None
            
            # Generate comment based on analysis
            comment = self.generate_comment(analysis, style)
            return comment
            
        except Exception as e:
            print(f"✗ Error in AI comment generation: {e}")
            import traceback
            traceback.print_exc()
            return self.get_fallback_comment()
    
    def _get_video_fallback_comment(self):
        """Fallback comments specifically for videos/reels (BMP-compatible only)"""
        video_comments = [
            "Love this reel!",
            "Amazing video!",
            "This is so good!",
            "Great content!",
            "Can't stop watching!",
            "This is fire!",
            "So entertaining!",
            "Perfect!",
            "Awesome!",
            "Nice!"
        ]
        comment = random.choice(video_comments)
        return f"{comment}. Please check my instagram page"
    
    def get_fallback_comment(self):
        """Return a safe generic comment if AI fails (no emojis - BMP only)"""
        fallbacks = [
            "Love this!",
            "Amazing!",
            "Beautiful!",
            "So good!",
            "Incredible!",
            "Perfect!",
            "Stunning!",
            "Great shot!",
            "Awesome!",
            "Nice work!"
        ]
        comment = random.choice(fallbacks)
        return f"{comment}. Please check my instagram page"
    
    def get_comment_variations(self, base_comment, count=3):
        """
        Generate variations of a comment to avoid repetition
        
        Args:
            base_comment: Original comment
            count: Number of variations
            
        Returns:
            list: Comment variations
        """
        variations = [base_comment]
        
        # Simple variations (you can make this more sophisticated)
        prefixes = ["", "Really ", "Truly ", "Absolutely "]
        suffixes = ["", " 👏", " ❤️", " 🔥"]
        
        for i in range(count - 1):
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            variation = prefix + base_comment.strip() + suffix
            variations.append(variation)
        
        return variations


# Usage example
if __name__ == "__main__":
    # Test the comment generator
    generator = AICommentGenerator(model='openai')
    
    # Mock analysis for testing
    test_analysis = {
        'description': 'Beautiful sunset over the ocean',
        'mood': 'peaceful',
        'subjects': ['sunset', 'ocean', 'sky'],
        'category': 'nature',
        'appropriate': True
    }
    
    print("Generating test comments:\n")
    for style in ['enthusiastic', 'appreciative', 'thoughtful', 'curious', 'supportive']:
        comment = generator.generate_comment(test_analysis, style=style)
        print(f"{style}: {comment}")
