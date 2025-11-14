"""
Core modules for Instagram automation
"""
from .config import Config
from .browser_setup import BrowserManager
from .actions import InstagramActions
from .safety import SafetyManager
from .humanize import HumanBehavior
from .ai_comments import AICommentGenerator
from .categories import POPULAR_CATEGORIES, get_primary_hashtag, get_all_categories

__all__ = [
    'Config',
    'BrowserManager',
    'InstagramActions',
    'SafetyManager',
    'HumanBehavior',
    'AICommentGenerator',
    'POPULAR_CATEGORIES',
    'get_primary_hashtag',
    'get_all_categories'
]
