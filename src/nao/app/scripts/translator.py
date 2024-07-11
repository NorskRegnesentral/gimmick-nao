
class Translator(object):
    language_map = { 'en': "English", 'nb': "Norwegian" }
    def __init__(self, tts, language_list = [], default_language='en'):
        self.translations = {}
        self.tts = tts
        self._language = default_language
        self.read_languages(language_list)

    def get_string(self, key):
        return self.translations[self._language][key]

    def get_language(self):
        return self._language

    def set_language(self, language):
        self._language = language

    language = property(get_language, set_language)

    def get_ttsTag(self):
        return self.language_map[self.language]

    ttsTag = property(get_ttsTag)

    def read_languages(self, languages_list):
        for language in languages_list:
            filename = 'lang/{}.txt'.format(language)
            self.translations[language] = self.read_translations(filename)

    def read_translations(self, filename):
        with open(filename, 'r') as file:
            return dict(line.strip().split('=', 1) for line in file if line.strip())

    def translated_say(self, tag):
        self.tts.setLanguage(self.ttsTag)
        self.tts.say(self.get_string(tag))

    def straight_say(self, translated_string):
        self.tts.setLanguage(self.ttsTag)
        self.tts.say(translated_string)
