from .user.registration import setup_registration_handlers
from .user.expenses import setup_expenses_handlers
from .user.profile import setup_profile_handlers
from .admin.moderate_users import setup_admin_moderation_handlers

__all__ = ['setup_registration_handlers', 'setup_admin_moderation_handlers', 'setup_expenses_handlers',
           'setup_profile_handlers']
