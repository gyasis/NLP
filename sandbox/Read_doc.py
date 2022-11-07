# %%
import docx
doc = docx.Document("/home/gyasis/Downloads/sich.docx")

# %%
import time

# %%
mainlist = []
for para in doc.paragraphs:
    temp = para.text
    #if string has "/", split into list
    if "/" in temp:
        temp = temp.split("/")
        #print(temp)
        for x in temp:
            mainlist.append(x)
    else:
        mainlist.append(temp)

for element in mainlist:
    print(element)

# %%
#if string has "?","." split into list and append to punc_list
def split_by_sep(sep, string):
    punc_list = []
    if sep in string:
        string = string.split(sep)
        for x in string:
            punc_list.append(x)
    else:
        punc_list.append(string)
    return punc_list
    
    
finalsplit =  []


# %%
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForCausalLM, pipeline

model = AutoModelWithLMHead.from_pretrained("facebook/wmt19-de-en")
tokenizer = AutoTokenizer.from_pretrained("facebook/wmt19-de-en")
translation = pipeline("translation_de_to_en", model=model, tokenizer=tokenizer)

# %%
list1 = []
list2 = []
for element in mainlist:
    
    list1.append(element)
    try:
        list2.append(translation(element)[0]['translation_text'])
    except:
        list2.append("null")

# %%
def lists2df(list1, list2, title1, title2):
    df = pd.DataFrame(zip(list1, list2), columns =[title1, title2])
    return df

# %%

dframe1 = lists2df(list1, list2,"German", "English")
# %%
# Now we can use spacy for NER and other NLP tasks

import spacy
nlp = spacy.load("de_core_news_sm")

def n_process(x):
    return nlp(x)
    
    
# %%
dframe1.head(10)
# %%
doc = n_process(dframe1.German[2])
# %%
for token in doc:
    print(token.text, token.pos_, token.lemma_)


# %%
def findverbinstring(string):
    import spacy
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(string)
    for token in doc:
        if token.pos_ == "VERB":
            rootverb = (token.lemma)
            try:
                translation1 = (translation(token.lemma)['translation_text'])
            except:
                translation1 = "error"
            return rootverb, translation1
            BREAK
        else:
            rootverb= ("null")
            translation1 = ("null")
    return rootverb, translation1


# %%
tree['rootverb'] = tree['German'].apply(findverbinstring)

# %%
# function to open and parse pdf, save to a variable for further processing
def pdf2text(path):
    import pdftotext
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
    pdftotext_text = "\n\n".join(pdf)
    return pdftotext_text


# %%
# function to open and read txt file, save to a variable for further processing

def seperate_lines(filename):
    with open(filename, encoding = "ISO-8859-1") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


# %%
a = pdf2text('/home/gyasis/Downloads/Verbkonjugation.pdf')
# %%
a
# %%
b = seperate_lines('/home/gyasis/Downloads/german_lesson.txt')
# %%
b

# %%
#seperate lines by \n into list
a = a.split("\n")
# %%
a
# %%
a=a[8:]
# %%
a
# %%
b
# %%
#create function loop through list and delete list items by list of strings

def delete_list_items(list1, list2):
    
    for line_ in list1:
        for item in list2:
            # list1 = [x for x in list1 if x != item]
            if item in line_:
                list1.remove(line_)            
    
    return list1

# %%
items2delete= ["from", "https://"]
c = delete_list_items(b, items2delete)
# %%
b
# %%
#comvbine list a and b

d = a + b
# %%
list1 = []
list2 = []
for element in d:
    
    list1.append(element)
    try:
        list2.append(translation(element)[0]['translation_text'])
    except:
        list2.append("null")

# %%
tree = lists2df(list1, list2,"German", "English")
# %%
