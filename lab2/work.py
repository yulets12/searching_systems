from yargy import rule, or_, and_, not_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram, type

from lab2.name import NAME

Work = fact(
    'Work',
    ['definition', 'author', 'name']
)

# Определение работы
WORK_DEFINITION = morph_pipeline(['работа', 'картина', 'композиция'])

# Имя автора
AUTHOR = rule(NAME).optional()

# Название работы -
WORK_NAME = rule(
        type('RU'), # любое русское слово
).repeatable(min=1)
QUOTE_LEFT = '«'
QUOTE_RIGHT = '»'
QUOTED_WORK_NAME = rule(QUOTE_LEFT, WORK_NAME, QUOTE_RIGHT)

''' Работа '''
# Включает в себя определение работы + имя автора (опционально) + название
WORK = rule(
    WORK_DEFINITION.interpretation(Work.definition.inflected()),
    AUTHOR.interpretation(Work.author),
    QUOTED_WORK_NAME.interpretation(Work.name)
).interpretation(Work)