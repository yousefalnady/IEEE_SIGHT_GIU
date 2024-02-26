
#pip install googletrans==4.0.0-rc1

from googletrans import Translator
translator = Translator()
text = 'cup'
print(translator.translate(text, dest='ar'))