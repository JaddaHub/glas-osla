from .user.registration import setup_registration_handlers
from .admin.moderate_users import setup_admin_moderation_handlers

__all__ = ['setup_registration_handlers', 'setup_admin_moderation_handlers']
