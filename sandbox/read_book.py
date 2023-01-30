# %%
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re



def extract_text_from_epub(file_path, add_newline=True):
    book = epub.read_epub(file_path)
    text = ""
    newline_positions = []
    current_position = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content().decode("utf-8"), 'html.parser')
            for string in soup.stripped_strings:
                text += string
                current_position += len(string)
                if add_newline:
                    newline_positions.append(current_position)
                    text += '\n'
                    current_position += 1
            for tag in soup.find_all(text=lambda x: not x.strip()):
                if add_newline:
                    newline_positions.append(current_position)
                    text += '\n'
                    current_position += 1
    return text, newline_positions

def get_text_by_positions(text, newline_positions, begin=0, end=None):
    if end is None:
        end = len(newline_positions)
    elif end > len(newline_positions):
        print("Error: End position exceeds total number of newlines in text.")
        return
    begin_pos = newline_positions[begin]
    end_pos = newline_positions[end - 1]
    return text[begin_pos:end_pos]

def get_newline_positions(text, newline_positions):
    text_split = text.split('\n')
    for pos in newline_positions:
        print("Newline at position: ", pos)
        try:
            print(text_split[int(pos)])
        except:
            print("Error: Position exceeds length of text.")

def remove_n(words, seperate_spaces=True):
    if seperate_spaces:
        words = re.sub(r"(\n){5,}", ". ", text)
    return words.replace("\n", "")

def separate_by_numbers(text_x):
    return re.split("\d+\.", text_x)


# %%
file_path = "/home/gyasis/Downloads/dokumen.pub_becoming-fluent-in-german-150-short-stories-for-beginners-german-edition.pdf.epub"
text, newline_positions = extract_text_from_epub(file_path)

#check file import by printing text and newline positions
# print(get_text_by_positions(text, newline_positions, end=500))


# %%

# %%
tree = separate_by_numbers(remove_n(text))
# %%


import nltk
nltk.download('punkt')

def separate_to_sentences(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    return sentences

text = "This is the first sentence. This is the second sentence. This is the third sentence."
sentences_list = separate_to_sentences(tree[1])
print(sentences_list)

# %%
import time
for sentences in sentences_list:
    print(sentences)
    print("\n")
    time.sleep(2)
# %%
