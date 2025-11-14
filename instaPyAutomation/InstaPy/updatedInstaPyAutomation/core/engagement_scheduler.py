"""
Instagram Peak Engagement Time Analyzer
Analyzes best posting/engagement times for each day of the week
"""
from datetime import datetime, time as dt_time
from collections import defaultdict


class EngagementScheduler:
    """
    Determines optimal engagement times based on Instagram research and analytics
    
    Based on general Instagram engagement research:
    - Best overall times: 11 AM - 2 PM on weekdays
    - Monday-Friday: Lunch hours (11 AM - 1 PM) and evening (7-9 PM)
    - Wednesday: Best day overall (11 AM and 3-4 PM)
    - Saturday-Sunday: 9 AM - 11 AM (morning browsing)
    """
    
    # Peak engagement times for each day (24-hour format)
    PEAK_TIMES = {
        'Monday': [
            {'hour': 11, 'minute': 0, 'engagement_level': 'high', 'reason': 'Late morning break'},
            {'hour': 19, 'minute': 0, 'engagement_level': 'high', 'reason': 'After work hours'}
        ],
        'Tuesday': [
            {'hour': 11, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Mid-morning peak'},
            {'hour': 14, 'minute': 0, 'engagement_level': 'high', 'reason': 'Afternoon break'}
        ],
        'Wednesday': [
            {'hour': 11, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Best day - morning peak'},
            {'hour': 15, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Best day - afternoon peak'}
        ],
        'Thursday': [
            {'hour': 12, 'minute': 0, 'engagement_level': 'high', 'reason': 'Lunch hour'},
            {'hour': 17, 'minute': 0, 'engagement_level': 'high', 'reason': 'End of workday'}
        ],
        'Friday': [
            {'hour': 13, 'minute': 0, 'engagement_level': 'high', 'reason': 'Lunch hour'},
            {'hour': 20, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Weekend starts'}
        ],
        'Saturday': [
            {'hour': 10, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Weekend morning'},
            {'hour': 19, 'minute': 0, 'engagement_level': 'high', 'reason': 'Saturday evening'}
        ],
        'Sunday': [
            {'hour': 10, 'minute': 0, 'engagement_level': 'very_high', 'reason': 'Sunday morning browsing'},
            {'hour': 19, 'minute': 0, 'engagement_level': 'high', 'reason': 'Sunday evening'}
        ]
    }
    
    @classmethod
    def get_peak_times(cls, day_name):
        """
        Get peak engagement times for a specific day
        
        Args:
            day_name: Day name (e.g., 'Monday', 'Tuesday')
            
        Returns:
            list: Peak time slots for the day
        """
        return cls.PEAK_TIMES.get(day_name, [])
    
    @classmethod
    def get_primary_peak_time(cls, day_name):
        """
        Get the single best time for a day
        
        Args:
            day_name: Day name
            
        Returns:
            dict: Primary peak time info
        """
        peaks = cls.get_peak_times(day_name)
        if peaks:
            # Return first peak (usually the best)
            return peaks[0]
        return None
    
    @classmethod
    def get_all_weekly_schedule(cls):
        """
        Get complete weekly schedule with peak times
        
        Returns:
            dict: Complete schedule for all 7 days
        """
        return cls.PEAK_TIMES
    
    @classmethod
    def format_time_12h(cls, hour, minute=0):
        """
        Format time in 12-hour format
        
        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
            
        Returns:
            str: Formatted time (e.g., "11:00 AM")
        """
        period = 'AM' if hour < 12 else 'PM'
        display_hour = hour % 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minute:02d} {period}"
    
    @classmethod
    def is_peak_time_now(cls, tolerance_minutes=30):
        """
        Check if current time is within peak engagement window
        
        Args:
            tolerance_minutes: Minutes before/after peak time to consider as peak
            
        Returns:
            tuple: (is_peak, day_name, peak_info)
        """
        now = datetime.now()
        day_name = now.strftime('%A')
        current_hour = now.hour
        current_minute = now.minute
        
        peaks = cls.get_peak_times(day_name)
        for peak in peaks:
            peak_hour = peak['hour']
            peak_minute = peak['minute']
            
            # Calculate difference in minutes
            time_diff = abs((current_hour * 60 + current_minute) - (peak_hour * 60 + peak_minute))
            
            if time_diff <= tolerance_minutes:
                return (True, day_name, peak)
        
        return (False, day_name, None)
    
    @classmethod
    def get_next_peak_time(cls):
        """
        Get the next upcoming peak time
        
        Returns:
            tuple: (day_name, peak_info, datetime_object)
        """
        now = datetime.now()
        current_day = now.strftime('%A')
        
        # Days of week in order
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_day_idx = days.index(current_day)
        
        # Check remaining peaks today
        today_peaks = cls.get_peak_times(current_day)
        for peak in today_peaks:
            peak_time = now.replace(hour=peak['hour'], minute=peak['minute'], second=0, microsecond=0)
            if peak_time > now:
                return (current_day, peak, peak_time)
        
        # Check next 7 days
        for i in range(1, 8):
            next_day_idx = (current_day_idx + i) % 7
            next_day = days[next_day_idx]
            peaks = cls.get_peak_times(next_day)
            if peaks:
                # Return first peak of that day
                peak = peaks[0]
                # Calculate datetime for next occurrence
                days_ahead = i
                next_date = now.replace(hour=peak['hour'], minute=peak['minute'], second=0, microsecond=0)
                from datetime import timedelta
                next_date = next_date + timedelta(days=days_ahead)
                return (next_day, peak, next_date)
        
        return (None, None, None)
    
    @classmethod
    def print_weekly_schedule(cls):
        """Print formatted weekly engagement schedule"""
        print("=" * 80)
        print("INSTAGRAM PEAK ENGAGEMENT TIMES - WEEKLY SCHEDULE")
        print("=" * 80)
        print()
        
        for day, peaks in cls.PEAK_TIMES.items():
            print(f"📅 {day.upper()}")
            print("-" * 80)
            for i, peak in enumerate(peaks, 1):
                time_str = cls.format_time_12h(peak['hour'], peak['minute'])
                level_emoji = "🔥" if peak['engagement_level'] == 'very_high' else "⚡"
                print(f"  {i}. {level_emoji} {time_str} - {peak['reason']}")
                print(f"     Engagement: {peak['engagement_level'].replace('_', ' ').title()}")
            print()
        
        print("=" * 80)
        print("💡 RECOMMENDATION: Schedule automation to run at these peak times")
        print("=" * 80)
        print()
    
    @classmethod
    def generate_automation_schedule(cls, categories_per_day=2, posts_per_category=5):
        """
        Generate a weekly automation schedule
        
        Args:
            categories_per_day: Number of categories to process per day
            posts_per_category: Number of posts per category
            
        Returns:
            dict: Weekly schedule with times and settings
        """
        schedule = {}
        
        for day, peaks in cls.PEAK_TIMES.items():
            # Use primary peak time for the day
            primary_peak = peaks[0]
            
            schedule[day] = {
                'time': cls.format_time_12h(primary_peak['hour'], primary_peak['minute']),
                'hour': primary_peak['hour'],
                'minute': primary_peak['minute'],
                'engagement_level': primary_peak['engagement_level'],
                'reason': primary_peak['reason'],
                'categories': categories_per_day,
                'posts_per_category': posts_per_category,
                'total_posts': categories_per_day * posts_per_category,
                'enabled': True
            }
        
        return schedule


def generate_task_scheduler_commands(schedule):
    """
    Generate Windows Task Scheduler commands for automation
    
    Args:
        schedule: Weekly schedule from generate_automation_schedule()
        
    Returns:
        list: PowerShell commands to create scheduled tasks
    """
    commands = []
    script_path = "C:\\Users\\siddh\\OneDrive\\Desktop\\instaPyAutomation\\InstaPy\\updatedInstaPyAutomation\\main.py"
    
    commands.append("# Windows Task Scheduler Commands")
    commands.append("# Run these in PowerShell as Administrator\n")
    
    for day, config in schedule.items():
        task_name = f"InstagramBot_{day}"
        time_str = f"{config['hour']:02d}:{config['minute']:02d}"
        
        # Get day of week number (Sunday = 0)
        days_map = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 
                    'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        day_num = days_map.get(day, 1)
        
        cmd = f"""schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc weekly /d {day.upper()[:3]} /st {time_str} /f"""
        
        commands.append(f"\n# {day} at {config['time']} ({config['reason']})")
        commands.append(cmd)
    
    return "\n".join(commands)


if __name__ == "__main__":
    scheduler = EngagementScheduler()
    
    # Print weekly schedule
    scheduler.print_weekly_schedule()
    
    # Check if now is peak time
    is_peak, day, peak_info = scheduler.is_peak_time_now(tolerance_minutes=60)
    print(f"\n📊 Current Status:")
    print(f"   Day: {day}")
    print(f"   Time: {datetime.now().strftime('%I:%M %p')}")
    print(f"   Is Peak Time: {'Yes 🔥' if is_peak else 'No'}")
    if is_peak:
        print(f"   Peak: {peak_info['reason']}")
    print()
    
    # Get next peak time
    next_day, next_peak, next_datetime = scheduler.get_next_peak_time()
    if next_day:
        print(f"⏭️  Next Peak Time:")
        print(f"   {next_day} at {scheduler.format_time_12h(next_peak['hour'], next_peak['minute'])}")
        print(f"   {next_peak['reason']}")
        print(f"   {next_datetime.strftime('%Y-%m-%d %I:%M %p')}")
    print()
    
    # Generate automation schedule
    print("\n" + "=" * 80)
    print("RECOMMENDED AUTOMATION SCHEDULE")
    print("=" * 80)
    auto_schedule = scheduler.generate_automation_schedule(categories_per_day=2, posts_per_category=5)
    
    for day, config in auto_schedule.items():
        print(f"\n{day}:")
        print(f"  ⏰ Time: {config['time']} ({config['engagement_level'].replace('_', ' ').title()})")
        print(f"  📂 Categories: {config['categories']}")
        print(f"  📝 Posts per category: {config['posts_per_category']}")
        print(f"  📊 Total posts: {config['total_posts']}")
        print(f"  💡 Reason: {config['reason']}")
    
    print("\n" + "=" * 80)
