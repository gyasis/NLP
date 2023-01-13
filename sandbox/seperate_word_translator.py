# %%

import sqlite3

def create_vocab_db():
    conn = sqlite3.connect("vocab.db")
    c = conn.cursor()
    c.execute("""
                CREATE TABLE IF NOT EXISTS vocabulary 
                (unique_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                language TEXT, 
                f_word TEXT, 
                e_word TEXT, 
                word_type TEXT)
                """)
    conn.commit()
    conn.close()

# %%
import re

def add_sentence_to_vocab(sentence, language):
    # Split the sentence into individual words
    words = re.findall(r'\w+', sentence)
    for word in words:
        word_info = translate_word(word, language)
        add_vocab(None, *word_info)



# %%
import transformers
import nltk
nltk.download('averaged_perceptron_tagger')

def find_word_type(word):
    tagged_word = nltk.pos_tag([word])
    return tagged_word[0][1]

def translate_word(word, language):
    # Load a pre-trained model
    model = transformers.AutoModelForCausalLM.from_pretrained("Helsinki-NLP/opus-mt-{}-en".format(language))

    # Translate the word to English
    translated_word = model.generate(input_ids=model.encode(word))
    translated_word = model.decode(translated_word[0])

    # Determine the word type (e.g. noun, verb, adjective)
    word_type = find_word_type(translated_word)

    return (language, word, translated_word, word_type)


# %%
