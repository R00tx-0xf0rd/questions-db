"""
Пакет для работы с базой данных.
"""

# Экспорт сессии
from .db_helper import get_db_session as get_db_session

# Экспорт моделей
from .models import Base as Base
from .models import Theme as Theme
from .models import Question as Question
from .models import Answer as Answer

# Экспорт CRUD-функций
from .crud import create_theme as create_theme
from .crud import get_theme_by_id as get_theme_by_id
from .crud import get_theme_by_name as get_theme_by_name
from .crud import get_all_themes as get_all_themes
from .crud import create_question as create_question
from .crud import get_question_by_id as get_question_by_id
from .crud import get_questions_by_theme_id as get_questions_by_theme_id
from .crud import create_answer as create_answer
from .crud import get_answer_by_id as get_answer_by_id
