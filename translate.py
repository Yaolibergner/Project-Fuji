from google.cloud import translate

class DetectResult(object):
    """Contains the detection language and confidence level."""
    def __init__(self, result):
        self.confidence = result['confidence']
        self.language = result['language']
        
def detect_language(text):
    # [START translate_detect_language]
    """Detects the text's language."""
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    return DetectResult(result)

# Test the detect_language function.
detect_language('你好')

class TranslateResult(object):
    """Contains translated texts."""
    def __init__(self, result):
        self.translated_text=result['translatedText']

def translate_text(target, text):
    # [START translate_translate_text]
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    use https://cloud.google.com/translate/docs/languages 
    to get the supported languages.
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    
    return TranslateResult(result)

# Print hello world to test the translation function.
print(translate_text('zh-CN', 'hello world').translated_text)

