from django import template

register = template.Library()

censored_words = ['редиска', 'редиски']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("фильтр только для строк")

    words = value.split()
    for i, word in enumerate(words):
        if word.lower() in censored_words:
            words[i] = '*' * len(word)
    return ' '.join(words)
