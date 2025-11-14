# Modern Instagram Automation Bot

A safer, more modern Instagram automation tool built with Python, Selenium, and undetected-chromedriver.

## ⚠️ WARNING

This bot automates Instagram actions which **VIOLATES Instagram's Terms of Service**. Use at your own risk.

**Potential Consequences:**
- Account suspension or permanent ban
- Temporary action blocks
- Shadowban (reduced visibility)

**Recommendations:**
- Use a test account first
- Start with very low limits
- Never use on important accounts

## ✨ Features

- **Undetected Chrome** - Bypasses most automation detection
- **Human-like Behavior** - Random delays, mouse movements, scrolling
- **Safety Limits** - Built-in rate limiting and quotas
- **Session Persistence** - Saves cookies to avoid repeated logins
- **Statistics Tracking** - Monitors all actions and limits
- **Modern Architecture** - Clean, modular code structure

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your Instagram credentials:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### 3. Run the Bot

```bash
python main.py
```

## 📁 Project Structure

```
updatedInstaPyAutomation/
├── main.py              # Main entry point
├── config.py            # Configuration management
├── browser_setup.py     # Chrome setup with stealth features
├── actions.py           # Instagram actions (like, comment, etc.)
├── humanize.py          # Human-like behavior simulation
├── safety.py            # Rate limiting and safety checks
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .env                 # Your credentials (create this)
└── data/                # Storage for cookies and stats
    ├── cookies.json     # Saved session cookies
    └── statistics.json  # Action statistics
```

## 🎯 Features

### Currently Implemented:
- ✅ Login with stealth mode
- ✅ Search hashtags
- ✅ Like posts
- ✅ Comment on posts
- ✅ Human-like delays and behavior
- ✅ Rate limiting
- ✅ Session persistence

### Coming Soon:
- ⏳ Follow/Unfollow users
- ⏳ Story viewing
- ⏳ DM automation
- ⏳ Follower/Following analysis
- ⏳ Scheduling

## ⚙️ Configuration

Edit `.env` to customize settings:

### Safety Limits (per day)
```
MAX_LIKES_PER_DAY=40
MAX_FOLLOWS_PER_DAY=25
MAX_COMMENTS_PER_DAY=10
MAX_ACTIONS_PER_HOUR=15
```

### Delays (seconds)
```
MIN_ACTION_DELAY=3
MAX_ACTION_DELAY=10
MIN_SESSION_BREAK=300
MAX_SESSION_BREAK=600
```

### Browser Settings
```
HEADLESS=False          # True to hide browser window
WINDOW_SIZE=1920,1080   # Browser window size
```

## 🛡️ Safety Features

1. **Rate Limiting**
   - Daily limits for each action type
   - Hourly action limits
   - Automatic daily reset

2. **Human-like Behavior**
   - Random delays between actions
   - Mouse movement simulation
   - Natural scrolling patterns
   - Session breaks every 10-20 actions

3. **Stealth Mode**
   - Undetected ChromeDriver
   - JavaScript fingerprint hiding
   - Real user agent strings
   - Cookie persistence

4. **Error Handling**
   - Graceful recovery from errors
   - Automatic modal dismissal
   - Session state tracking

## 📊 Statistics

The bot tracks:
- Daily action counts (likes, follows, comments)
- Hourly action counts
- Session statistics
- Success/failure rates

Stats are saved in `data/statistics.json`

## 🔧 Customization

### Change Target Hashtags

Edit `main.py`:
```python
hashtags = ['your', 'hashtags', 'here']
```

### Adjust Like Amount

```python
actions.like_posts_by_hashtag(hashtag, amount=10)  # Change 10 to your desired amount
```

### Add Custom Comments

In `actions.py`, modify the `comment_on_post` function to use your comment list.

## 🐛 Troubleshooting

### "Chrome driver not found"
- Undetected-chromedriver downloads automatically
- Ensure you have Chrome installed
- Check your internet connection

### "Login failed"
- Verify credentials in `.env`
- Check if Instagram requires verification
- Try logging in manually first

### "Action limits reached"
- Check `data/statistics.json` for current counts
- Wait until next day for daily reset
- Adjust limits in `.env`

### Browser crashes or freezes
- Update Chrome to latest version
- Reduce `MAX_ACTIONS_PER_HOUR`
- Increase delays in config

## 📝 Best Practices

1. **Start Slow**
   - Day 1-3: 5-10 likes per day
   - Day 4-7: 15-20 likes per day
   - Week 2+: 30-40 likes per day

2. **Be Random**
   - Don't run at the same time every day
   - Vary the hashtags you target
   - Mix with manual usage

3. **Monitor Your Account**
   - Check for action blocks
   - Watch for security challenges
   - Stop immediately if you get warnings

4. **Use Test Accounts**
   - Never use your main account
   - Create dedicated test accounts
   - Keep multiple backups

## 📜 License

This project is for educational purposes only. The creator is not responsible for any misuse or account bans.

## 🤝 Contributing

This is a learning project. Feel free to modify and improve it for your own educational purposes.

## ⚖️ Disclaimer

This bot violates Instagram's Terms of Service. Use at your own risk. The author takes no responsibility for any consequences including account suspension, data loss, or legal action.

---

**Remember:** The safest way to grow on Instagram is through authentic engagement and quality content. Automation should only be used for learning and testing purposes.
