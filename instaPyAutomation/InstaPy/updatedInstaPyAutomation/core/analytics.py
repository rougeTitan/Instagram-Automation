"""
Instagram Analytics & Insights
Track engagement patterns, optimal posting times, follower growth
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


class InstagramAnalytics:
    """Track and analyze Instagram account performance"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.analytics_file = os.path.join(data_dir, 'analytics.json')
        self.data = self.load_data()
    
    def load_data(self):
        """Load analytics data from file"""
        if os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        return {
            'posts': [],
            'engagement_by_time': defaultdict(lambda: {'likes': 0, 'comments': 0, 'count': 0}),
            'engagement_by_day': defaultdict(lambda: {'likes': 0, 'comments': 0, 'count': 0}),
            'hashtag_performance': defaultdict(lambda: {'uses': 0, 'total_engagement': 0}),
            'follower_history': [],
            'action_history': []
        }
    
    def save_data(self):
        """Save analytics data to file"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Convert defaultdict to regular dict for JSON serialization
        save_data = {
            'posts': self.data['posts'],
            'engagement_by_time': dict(self.data['engagement_by_time']),
            'engagement_by_day': dict(self.data['engagement_by_day']),
            'hashtag_performance': dict(self.data['hashtag_performance']),
            'follower_history': self.data['follower_history'],
            'action_history': self.data['action_history']
        }
        
        with open(self.analytics_file, 'w') as f:
            json.dump(save_data, f, indent=2)
    
    def record_action(self, action_type, details=None):
        """
        Record an action taken by the bot
        
        Args:
            action_type: 'like', 'comment', 'follow', 'unfollow', etc.
            details: Additional info (hashtag, username, etc.)
        """
        action = {
            'type': action_type,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.data['action_history'].append(action)
        self.save_data()
    
    def record_post_engagement(self, post_url, likes, comments, hashtags=None, posted_at=None):
        """
        Record engagement metrics for a post
        
        Args:
            post_url: URL of the post
            likes: Number of likes
            comments: Number of comments
            hashtags: List of hashtags used
            posted_at: When post was created (datetime or ISO string)
        """
        if posted_at is None:
            posted_at = datetime.now()
        elif isinstance(posted_at, str):
            posted_at = datetime.fromisoformat(posted_at)
        
        post_data = {
            'url': post_url,
            'likes': likes,
            'comments': comments,
            'engagement': likes + comments,
            'hashtags': hashtags or [],
            'posted_at': posted_at.isoformat(),
            'hour': posted_at.hour,
            'day': posted_at.strftime('%A')
        }
        
        self.data['posts'].append(post_data)
        
        # Update time-based analytics
        hour_key = str(posted_at.hour)
        self.data['engagement_by_time'][hour_key]['likes'] += likes
        self.data['engagement_by_time'][hour_key]['comments'] += comments
        self.data['engagement_by_time'][hour_key]['count'] += 1
        
        # Update day-based analytics
        day_key = posted_at.strftime('%A')
        self.data['engagement_by_day'][day_key]['likes'] += likes
        self.data['engagement_by_day'][day_key]['comments'] += comments
        self.data['engagement_by_day'][day_key]['count'] += 1
        
        # Update hashtag performance
        if hashtags:
            engagement_per_tag = (likes + comments) / len(hashtags)
            for tag in hashtags:
                self.data['hashtag_performance'][tag]['uses'] += 1
                self.data['hashtag_performance'][tag]['total_engagement'] += engagement_per_tag
        
        self.save_data()
    
    def record_follower_count(self, count):
        """Record current follower count"""
        entry = {
            'count': count,
            'timestamp': datetime.now().isoformat()
        }
        self.data['follower_history'].append(entry)
        self.save_data()
    
    def get_best_posting_times(self, top_n=5):
        """
        Get best times to post based on historical engagement
        
        Returns:
            list: Top N hours with highest average engagement
        """
        time_stats = {}
        
        for hour, data in self.data['engagement_by_time'].items():
            if data['count'] > 0:
                avg_engagement = (data['likes'] + data['comments']) / data['count']
                time_stats[int(hour)] = avg_engagement
        
        # Sort by engagement and return top N
        sorted_times = sorted(time_stats.items(), key=lambda x: x[1], reverse=True)
        return sorted_times[:top_n]
    
    def get_best_posting_days(self):
        """
        Get best days to post based on historical engagement
        
        Returns:
            list: Days ranked by average engagement
        """
        day_stats = {}
        
        for day, data in self.data['engagement_by_day'].items():
            if data['count'] > 0:
                avg_engagement = (data['likes'] + data['comments']) / data['count']
                day_stats[day] = avg_engagement
        
        # Sort by engagement
        sorted_days = sorted(day_stats.items(), key=lambda x: x[1], reverse=True)
        return sorted_days
    
    def get_best_hashtags(self, min_uses=2, top_n=10):
        """
        Get best performing hashtags
        
        Args:
            min_uses: Minimum times hashtag must be used
            top_n: Number of top hashtags to return
            
        Returns:
            list: Top hashtags with average engagement
        """
        hashtag_stats = {}
        
        for tag, data in self.data['hashtag_performance'].items():
            if data['uses'] >= min_uses:
                avg_engagement = data['total_engagement'] / data['uses']
                hashtag_stats[tag] = {
                    'avg_engagement': avg_engagement,
                    'uses': data['uses'],
                    'total_engagement': data['total_engagement']
                }
        
        # Sort by average engagement
        sorted_tags = sorted(
            hashtag_stats.items(),
            key=lambda x: x[1]['avg_engagement'],
            reverse=True
        )
        return sorted_tags[:top_n]
    
    def get_engagement_rate(self, follower_count=None):
        """
        Calculate engagement rate
        
        Args:
            follower_count: Current follower count (if None, uses latest recorded)
            
        Returns:
            float: Engagement rate percentage
        """
        if not self.data['posts']:
            return 0.0
        
        if follower_count is None:
            if self.data['follower_history']:
                follower_count = self.data['follower_history'][-1]['count']
            else:
                return 0.0
        
        # Calculate average engagement
        total_engagement = sum(post['engagement'] for post in self.data['posts'])
        avg_engagement = total_engagement / len(self.data['posts'])
        
        # Engagement rate = (avg_engagement / followers) * 100
        if follower_count > 0:
            return (avg_engagement / follower_count) * 100
        return 0.0
    
    def get_follower_growth(self, days=30):
        """
        Calculate follower growth over period
        
        Args:
            days: Number of days to analyze
            
        Returns:
            dict: Growth statistics
        """
        if len(self.data['follower_history']) < 2:
            return {'growth': 0, 'growth_rate': 0, 'status': 'insufficient_data'}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [
            entry for entry in self.data['follower_history']
            if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
        ]
        
        if len(recent_entries) < 2:
            return {'growth': 0, 'growth_rate': 0, 'status': 'insufficient_recent_data'}
        
        start_count = recent_entries[0]['count']
        end_count = recent_entries[-1]['count']
        growth = end_count - start_count
        growth_rate = (growth / start_count * 100) if start_count > 0 else 0
        
        return {
            'growth': growth,
            'growth_rate': growth_rate,
            'start_count': start_count,
            'end_count': end_count,
            'period_days': days,
            'status': 'success'
        }
    
    def get_activity_summary(self, days=7):
        """
        Get summary of bot activity over period
        
        Args:
            days: Number of days to analyze
            
        Returns:
            dict: Activity statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_actions = [
            action for action in self.data['action_history']
            if datetime.fromisoformat(action['timestamp']) >= cutoff_date
        ]
        
        summary = {
            'total_actions': len(recent_actions),
            'likes': sum(1 for a in recent_actions if a['type'] == 'like'),
            'comments': sum(1 for a in recent_actions if a['type'] == 'comment'),
            'follows': sum(1 for a in recent_actions if a['type'] == 'follow'),
            'unfollows': sum(1 for a in recent_actions if a['type'] == 'unfollow'),
            'period_days': days
        }
        
        # Calculate daily average
        if days > 0:
            summary['avg_actions_per_day'] = summary['total_actions'] / days
        
        return summary
    
    def generate_report(self, follower_count=None):
        """
        Generate comprehensive analytics report
        
        Args:
            follower_count: Current follower count
            
        Returns:
            str: Formatted report
        """
        report = []
        report.append("=" * 60)
        report.append("INSTAGRAM ANALYTICS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Account Overview
        report.append("📊 ACCOUNT OVERVIEW")
        report.append("-" * 60)
        if follower_count:
            report.append(f"Current Followers: {follower_count:,}")
        
        engagement_rate = self.get_engagement_rate(follower_count)
        report.append(f"Engagement Rate: {engagement_rate:.2f}%")
        
        if engagement_rate >= 10:
            report.append("  Status: 🔥 Excellent (Viral potential)")
        elif engagement_rate >= 5:
            report.append("  Status: ✅ Very Good")
        elif engagement_rate >= 3:
            report.append("  Status: 👍 Good")
        elif engagement_rate >= 1:
            report.append("  Status: ⚠️  Below Average")
        else:
            report.append("  Status: ❌ Needs Improvement")
        report.append("")
        
        # Follower Growth
        report.append("📈 FOLLOWER GROWTH (Last 30 Days)")
        report.append("-" * 60)
        growth_data = self.get_follower_growth(30)
        if growth_data['status'] == 'success':
            report.append(f"Growth: {growth_data['growth']:+,} followers")
            report.append(f"Growth Rate: {growth_data['growth_rate']:+.2f}%")
            report.append(f"Start: {growth_data['start_count']:,} → End: {growth_data['end_count']:,}")
        else:
            report.append(f"Status: {growth_data['status']}")
        report.append("")
        
        # Best Posting Times
        report.append("⏰ BEST POSTING TIMES")
        report.append("-" * 60)
        best_times = self.get_best_posting_times(5)
        if best_times:
            for i, (hour, engagement) in enumerate(best_times, 1):
                time_12hr = f"{hour % 12 or 12}:00 {'PM' if hour >= 12 else 'AM'}"
                report.append(f"{i}. {time_12hr} - Avg Engagement: {engagement:.1f}")
        else:
            report.append("Not enough data yet")
        report.append("")
        
        # Best Posting Days
        report.append("📅 BEST POSTING DAYS")
        report.append("-" * 60)
        best_days = self.get_best_posting_days()
        if best_days:
            for i, (day, engagement) in enumerate(best_days, 1):
                report.append(f"{i}. {day} - Avg Engagement: {engagement:.1f}")
        else:
            report.append("Not enough data yet")
        report.append("")
        
        # Top Hashtags
        report.append("🏷️  TOP PERFORMING HASHTAGS")
        report.append("-" * 60)
        top_tags = self.get_best_hashtags(min_uses=2, top_n=10)
        if top_tags:
            for i, (tag, stats) in enumerate(top_tags, 1):
                report.append(
                    f"{i}. #{tag} - Avg: {stats['avg_engagement']:.1f} "
                    f"(used {stats['uses']}x)"
                )
        else:
            report.append("Not enough data yet")
        report.append("")
        
        # Recent Activity
        report.append("🤖 BOT ACTIVITY (Last 7 Days)")
        report.append("-" * 60)
        activity = self.get_activity_summary(7)
        report.append(f"Total Actions: {activity['total_actions']}")
        report.append(f"  Likes: {activity['likes']}")
        report.append(f"  Comments: {activity['comments']}")
        report.append(f"  Follows: {activity['follows']}")
        report.append(f"  Unfollows: {activity['unfollows']}")
        if activity['total_actions'] > 0:
            report.append(f"  Avg/Day: {activity['avg_actions_per_day']:.1f}")
        report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 60)
        
        if engagement_rate < 3:
            report.append("⚠️  Low engagement rate:")
            report.append("   • Focus on high-quality, value-driven content")
            report.append("   • Use Reels for higher reach")
            report.append("   • Engage more with your audience")
        
        if best_times:
            top_time = best_times[0][0]
            time_12hr = f"{top_time % 12 or 12}:00 {'PM' if top_time >= 12 else 'AM'}"
            report.append(f"✓ Post consistently around {time_12hr}")
        
        if best_days:
            top_day = best_days[0][0]
            report.append(f"✓ Prioritize posting on {top_day}")
        
        if top_tags:
            report.append(f"✓ Use high-performing hashtags: {', '.join('#' + tag for tag, _ in top_tags[:3])}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_data(self, filename='analytics_export.json'):
        """Export all analytics data to a file"""
        export_path = os.path.join(self.data_dir, filename)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'data': {
                'posts': self.data['posts'],
                'engagement_by_time': dict(self.data['engagement_by_time']),
                'engagement_by_day': dict(self.data['engagement_by_day']),
                'hashtag_performance': dict(self.data['hashtag_performance']),
                'follower_history': self.data['follower_history'],
                'action_history': self.data['action_history']
            }
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Analytics exported to {export_path}")
        return export_path


# Example usage
if __name__ == "__main__":
    analytics = InstagramAnalytics()
    
    # Example: Record some actions
    analytics.record_action('like', {'hashtag': 'travel', 'post_url': 'https://...'})
    analytics.record_action('comment', {'comment': 'Beautiful!', 'post_url': 'https://...'})
    
    # Example: Record follower count
    analytics.record_follower_count(1250)
    
    # Generate report
    print(analytics.generate_report(follower_count=1250))
