# 🚀 Quick Start Guide - Your Updated Bot

## ✅ What Your Bot Does NOW (After Updates)

When you run `python main.py`, your bot will:

1. **Login** to Instagram
2. **Search hashtags** (#travel, #nature, #photography)
3. **Like posts** (5 per hashtag)
4. **Comment on 30%** of liked posts (randomly selected)

### Current Setup (Without AI):
- ✅ Likes posts
- ✅ Comments with generic messages: "Love this! ❤️", "Amazing! ✨", etc.
- ❌ AI comments (disabled by default)

---

## 📊 Current Limits (Your .env Settings)

```
MAX_LIKES_PER_DAY = 10 (can like up to 10 posts per day)
MAX_COMMENTS_PER_DAY = 5 (can comment up to 5 times per day)
MAX_ACTIONS_PER_HOUR = 8 (max 8 actions per hour)
Comment Rate = 30% (comments on 30% of liked posts)
```

### What This Means:
- Bot will like ~10 posts
- Bot will comment on ~3 posts (30% of 10)
- Uses generic comments like "Love this! ❤️"

---

## 🤖 To Enable AI Comments

### Step 1: Get API Key
Go to: https://platform.openai.com/api-keys
- Create account
- Add $5-10 credit
- Create new key (starts with `sk-...`)

### Step 2: Update .env
Open `.env` and add:
```bash
# Uncomment and add your key:
OPENAI_API_KEY=sk-your-actual-key-here
USE_AI_COMMENTS=True
```

### Step 3: Install Dependencies
```powershell
pip install openai requests pillow
```

### Step 4: Run Bot
```powershell
python main.py
```

Now it will:
- Analyze images with AI
- Generate contextual comments
- Example: "Wow! This is incredible! 🌅" for sunset photo

---

## 📝 Current Behavior Examples

### Without AI (Current):
```
Post 1: [Random image]
→ Like ❤️
→ Comment: "Love this! ❤️" (generic)

Post 2: [Random image]
→ Like ❤️
→ No comment (30% rate)

Post 3: [Random image]
→ Like ❤️
→ Comment: "Amazing! ✨" (generic)
```

### With AI Enabled:
```
Post 1: [Sunset photo]
→ Like ❤️
→ AI analyzes: "sunset, ocean, peaceful"
→ Comment: "Wow! This is incredible! 🌅✨"

Post 2: [Food photo]
→ Like ❤️
→ No comment (30% rate)

Post 3: [Mountain photo]
→ Like ❤️
→ AI analyzes: "mountain, hiking, adventure"
→ Comment: "Where is this? Looks amazing! ⛰️"
```

---

## ⚙️ Customization Options

### 1. Change Hashtags
Edit `main.py` line ~103:
```python
hashtags = ['travel', 'nature', 'photography']
# Change to your interests:
hashtags = ['fitness', 'food', 'fashion']
```

### 2. Adjust Posts Per Hashtag
Edit `main.py` line ~104:
```python
posts_per_hashtag = 5
# Change to like more/fewer posts:
posts_per_hashtag = 10  # Will process 10 posts per hashtag
```

### 3. Change Comment Rate
Edit `main.py` line ~105:
```python
comment_percentage = 30  # Comments on 30% of liked posts
# Change to comment more/less:
comment_percentage = 50  # Comments on 50% of posts
comment_percentage = 100  # Comments on ALL posts
comment_percentage = 0  # Never comments
```

### 4. Increase Daily Limits
Edit `.env`:
```bash
MAX_LIKES_PER_DAY=50  # Up from 10
MAX_COMMENTS_PER_DAY=15  # Up from 5
MAX_ACTIONS_PER_HOUR=15  # Up from 8
```

⚠️ **Warning**: Higher limits = higher risk of shadowban

---

## 🎯 What About Following?

Following is **NOT implemented yet** in the current workflow, but the foundation is there.

### To Add Following (Future):
You would need to add code in `main.py` to:
1. Click on the post author's profile
2. Click "Follow" button
3. Track with safety limits

This would require additional development.

---

## 🧪 Testing Recommendations

### Day 1-3: Test Phase
```bash
MAX_LIKES_PER_DAY=10
MAX_COMMENTS_PER_DAY=5
USE_AI_COMMENTS=False  # Start without AI
```
Run 1-2 times per day, monitor for issues

### Day 4-7: Increase Slowly
```bash
MAX_LIKES_PER_DAY=20
MAX_COMMENTS_PER_DAY=10
USE_AI_COMMENTS=False
```

### Week 2+: Add AI
```bash
MAX_LIKES_PER_DAY=30
MAX_COMMENTS_PER_DAY=15
USE_AI_COMMENTS=True  # Enable AI
OPENAI_API_KEY=sk-...
```

---

## 🚦 Run Your Bot

### Standard Run (Without AI):
```powershell
cd C:\Users\siddh\Desktop\instaPyAutomation\InstaPy\updatedInstaPyAutomation
python main.py
```

**What happens**:
1. Shows warning prompt
2. Logs in
3. Searches #travel
4. Likes 5 posts, comments on ~2 (generic)
5. Searches #nature
6. Likes 5 posts, comments on ~2 (generic)
7. Stops (daily limit reached)

### With AI Comments:
1. Add `OPENAI_API_KEY` to `.env`
2. Set `USE_AI_COMMENTS=True`
3. Run `python main.py`

**What happens**:
- Same as above BUT
- Comments are AI-generated based on image content
- More natural and contextual

---

## 📊 View Analytics

After running the bot, check your performance:

```powershell
python -c "from analytics import InstagramAnalytics; a = InstagramAnalytics(); print(a.generate_report(follower_count=1000))"
```

Shows:
- Best posting times
- Top hashtags
- Engagement rate
- Activity summary

---

## ❓ FAQ

**Q: Does it follow accounts?**
A: Not yet. Only likes and comments.

**Q: Do I NEED AI comments?**
A: No! Bot works fine with generic comments. AI is optional.

**Q: How much does AI cost?**
A: ~$0.01 per comment. 5 comments/day = $1.50/month.

**Q: Is this safe?**
A: Safer than most bots (low limits, human-like), but still against Instagram ToS.

**Q: Can I run it multiple times per day?**
A: Yes, but limits are per 24 hours. If you hit 10 likes, wait until next day.

---

## 🎉 Summary

✅ **Your bot NOW**:
- Likes posts (10/day)
- Comments on posts (5/day)
- Uses generic comments by default
- Can enable AI comments with API key

✅ **Setup is complete**, just run:
```powershell
python main.py
```

🚀 **Ready to go!**
