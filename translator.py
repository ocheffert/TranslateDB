from deep_translator import GoogleTranslator, MyMemoryTranslator
from reverso_context_api import Client


class Translator:
    def __init__(self, translator: str = "Reverso"):
        """Constructor

        Args:
            translator (str, optional): name of the translator. Defaults to "Reverso".
        """
        self.__nbRequests = 0
        self.__supportedTranslators = [GoogleTranslator.__name__,
                                       MyMemoryTranslator.__name__,
                                       "Reverso"]
        self.__src = "fr"
        self.__target = "en"
        if translator.lower() in ["google", "g"]:
            self.__translator = GoogleTranslator(source='fr', target='en')
            self.__translatorName = GoogleTranslator.__name__
        elif translator.lower() in ["mymemory", "m"]:
            self.__translator = MyMemoryTranslator(source='fr', target='en')
            self.__translatorName = MyMemoryTranslator.__name__
        elif translator.lower() in ["reverso", "r"]:
            self.__translator = Client("fr", "en")
            self.__translator2 = GoogleTranslator(source='fr', target='en')
            self.__translatorName = "Reverso"
        else:
            print("The name given is not correct, use set_translator to set it before using the translation")
            print("The method availableTranslators gives the available translator names")

    def availableTranslators(self):
        """Print the name of the supported translators
        """
        print("This supports the following translators:")
        for name in self.__supportedTranslators:
            print('- ' + name)

    def set_translator(self, translator: str, src: str, target: str):
        """Set the translator

        Args:
            translator (str): name of the new translator (full list with availableTranslators)
            src (str): source language
            target (str): target language
        """
        self.__src = src
        self.__target = target
        if translator.lower() in ["google", "g"]:
            self.__translator = GoogleTranslator(source=src, target=target)
            self.__translatorName = GoogleTranslator.__name__
        elif translator.lower() in ["mymemory", "m"]:
            self.__translator = MyMemoryTranslator(source=src, target=target)
            self.__translatorName = MyMemoryTranslator.__name__
        elif translator.lower() in ["reverso", "r"]:
            self.__translator = Client(src, target)
            self.__translatorName = "Reverso"
        else:
            print(f"You have asked to access the translator {translator} but this does not seem to be supported")
            print("Maybe you have mistyped a translator or asked a non supported one.")
            self.availableTranslators()

    def set_languages(self, src: str, target: str):
        """Set the source and target languages

        Args:
            src (str): source language
            target (str): target language
        """
        if src not in self.get_supported_languages():
            print("You are not using an accepted languages or have mistyped it")
            print("You can have the full list of supported languages via get_supported_languages")
            return
        self.__src = src
        self.__target = target
        if isinstance(self.__translator, GoogleTranslator):
            self.__translator = GoogleTranslator(source=src, target=target)
        elif isinstance(self.__translator, Client):
            self.__translator = Client(src, target)
            self.__translator2 = GoogleTranslator(source=src, target=target)
        else:
            self.__translator = MyMemoryTranslator(source=src, target=target)

    def get_supported_languages(self, translator: str = None):
        """Print the supported languages

        Args:
            translator (str, optional): name of the translator from which we
                want the supported languages, None ask for the supported
                languages of the translator chosen at this stage. Defaults to
                None.
        """
        if translator is None:
            print(self.__translator.get_supported_languages())
        elif translator.lower() in ["google", "g"]:
            print(GoogleTranslator.get_supported_languages())
        elif translator.lower() in ["reverso", "r"]:
            print("Not implemented")
        else:
            print(MyMemoryTranslator.get_supported_languages())

    def is_language_supported(self, language: str):
        """Check if a language is supported (not available for reverso)

        Args:
            language (str): the source or target language
        """
        if isinstance(self.__translator, Client):
            print("Not implemented")
        else:
            print(self.__translator.is_language_supported(language))

    def translate(self, text: str):
        """Translate the text in argument

        Args:
            text (str): text to translate

        Returns:
            str: translated text
        """
        self.__nbRequests += 1
        if isinstance(self.__translator, Client):
            try:
                res = next(self.__translator.get_translations(text))
                self.__translatorName = "Reverso"
                return res
            except StopIteration:
                res = self.__translator2.translate(text)
                self.__translatorName = GoogleTranslator.__name__
                return res
            except HTTPError:  # too much requests to reverso,
                self.__translator = GoogleTranslator(src=self.__src, target=self.__target)
        return self.__translator.translate(text)

    def get_nb_requests(self):
        """Get the number of calls to translate

        Returns:
            int: number of calls to translate
        """
        return self.__nbRequests

    def getTranslatorName(self):
        """Get the name of the translator

        Returns:
            str: name of the translator
        """
        return self.__translatorName


# Usage example :

# myTranslator = Translator()

# print(myTranslator.translate("Le but est l'apprentissage"))
