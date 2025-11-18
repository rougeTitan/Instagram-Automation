"""
Daily Report Generator for Instagram Automation
Generates comprehensive performance reports and saves them as HTML and JSON
"""
import os
import sys
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.analytics import InstagramAnalytics
from core.config import Config

# Initialize colorama
init(autoreset=True)


def read_log_file(log_path):
    """Read and return log file content"""
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "No log data available"


def get_recent_log_summary(logs_dir, days=7):
    """Get summary of recent execution logs"""
    summary = []
    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    for day in day_names:
        log_file = os.path.join(logs_dir, f'{day}.log')
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract key metrics from log
            lines = content.split('\n')
            last_run = None
            posts_processed = 0
            comments_posted = 0
            likes_given = 0
            
            for line in lines:
                if 'Day:' in line and 'at' in line:
                    last_run = line.strip()
                elif 'Total posts processed:' in line:
                    try:
                        posts_processed = int(line.split(':')[1].split('/')[0].strip())
                    except:
                        pass
                elif 'Comments posted:' in line:
                    try:
                        comments_posted = int(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Posts liked:' in line:
                    try:
                        likes_given = int(line.split(':')[1].strip())
                    except:
                        pass
            
            if last_run or posts_processed > 0:
                summary.append({
                    'day': day.capitalize(),
                    'last_run': last_run,
                    'posts': posts_processed,
                    'comments': comments_posted,
                    'likes': likes_given
                })
    
    return summary


def generate_html_report(analytics, logs_dir, output_path):
    """Generate HTML report with styling"""
    
    # Get data
    best_times = analytics.get_best_posting_times(5)
    best_days = analytics.get_best_posting_days()
    top_hashtags = analytics.get_best_hashtags(min_uses=1, top_n=10)
    activity = analytics.get_activity_summary(7)
    growth = analytics.get_follower_growth(30)
    recent_logs = get_recent_log_summary(logs_dir, 7)
    
    # Calculate engagement rate (assuming we track follower count)
    engagement_rate = analytics.get_engagement_rate()
    
    # Current time
    now = datetime.now()
    report_time = now.strftime('%B %d, %Y at %I:%M %p')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Automation Daily Report - {now.strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .stat-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .table td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .table tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-success {{
            background: #10b981;
            color: white;
        }}
        
        .badge-warning {{
            background: #f59e0b;
            color: white;
        }}
        
        .badge-info {{
            background: #3b82f6;
            color: white;
        }}
        
        .engagement-status {{
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        
        .engagement-excellent {{
            background: #d1fae5;
            border-left: 4px solid #10b981;
        }}
        
        .engagement-good {{
            background: #dbeafe;
            border-left: 4px solid #3b82f6;
        }}
        
        .engagement-warning {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
        }}
        
        .recent-activity {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }}
        
        .activity-item {{
            padding: 15px;
            background: white;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .activity-day {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .activity-stats {{
            display: flex;
            gap: 20px;
            font-size: 0.9em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }}
        
        .recommendations {{
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .recommendations h4 {{
            color: #f59e0b;
            margin-bottom: 10px;
        }}
        
        .recommendations ul {{
            list-style-position: inside;
            color: #666;
        }}
        
        .recommendations li {{
            margin: 8px 0;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Instagram Automation Report</h1>
            <p>Generated on {report_time}</p>
        </div>
        
        <div class="content">
            <!-- Quick Stats -->
            <div class="section">
                <h2 class="section-title">📈 Quick Stats (Last 7 Days)</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Actions</h3>
                        <div class="value">{activity['total_actions']}</div>
                        <div class="label">Actions Performed</div>
                    </div>
                    <div class="stat-card">
                        <h3>Posts Liked</h3>
                        <div class="value">{activity['likes']}</div>
                        <div class="label">❤️ Likes Given</div>
                    </div>
                    <div class="stat-card">
                        <h3>Comments Posted</h3>
                        <div class="value">{activity['comments']}</div>
                        <div class="label">💬 AI Comments</div>
                    </div>
                    <div class="stat-card">
                        <h3>Avg Per Day</h3>
                        <div class="value">{activity.get('avg_actions_per_day', 0):.1f}</div>
                        <div class="label">Daily Average</div>
                    </div>
                </div>
            </div>
            
            <!-- Engagement Rate -->
            <div class="section">
                <h2 class="section-title">💯 Engagement Status</h2>
"""
    
    # Add engagement status
    if engagement_rate >= 5:
        html += f"""
                <div class="engagement-status engagement-excellent">
                    <h3>🔥 Excellent Engagement!</h3>
                    <p><strong>Engagement Rate: {engagement_rate:.2f}%</strong></p>
                    <p>Your content is performing extremely well. Keep up the great work!</p>
                </div>
"""
    elif engagement_rate >= 3:
        html += f"""
                <div class="engagement-status engagement-good">
                    <h3>✅ Good Engagement</h3>
                    <p><strong>Engagement Rate: {engagement_rate:.2f}%</strong></p>
                    <p>Solid performance. Consider posting more consistently to increase reach.</p>
                </div>
"""
    else:
        html += f"""
                <div class="engagement-status engagement-warning">
                    <h3>⚠️ Needs Improvement</h3>
                    <p><strong>Engagement Rate: {engagement_rate:.2f}%</strong></p>
                    <p>Focus on creating more engaging content and interacting with your audience.</p>
                </div>
"""
    
    html += """
            </div>
            
            <!-- Recent Execution Logs -->
            <div class="section">
                <h2 class="section-title">🤖 Recent Execution History</h2>
                <div class="recent-activity">
"""
    
    if recent_logs:
        for log in recent_logs[-7:]:  # Last 7 days
            html += f"""
                    <div class="activity-item">
                        <div>
                            <div class="activity-day">{log['day']}</div>
                            <div style="font-size: 0.85em; color: #666;">{log['last_run'] or 'No execution'}</div>
                        </div>
                        <div class="activity-stats">
                            <span>📝 {log['posts']} posts</span>
                            <span>💬 {log['comments']} comments</span>
                            <span>❤️ {log['likes']} likes</span>
                        </div>
                    </div>
"""
    else:
        html += """
                    <p>No recent execution data available.</p>
"""
    
    html += """
                </div>
            </div>
            
            <!-- Best Posting Times -->
            <div class="section">
                <h2 class="section-title">⏰ Optimal Posting Times</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Time</th>
                            <th>Avg Engagement</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    if best_times:
        for i, (hour, engagement) in enumerate(best_times, 1):
            time_12hr = f"{hour % 12 or 12}:00 {'PM' if hour >= 12 else 'AM'}"
            status = 'badge-success' if i == 1 else 'badge-info'
            html += f"""
                        <tr>
                            <td><strong>#{i}</strong></td>
                            <td>{time_12hr}</td>
                            <td>{engagement:.1f}</td>
                            <td><span class="badge {status}">{'Best Time' if i == 1 else 'Good Time'}</span></td>
                        </tr>
"""
    else:
        html += """
                        <tr>
                            <td colspan="4" style="text-align: center; color: #999;">Not enough data yet - keep running the bot!</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Best Days -->
            <div class="section">
                <h2 class="section-title">📅 Best Posting Days</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Day</th>
                            <th>Avg Engagement</th>
                            <th>Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    if best_days:
        for i, (day, engagement) in enumerate(best_days, 1):
            status = 'badge-success' if i == 1 else 'badge-info'
            html += f"""
                        <tr>
                            <td><strong>#{i}</strong></td>
                            <td>{day}</td>
                            <td>{engagement:.1f}</td>
                            <td><span class="badge {status}">{'Priority' if i == 1 else 'Post Here'}</span></td>
                        </tr>
"""
    else:
        html += """
                        <tr>
                            <td colspan="4" style="text-align: center; color: #999;">Not enough data yet</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Top Hashtags -->
            <div class="section">
                <h2 class="section-title">🏷️ Top Performing Hashtags</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Hashtag</th>
                            <th>Times Used</th>
                            <th>Avg Engagement</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    if top_hashtags:
        for i, (tag, stats) in enumerate(top_hashtags, 1):
            html += f"""
                        <tr>
                            <td><strong>#{i}</strong></td>
                            <td>#{tag}</td>
                            <td>{stats['uses']}</td>
                            <td>{stats['avg_engagement']:.1f}</td>
                        </tr>
"""
    else:
        html += """
                        <tr>
                            <td colspan="4" style="text-align: center; color: #999;">Start using hashtags to track performance</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Recommendations -->
            <div class="section">
                <h2 class="section-title">💡 Recommendations</h2>
                <div class="recommendations">
                    <h4>Action Items:</h4>
                    <ul>
"""
    
    # Generate dynamic recommendations
    if engagement_rate < 3:
        html += """
                        <li>📉 Engagement rate is low. Focus on creating more valuable, engaging content</li>
                        <li>🎥 Try using Reels - they get 3x more reach than regular posts</li>
                        <li>💬 Engage more with your audience in comments and DMs</li>
"""
    
    if best_times:
        top_time = best_times[0][0]
        time_12hr = f"{top_time % 12 or 12}:00 {'PM' if top_time >= 12 else 'AM'}"
        html += f"""
                        <li>⏰ Your best posting time is {time_12hr} - schedule posts around this time</li>
"""
    
    if best_days:
        top_day = best_days[0][0]
        html += f"""
                        <li>📅 {top_day} is your best performing day - prioritize posting then</li>
"""
    
    if top_hashtags:
        top_3 = ', '.join(f"#{tag}" for tag, _ in top_hashtags[:3])
        html += f"""
                        <li>🏷️ Use these high-performing hashtags: {top_3}</li>
"""
    
    html += f"""
                        <li>🤖 Bot is running automatically 7 days a week at peak engagement times</li>
                        <li>📊 Review this report daily to track your growth and optimize strategy</li>
                    </ul>
                </div>
            </div>
            
            <!-- Growth Stats -->
"""
    
    if growth['status'] == 'success':
        html += f"""
            <div class="section">
                <h2 class="section-title">📈 Growth Stats (Last 30 Days)</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Follower Growth</h3>
                        <div class="value">{growth['growth']:+,}</div>
                        <div class="label">New Followers</div>
                    </div>
                    <div class="stat-card">
                        <h3>Growth Rate</h3>
                        <div class="value">{growth['growth_rate']:+.2f}%</div>
                        <div class="label">Percentage Change</div>
                    </div>
                </div>
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="footer">
            <p><strong>Instagram Automation Bot</strong></p>
            <p>Deployed on Google Cloud Platform (GCP)</p>
            <p>Running 24/7 with AI-powered engagement</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Report generated: {report_time}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def generate_json_report(analytics, logs_dir, output_path):
    """Generate JSON report for programmatic access"""
    
    best_times = analytics.get_best_posting_times(5)
    best_days = analytics.get_best_posting_days()
    top_hashtags = analytics.get_best_hashtags(min_uses=1, top_n=10)
    activity = analytics.get_activity_summary(7)
    growth = analytics.get_follower_growth(30)
    recent_logs = get_recent_log_summary(logs_dir, 7)
    
    report_data = {
        'generated_at': datetime.now().isoformat(),
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'engagement_rate': analytics.get_engagement_rate(),
        'activity_last_7_days': activity,
        'growth_last_30_days': growth,
        'best_posting_times': [
            {'hour': hour, 'time_12hr': f"{hour % 12 or 12}:00 {'PM' if hour >= 12 else 'AM'}", 'avg_engagement': eng}
            for hour, eng in best_times
        ],
        'best_posting_days': [
            {'day': day, 'avg_engagement': eng}
            for day, eng in best_days
        ],
        'top_hashtags': [
            {'hashtag': tag, 'stats': stats}
            for tag, stats in top_hashtags
        ],
        'recent_executions': recent_logs
    }
    
    import json
    with open(output_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    return output_path


def main():
    """Generate daily report"""
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print("DAILY REPORT GENERATOR")
    print(f"{'=' * 80}{Style.RESET_ALL}")
    print(f"📅 Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"⏰ Time: {datetime.now().strftime('%I:%M %p')}")
    print()
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, 'logs')
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Create reports directory
    os.makedirs(reports_dir, exist_ok=True)
    
    # Initialize analytics
    print(f"{Fore.YELLOW}→ Loading analytics data...{Style.RESET_ALL}")
    analytics = InstagramAnalytics(data_dir=os.path.join(base_dir, 'data'))
    print(f"{Fore.GREEN}✓ Analytics loaded{Style.RESET_ALL}")
    
    # Generate timestamp for files
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    # Generate HTML report
    print(f"\n{Fore.YELLOW}→ Generating HTML report...{Style.RESET_ALL}")
    html_path = os.path.join(reports_dir, f'daily_report_{timestamp}.html')
    generate_html_report(analytics, logs_dir, html_path)
    print(f"{Fore.GREEN}✓ HTML report saved: {html_path}{Style.RESET_ALL}")
    
    # Generate JSON report
    print(f"\n{Fore.YELLOW}→ Generating JSON report...{Style.RESET_ALL}")
    json_path = os.path.join(reports_dir, f'daily_report_{timestamp}.json')
    generate_json_report(analytics, logs_dir, json_path)
    print(f"{Fore.GREEN}✓ JSON report saved: {json_path}{Style.RESET_ALL}")
    
    # Create symlinks to latest reports
    latest_html = os.path.join(reports_dir, 'latest.html')
    latest_json = os.path.join(reports_dir, 'latest.json')
    
    try:
        # Remove old symlinks if they exist
        if os.path.exists(latest_html):
            os.remove(latest_html)
        if os.path.exists(latest_json):
            os.remove(latest_json)
        
        # Create new symlinks (or copies on Windows)
        import shutil
        shutil.copy2(html_path, latest_html)
        shutil.copy2(json_path, latest_json)
        
        print(f"\n{Fore.GREEN}✓ Latest reports updated{Style.RESET_ALL}")
        print(f"   • {latest_html}")
        print(f"   • {latest_json}")
    except Exception as e:
        print(f"{Fore.YELLOW}⚠ Could not create latest report links: {e}{Style.RESET_ALL}")
    
    # Generate text summary
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print("REPORT SUMMARY")
    print(f"{'=' * 80}{Style.RESET_ALL}")
    print(analytics.generate_report())
    
    print(f"\n{Fore.GREEN}{'=' * 80}")
    print("✓ Daily report generation completed!")
    print(f"{'=' * 80}{Style.RESET_ALL}")
    print(f"\n📊 View your report:")
    print(f"   HTML: {html_path}")
    print(f"   JSON: {json_path}")
    print(f"\n💡 Latest report always available at:")
    print(f"   {latest_html}")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error generating report: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
