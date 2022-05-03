from .user.registration import setup_registration_handlers
from .user.expenses import setup_expenses_handlers
from .user.revenues import setup_revenues_handlers
from .user.general import setup_general_handlers
from .admin.moderate_users import setup_admin_moderation_handlers
from .user.revenues import setup_revenues_handlers

__all__ = ['setup_registration_handlers', 'setup_admin_moderation_handlers',
           'setup_expenses_handlers', 'setup_revenues_handlers',
           'setup_general_handlers', 'setup_revenues_handlers']
