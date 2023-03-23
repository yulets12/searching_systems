from natasha import MorphVocab, AddrExtractor, DatesExtractor, NamesExtractor
from yargy import Parser
from lab2.name import NAME
from lab2.person import PERSON
from lab2.work import WORK

parser = Parser(WORK)

text = open('text.txt', encoding="utf-8").read()
morph_vocab = MorphVocab()

# Сущности по готовым правилам из библиотеки
# Сущность - адрес
extractor = AddrExtractor(morph_vocab)
matches = [match.fact for match in extractor(text)]
for match in matches:
    print(match)

# Сущность - дата
extractor = DatesExtractor(morph_vocab)
matches = [match.fact for match in extractor(text)]
for match in matches:
    print(match)

# Сущность - имя
extractor = NamesExtractor(morph_vocab)
matches = [match.fact for match in extractor(text)]
for match in matches:
    print(match)

# Сущности по новым правилам
# Сущность - имя
parser = Parser(NAME)
matches = [match.fact for match in parser.findall(text)]
for match in matches:
    print(match)

# Сущность - художественная работа
parser = Parser(WORK)
matches = [match.fact for match in parser.findall(text)]
for match in matches:
    print(match)

# Сущность - персона
parser = Parser(PERSON)
matches = [match.fact for match in parser.findall(text)]
for match in matches:
    print(match)
