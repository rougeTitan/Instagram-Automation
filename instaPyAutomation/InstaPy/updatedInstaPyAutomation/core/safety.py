"""
Safety Manager
Tracks actions and enforces rate limits
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from .config import Config


class SafetyManager:
    """Manages action counts and enforces safety limits"""
    
    def __init__(self):
        self.stats_file = Config.STATS_FILE
        self.stats = self.load_stats()
        self.reset_daily_stats_if_needed()
    
    def load_stats(self):
        """Load statistics from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"✗ Failed to load stats: {e}")
        
        return self.get_default_stats()
    
    def get_default_stats(self):
        """Get default statistics structure"""
        return {
            'last_reset': datetime.now().strftime('%Y-%m-%d'),
            'daily': {
                'likes': 0,
                'follows': 0,
                'comments': 0,
                'unfollows': 0,
                'total_actions': 0
            },
            'hourly': {
                'last_hour': datetime.now().strftime('%Y-%m-%d %H:00:00'),
                'actions': 0
            },
            'session': {
                'start_time': None,
                'actions': 0
            }
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"✗ Failed to save stats: {e}")
    
    def reset_daily_stats_if_needed(self):
        """Reset daily stats if it's a new day"""
        last_reset = datetime.strptime(self.stats['last_reset'], '%Y-%m-%d').date()
        today = datetime.now().date()
        
        if today > last_reset:
            print("🔄 Resetting daily statistics for new day")
            self.stats['daily'] = {
                'likes': 0,
                'follows': 0,
                'comments': 0,
                'unfollows': 0,
                'total_actions': 0
            }
            self.stats['last_reset'] = today.strftime('%Y-%m-%d')
            self.save_stats()
    
    def reset_hourly_stats_if_needed(self):
        """Reset hourly stats if it's a new hour"""
        current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        # Initialize if missing
        if 'last_hour' not in self.stats['hourly']:
            self.stats['hourly']['last_hour'] = current_hour.strftime('%Y-%m-%d %H:00:00')
            self.stats['hourly']['actions'] = 0
            self.save_stats()
            return
        
        last_hour = datetime.strptime(
            self.stats['hourly']['last_hour'],
            '%Y-%m-%d %H:00:00'
        )
        
        if current_hour > last_hour:
            self.stats['hourly'] = {
                'last_hour': current_hour.strftime('%Y-%m-%d %H:00:00'),
                'actions': 0
            }
            self.save_stats()
    
    def can_perform_action(self, action_type):
        """Check if action can be performed within safety limits"""
        self.reset_daily_stats_if_needed()
        self.reset_hourly_stats_if_needed()
        
        # Check daily limits
        daily_limits = {
            'like': Config.MAX_LIKES_PER_DAY,
            'follow': Config.MAX_FOLLOWS_PER_DAY,
            'comment': Config.MAX_COMMENTS_PER_DAY,
            'unfollow': Config.MAX_UNFOLLOWS_PER_DAY
        }
        
        daily_action_map = {
            'like': 'likes',
            'follow': 'follows',
            'comment': 'comments',
            'unfollow': 'unfollows'
        }
        
        if action_type in daily_limits:
            stat_key = daily_action_map[action_type]
            current_count = self.stats['daily'][stat_key]
            limit = daily_limits[action_type]
            
            if current_count >= limit:
                print(f"⚠️  Daily limit reached for {action_type} ({current_count}/{limit})")
                return False
        
        # Check hourly limits
        if self.stats['hourly']['actions'] >= Config.MAX_ACTIONS_PER_HOUR:
            print(f"⚠️  Hourly action limit reached ({Config.MAX_ACTIONS_PER_HOUR})")
            return False
        
        return True
    
    def record_action(self, action_type, success=True):
        """Record an action in statistics"""
        if not success:
            return
        
        action_map = {
            'like': 'likes',
            'follow': 'follows',
            'comment': 'comments',
            'unfollow': 'unfollows'
        }
        
        if action_type in action_map:
            stat_key = action_map[action_type]
            self.stats['daily'][stat_key] += 1
        
        self.stats['daily']['total_actions'] += 1
        self.stats['hourly']['actions'] += 1
        self.stats['session']['actions'] += 1
        
        self.save_stats()
    
    def start_session(self):
        """Mark session start"""
        self.stats['session'] = {
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'actions': 0
        }
        self.save_stats()
    
    def get_session_stats(self):
        """Get current session statistics"""
        return self.stats['session']
    
    def get_daily_stats(self):
        """Get daily statistics"""
        return self.stats['daily']
    
    def print_stats(self):
        """Print current statistics"""
        print("\n" + "="*60)
        print("📊 CURRENT STATISTICS")
        print("="*60)
        
        daily = self.stats['daily']
        print(f"Today's Actions:")
        print(f"  Likes:      {daily['likes']}/{Config.MAX_LIKES_PER_DAY}")
        print(f"  Follows:    {daily['follows']}/{Config.MAX_FOLLOWS_PER_DAY}")
        print(f"  Comments:   {daily['comments']}/{Config.MAX_COMMENTS_PER_DAY}")
        print(f"  Unfollows:  {daily['unfollows']}/{Config.MAX_UNFOLLOWS_PER_DAY}")
        print(f"  Total:      {daily['total_actions']}")
        
        print(f"\nThis Hour:    {self.stats['hourly']['actions']}/{Config.MAX_ACTIONS_PER_HOUR} actions")
        print(f"This Session: {self.stats['session']['actions']} actions")
        print("="*60 + "\n")
