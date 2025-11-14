"""
Popular Instagram Categories/Hashtags
Top performing categories across different niches
"""

# Top 10 Most Popular Instagram Categories
POPULAR_CATEGORIES = {
    'travel': {
        'hashtags': ['travel', 'travelgram', 'instatravel', 'wanderlust', 'vacation'],
        'description': 'Travel, destinations, adventures',
        'engagement_rate': 'High'
    },
    'fashion': {
        'hashtags': ['fashion', 'style', 'ootd', 'fashionista', 'instafashion'],
        'description': 'Fashion, outfits, style trends',
        'engagement_rate': 'Very High'
    },
    'fitness': {
        'hashtags': ['fitness', 'gym', 'workout', 'fitnessmotivation', 'health'],
        'description': 'Fitness, workouts, health',
        'engagement_rate': 'High'
    },
    'food': {
        'hashtags': ['food', 'foodie', 'instafood', 'foodporn', 'delicious'],
        'description': 'Food, cooking, restaurants',
        'engagement_rate': 'Very High'
    },
    'beauty': {
        'hashtags': ['beauty', 'makeup', 'skincare', 'beautyblogger', 'makeupartist'],
        'description': 'Beauty, makeup, skincare',
        'engagement_rate': 'Very High'
    },
    'photography': {
        'hashtags': ['photography', 'photooftheday', 'photographer', 'naturephotography', 'instagood'],
        'description': 'Photography, art, visuals',
        'engagement_rate': 'Medium'
    },
    'lifestyle': {
        'hashtags': ['lifestyle', 'lifestyleblogger', 'dailylife', 'instagood', 'instadaily'],
        'description': 'Daily life, personal moments',
        'engagement_rate': 'High'
    },
    'pets': {
        'hashtags': ['pets', 'dogsofinstagram', 'catsofinstagram', 'petlover', 'cute'],
        'description': 'Pets, animals, cute moments',
        'engagement_rate': 'Very High'
    },
    'motivation': {
        'hashtags': ['motivation', 'inspiration', 'motivationalquotes', 'success', 'mindset'],
        'description': 'Motivational content, quotes',
        'engagement_rate': 'Medium'
    },
    'luxury': {
        'hashtags': ['luxury', 'luxurylifestyle', 'billionaire', 'success', 'entrepreneur'],
        'description': 'Luxury lifestyle, success',
        'engagement_rate': 'High'
    }
}


def get_all_categories():
    """Get list of all category names"""
    return list(POPULAR_CATEGORIES.keys())


def get_category_hashtags(category):
    """
    Get hashtags for a specific category
    
    Args:
        category: Category name (e.g., 'travel', 'fashion')
        
    Returns:
        list: Hashtags for the category
    """
    if category in POPULAR_CATEGORIES:
        return POPULAR_CATEGORIES[category]['hashtags']
    return []


def get_primary_hashtag(category):
    """
    Get the primary hashtag for a category
    
    Args:
        category: Category name
        
    Returns:
        str: Primary hashtag (first in the list)
    """
    hashtags = get_category_hashtags(category)
    return hashtags[0] if hashtags else None


def get_category_info(category):
    """
    Get full information about a category
    
    Args:
        category: Category name
        
    Returns:
        dict: Category information
    """
    return POPULAR_CATEGORIES.get(category, {})


def print_categories_summary():
    """Print a formatted summary of all categories"""
    print("=" * 70)
    print("TOP 10 INSTAGRAM CATEGORIES")
    print("=" * 70)
    
    for i, (category, info) in enumerate(POPULAR_CATEGORIES.items(), 1):
        print(f"\n{i}. {category.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Engagement: {info['engagement_rate']}")
        print(f"   Hashtags: {', '.join('#' + tag for tag in info['hashtags'][:3])}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_categories_summary()
