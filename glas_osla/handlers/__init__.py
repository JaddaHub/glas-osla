from .user.registration import setup_registration_handlers
from .user.expenses import setup_expenses_handlers
from .user.revenues import setup_revenues_handlers
from .user.general import setup_general_handlers
from .admin.moderate_users import setup_admin_moderation_handlers
from .user.revenues import setup_revenues_handlers
from .user.revenues import setup_revenues_handlers
from .user.circles_diagrams import setup_circles_diagrams_handlers
from .user.graphics import setup_graphics_handlers
from .user.reports import setup_reports_handlers

__all__ = ['setup_registration_handlers', 'setup_admin_moderation_handlers',
           'setup_expenses_handlers',
           'setup_general_handlers', 'setup_revenues_handlers', 'setup_circles_diagrams_handlers',
           'setup_graphics_handlers', 'setup_reports_handlers'
           ]
