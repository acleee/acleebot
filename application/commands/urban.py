import requests


def urban_dictionary_defintion(word):
    params = {'term': word}
    req = requests.get('http://api.urbandictionary.com/v0/define', params=params)
    if len(req.json()['list']):
        definition = str(req.json()['list'][0]['definition'])[0:300] + '...'
        example = str(req.json()['list'][0]['example'])
        word = req.json()['list'][0]['word'].upper()
        return f"{word}: {definition}. EXAMPLE: '{example}'"
    else:
        return 'word not found :('
