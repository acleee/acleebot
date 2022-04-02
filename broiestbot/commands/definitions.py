"""Lookup definitions via Wikipedia, Urban Dictionary, etc"""
import requests
from emoji import emojize
from PyMultiDictionary import MultiDictionary
from requests.exceptions import HTTPError

from clients import wiki
from config import RAPID_API_KEY
from logger import LOGGER


def get_english_definition(word: str) -> str:
    """
    Fetch English Dictionary definition for a given phrase or word.

    :param str word: Word or phrase to fetch English definition for.

    :returns: str
    """
    try:
        response = "\n\n\n"
        dictionary = MultiDictionary()
        word_definitions = dictionary.meaning("en", word)
        for i, word_type in enumerate(word_definitions[0]):
            definition = emojize(f":bookmark: {word_type}\n", language="en")
            definition += emojize(
                f":left_speech_bubble: {word_definitions[i + 1]}\n", language="en"
            )
            if i < len(word_definitions[0]):
                definition += "\n"
            response += definition
        return response
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching English definition for `{word}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", language="en")


def get_urban_definition(term: str) -> str:
    """
    Fetch Urban Dictionary definition for a given phrase or word.

    :param str term: Word or phrase to fetch UD definition for.

    :returns: str
    """
    params = {"term": term}
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.get(
            "http://api.urbandictionary.com/v0/define", params=params, headers=headers
        )
        results = req.json().get("list")
        if results:
            word = term.upper()
            results = sorted(results, key=lambda i: i["thumbs_down"], reverse=True)
            definition = (str(results[0].get("definition")).replace("[", "").replace("]", ""))[
                0:1500
            ]
            example = results[0].get("example")
            if example:
                example = str(example).replace("[", "").replace("]", "")[0:250]
                return f"{word}:\n\n {definition} \n\n EXAMPLE: {example}"
            return f"{word}:\n\n {definition}"
        return emojize(":warning: idk wtf ur trying to search for tbh :warning:", language="en")
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while trying to get Urban definition for `{term}`: {e.response.content}"
        )
        return emojize(f":warning: wtf urban dictionary is down :warning:", language="en")
    except KeyError as e:
        LOGGER.error(f"KeyError error when fetching Urban definition for `{term}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", language="en")
    except IndexError as e:
        LOGGER.error(f"IndexError error when fetching Urban definition for `{term}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", language="en")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Urban definition for `{term}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", language="en")


def wiki_summary(query: str) -> str:
    """
    Fetch Wikipedia summary for a given query.

    :param str query: Query to fetch corresponding Wikipedia page.

    :returns: str
    """
    try:
        wiki_page = wiki.page(query)
        if wiki_page.exists():
            title = wiki_page.title.upper()
            main_category = list(wiki_page.categories.values())[0].title.replace(
                "Category:", "Category: "
            )
            text = wiki_page.text
            if "disambiguation" in main_category and "Other uses" in text:
                text = text.split("Other uses")[0]
            return f"\n\n\n\n{title}: {text[0:1500]}\n \n\n {main_category}"
        return emojize(
            f":warning: bruh i couldnt find shit for `{query}` :warning:",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching wiki summary for `{query}`: {e}")
        return emojize(
            f":warning: BRUH YOU BROKE THE BOT WTF IS `{query}`?! :warning:",
            language="en",
        )


def get_english_translation(language: str, phrase: str):
    """
    Translate a phrase between languages.

    :param str language: Language to translate from into English
    :param str phrase: Message to be translated.

    :return: str
    """
    try:
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        data = {
            "q": phrase,
            "target": "en",
            "source": language,
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "application/gzip",
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "google-translate1.p.rapidapi.com",
        }
        res = requests.request("POST", url, data=data, headers=headers)
        if res.status_code == 429:
            return emojize(
                f":warning: yall translated too much shit this month now google tryna charge me smh :warning:"
            )
        return f'TRANSLATION: `{res.json()["data"]["translations"][0]["translatedText"]}`'
    except HTTPError as e:
        LOGGER.error(f"HTTPError while translating `{phrase}`: {e.response.content}")
        return emojize(
            f":warning: wtf you broke the api? SPEAK ENGLISH :warning:",
            language="en",
        )
    except KeyError as e:
        LOGGER.error(f"KeyError error while translating `{phrase}`: {e}")
        return emojize(":warning: mfer you broke bot SPEAK ENGLISH :warning:", language="en")
    except IndexError as e:
        LOGGER.error(f"IndexError error while translating `{phrase}`: {e}")
        return emojize(":warning: mfer you broke bot SPEAK ENGLISH :warning:", language="en")
    except Exception as e:
        LOGGER.error(f"Unexpected error while translating `{phrase}`: {e}")
        return emojize(":warning: mfer you broke bot SPEAK ENGLISH :warning:", language="en")
