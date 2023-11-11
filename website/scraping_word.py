import requests, bs4
from googletrans import Translator


from website.models import Word


def translate_word(word_english):
    translator = Translator()
    translation = translator.translate(word_english, src='en', dest='vi')
    return translation.text

def textHtml(className, soup, index):
    elements = soup.select(f'.{className}')
    if len(elements) == 0:
        return ''
    if len(elements) == 1 and index != 0:
        index = 0
    if len(elements) >= 2 and len(elements) % 2 == 0:
        index = int(len(elements)/2)
    return elements[index].getText().lower()

def translateWord(text):
    url = 'https://dictionary.cambridge.org/dictionary/english/' + text
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    pronounClassName = 'page>.pr.dictionary:first-child .ipa.dipa.lpr-2.lpl-1'
    wordClassName = '.'.join('hw dhw'.split(' '))
    typeWordClassName = '.'.join('pos dpos'.split(' '))
    word = textHtml(wordClassName, soup, 0)

    pronoun = textHtml(pronounClassName, soup, 1)
    typeWord = textHtml(typeWordClassName, soup, 0)
    try:
        meaningVietnames = translate_word(word).lower()
    except TypeError:
        return None
    # newWord = f'new Word(\"{word}\", \"{meaningVietnames}\", \"{pronoun}\", Type.{typeWord.upper()}) '
    newWord = Word(oldWord=text, word=word, meaning=meaningVietnames, pronoun=pronoun, type=typeWord)
    return newWord

def add(word, dictionary):
    newWord = Word(oldWord=word)
    if newWord in dictionary and not dictionary[dictionary.index(newWord)].isUsed:
        return None
    if newWord in dictionary and dictionary[dictionary.index(newWord)].isUsed:
        dictionary[dictionary.index(newWord)].increaseCount()
        return None
    elif newWord not in dictionary:
        newWord = translateWord(word)
        print(newWord)
        dictionary.append(newWord)
        return newWord