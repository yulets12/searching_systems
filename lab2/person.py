from yargy import rule
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline

from lab2.name import NAME

Person = fact('Person', ['profession', 'addition', 'name'])

# Профессия
PROFESSION = morph_pipeline(['художник', 'антиквар', 'ученый', 'поэт', 'историк', 'скульптор', 'архитектор'])

# Персона
PERSON = rule(
    PROFESSION.interpretation(Person.profession.inflected()),
    NAME.interpretation(Person.name)
).interpretation(Person)