import mongoengine as me
import os

MONGO_URI = os.environ.get("MONGO_URI")

class HomophonesGroup:
    def __init__(self, homophonesList):
        self.homophonesList = homophonesList
        self.audio = self.determine_audio_URL()
        self.ipa = self.determine_ipa()

    def determine_ipa(self):
        """ Return first IPA string for a list of homophones.

            If no IPA is available, return `None`
        """

        if not self.homophonesList:
            return None

        # Find first IPA string from list of homophones
        for homophone in self.homophonesList:
            if homophone['pronunciations']['IPA']:
                ipa = homophone['pronunciations']['IPA']
                return ipa
        return None

    def determine_audio_URL(self):
        """ Return first audio URL from Wiktionary for a list of homophones.

            If no audio is available, request from Google Translate
            (this URL may break anytime).
        """

        if not self.homophonesList:
            return None

        # Find any audio file from list of homophones
        # If not available, get from Google Translate (this URL may break anytime)
        audio = f"//translate.google.com.vn/translate_tts?ie=&q={self.homophonesList[0]['word']}&tl=fr-fr&client=tw-ob"
        for homophone in self.homophonesList:
            if homophone['pronunciations']['audio']:
                audio = homophone['pronunciations']['audio']

        # Return the first if there are more than one
        if isinstance(audio, list):
            return audio[0]
        else:
            return audio


### OLD
class Pronunciations(me.EmbeddedDocument):
    text = me.ListField()
    audio = me.ListField()


class RelatedWords(me.EmbeddedDocument):
    relationshipType = me.StringField()
    words = me.ListField()


class Definitions(me.EmbeddedDocument):
    partOfSpeech = me.StringField(required=True)
    text = me.ListField()
    relatedWords = me.EmbeddedDocumentListField(RelatedWords)
    examples = me.ListField()


class Word(me.Document):
    etymology = me.StringField()
    definitions = me.EmbeddedDocumentListField(Definitions, required=True)
    pronunciations = me.EmbeddedDocumentField(Pronunciations, required=True)
###

if __name__ == "__main__":
    lista = []
    homophones = HomophonesGroup(lista)
    pass
