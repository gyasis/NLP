# %%
from easyocr import Reader
reader_german = Reader(['de'])

# %%
#read an image
def read_text(image_name, model_name,in_line=True):
    
    # read data
    text = model_name.readtext(image_name, detail=0, paragraph=in_line)
    
    # Join txts writing each text in new line
    
    return '\n'.join(text)



# %%
g_text = read_text("/home/gyasis/Pictures/German_kindle.jpg", reader_german)
print(g_text)
    
# %%
#sentence tokenization from a paragraph
def tokenize_sentences(text):
    import nltk
    sentences = nltk.sent_tokenize(text)
    return sentences 