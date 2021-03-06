import requests
import shutil
import os

POEDITOR_API_KEY = os.environ['POEDITOR_API_KEY']
POEDITOR_PROJECT_ID = os.environ['POEDITOR_PROJECT_ID']
ARTIFACTORY_URL = os.environ.get('ARTIFACTORY_URL', 'https://psono.jfrog.io/psono')
ARTIFACTORY_PATH = os.environ.get('ARTIFACTORY_PATH', '/psono/admin-client/languages/')
ARTIFACTORY_USER = os.environ.get('ARTIFACTORY_USER', 'gitlab')
ARTIFACTORY_PASS = os.environ['ARTIFACTORY_PASS']


LANGUAGE_CODES = [
    "af", "sq", "ar-sa", "ar-iq", "ar-eg", "ar-ly", "ar-dz", "ar-ma", "ar-tn", "ar-om",
    "ar-ye", "ar-sy", "ar-jo", "ar-lb", "ar-kw", "ar-ae", "ar-bh", "ar-qa", "eu", "bg",
    "be", "ca", "zh-tw", "zh-cn", "zh-hk", "zh-sg", "hr", "cs", "da", "nl", "nl-be", "en",
    "en-us", "en-eg", "en-au", "en-gb", "en-ca", "en-nz", "en-ie", "en-za", "en-jm",
    "en-bz", "en-tt", "et", "fo", "fa", "fi", "fr", "fr-be", "fr-ca", "fr-ch", "fr-lu",
    "gd", "gd-ie", "de", "de-ch", "de-at", "de-lu", "de-li", "el", "he", "hi", "hu",
    "is", "id", "it", "it-ch", "ja", "ko", "lv", "lt", "mk", "mt", "no", "pl",
    "pt-br", "pt", "rm", "ro", "ro-mo", "ru", "ru-mi", "sz", "sr", "sk", "sl", "sb",
    "es", "es-ar", "es-gt", "es-cr", "es-pa", "es-do", "es-mx", "es-ve", "es-co",
    "es-pe", "es-ec", "es-cl", "es-uy", "es-py", "es-bo", "es-sv", "es-hn", "es-ni",
    "es-pr", "sx", "sv", "sv-fi", "th", "ts", "tn", "tr", "uk", "ur", "ve", "vi", "xh",
    "ji", "zu", "ar", "bn"
]

WEBHOOKS = {
    'da': 'https://api.poeditor.com/webhooks/149f094ac6',
    'sv': 'https://api.poeditor.com/webhooks/cb53bc3005',
    'no': 'https://api.poeditor.com/webhooks/a44b3853dc',
    'he': 'https://api.poeditor.com/webhooks/61c796e8a6',
    'ar': 'https://api.poeditor.com/webhooks/fffae4b374',
    'hi': 'https://api.poeditor.com/webhooks/85a40635f6',
    'bn': 'https://api.poeditor.com/webhooks/53ce98d19d',
    'cs': 'https://api.poeditor.com/webhooks/fed2e677ff',
    'de': 'https://api.poeditor.com/webhooks/25c8bbdbdf',
    'en': 'https://api.poeditor.com/webhooks/2cf5b85261',
    'es': 'https://api.poeditor.com/webhooks/cf0d541a18',
    'fi': 'https://api.poeditor.com/webhooks/7d25d5f785',
    'fr': 'https://api.poeditor.com/webhooks/5991571493',
    'hr': 'https://api.poeditor.com/webhooks/218017a9ee',
    'it': 'https://api.poeditor.com/webhooks/993bb97003',
    'ja': 'https://api.poeditor.com/webhooks/29b75b89d5',
    'ko': 'https://api.poeditor.com/webhooks/386b97cba5',
    'nl': 'https://api.poeditor.com/webhooks/8c3b5a5b48',
    'pl': 'https://api.poeditor.com/webhooks/ca5738b9c7',
    'pt': 'https://api.poeditor.com/webhooks/e591ad33ed',
    'pt-br': 'https://api.poeditor.com/webhooks/6ecefa4a90',
    'ru': 'https://api.poeditor.com/webhooks/b5599e4961',
    'vi': 'https://api.poeditor.com/webhooks/4d4b47eccc',
    'zh-cn': 'https://api.poeditor.com/webhooks/8ea70c8da9',
}


def upload_language(lang):

    if lang in WEBHOOKS:
        params = (
            ('api_token', POEDITOR_API_KEY),
            ('id_project', POEDITOR_PROJECT_ID),
        )

        r = requests.post(WEBHOOKS[lang], params=params)
    else:
        print("Error: upload_language " + lang + " No webhook configured for this language")
    #     params = (
    #         ('api_token', POEDITOR_API_KEY),
    #         ('id_project', POEDITOR_PROJECT_ID),
    #         ('language', lang),
    #         ('operation', 'import_terms_and_translations'),
    #     )
    #
    #     r = requests.post('https://poeditor.com/api/webhooks/gitlab', params=params)
    if not r.ok or r.text != 'Request received':
        print("Error: upload_language " + lang)
        print(r.text)
        exit(1)
    print("Success: upload_language " + lang)

def download_language(lang):
    data = [
        ('api_token', POEDITOR_API_KEY),
        ('action', 'export'),
        ('id', POEDITOR_PROJECT_ID),
        ('language', lang),
        ('type', 'key_value_json'),
    ]

    r = requests.post('https://poeditor.com/api/', data=data)

    if not r.ok:
        print("Error: download_language")
        print(r.text)
        exit(1)

    result = r.json()

    r = requests.get(result['item'], stream=True)

    path = 'locale-'+lang+'.json'

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    print("Success: download_language " + lang)

    return path

def deploy_to_artifactory(artifactory_user, artifactory_pass, artifactory_url, path, lang, file):
    with open(file, 'rb') as f:
        r = requests.put(artifactory_url + path  + file,
                         data=f,
                         auth=(artifactory_user, artifactory_pass))
    if not r.ok:
        print("Error: get_languages")
        print(r.json())
        exit(1)
    result = r.json()
    print("Success: deploy_to_artifactory " + lang)

def get_languages():
    data = [
      ('api_token', POEDITOR_API_KEY),
      ('id', POEDITOR_PROJECT_ID),
    ]

    r = requests.post('https://api.poeditor.com/v2/languages/list', data=data)
    if not r.ok:
        print("Error: get_languages")
        print(r.json())
        exit(1)
    result = r.json()
    print(result['result']['languages'])
    return result['result']['languages']



def main():
    languages = get_languages()
    for lang in languages:
        language_code = lang['code'].lower()
        if language_code not in LANGUAGE_CODES:
            print("Error: main")
            print("Invalid Language Code " + language_code)
            exit(1)
        upload_language(language_code)
        file = download_language(language_code)
        deploy_to_artifactory(ARTIFACTORY_USER, ARTIFACTORY_PASS, ARTIFACTORY_URL, ARTIFACTORY_PATH, language_code, file)

    print("Success")

if __name__ == "__main__":
    main()