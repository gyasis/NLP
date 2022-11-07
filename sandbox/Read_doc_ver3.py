# %%
%load_ext autotime
# %%
import docx
doc = docx.Document("/home/gyasis/Downloads/sich.docx")

# %%

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
def translatetext(examplelist):
    list1 = []
    list2 = []
    for element in examplelist:
        
        list1.append(element)
        try:
            list2.append(translation(element)[0]['translation_text'])
        except:
            list2.append("null")
            
    return lists2df(list1, list2,"German", "English")

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
#save as csv
dframe1.to_csv("/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/doc/German1.csv") 


# %%
dframe1.isnull().count()
# %%
df = dframe1.dropna()
# %%
doc = n_process(dframe1.German[2])
# %%
for token in doc:
    print(token.text, token.pos_, token.lemma_)


# %%
# %%
def findtypeinstring(stringf, typef):
    list1 = []
    for token in nlp(stringf):
        if token.pos_ == typef:
            list1.append(token.lemma_)
    return list1


# %%
def findtypeinstring(stringf, typef):
    import spacy
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(stringf)
    print(doc)
    for token in doc:
        print(token.text, token.pos_, token.lemma_)
        if token.pos_ == typef:
            rootverb = (token.lemma_)
            # print(rootverb)
            try:
                translation1 = (translation(token.lemma_)['translation_text'])
                return rootverb, translation1
                break
            except:
                print('translation error')
                translation1 = "null"
            
            
        else:
            # rootverb= ("null")
            # translation1 = ("null")
            # print(rootverb)
            # return rootverb, translation1
            pass


# %%
def createrootverbcolumn(x):
        x['rootverb'] = x['German'].apply(findverbinstring)

# %%
createrootverbcolumn(df)



# %%

#split text by sentences using NLTK
def getallverbs(examplelist):
    list1=[]
    for x in examplelist:
        for  token in nlp(x):
            if token.pos_ == "VERB":
                list1.append(token.lemma_)
    
    return list1
    
    
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
varX = seperate_lines("/home/gyasis/Downloads/german2.txt")
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
items2delete= ["from","From","https://", "Everyone"]
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
def create_frame(oak):
    list1 = []
    list2 = []
    for element in oak:
        
        list1.append(element)
        try:
            list2.append(translation(element)[0]['translation_text'])
        except:
            list2.append("null")
            
    return lists2df(list1, list2,"German", "English")
# %%
willow = create_frame(d)
maple = create_frame(varX)
# %%
# from the dataframe tree in the clolumn German, if "From" is found delete row

def delete_row(df, column, string):
    df = df[df[column].str.contains(string) == False]
    return df


# %%
df = delete_row(tree, "German", "From")
# %%
#searh through list and get the first element in each tuple and append to another list

def unique(examplelist):
    import numpy as np
    x = np.array(examplelist)
    x = np.unique(x)
    return x.tolist()
    

def grab_verbs(list1):
    list2 = []
    
    for element in list1:
        try:
            if element[0] != "null":
                list2.append(element[0])
        except:
            pass
    #check list2 for duplicates and remove
    list2 = unique(list2)
    
    return list2
# %%
listofverbs = grab_verbs(tree['rootverb'])
# %%
#process subtitle text file

def ingest_txt(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content
# %%
oak = ingest_txt('/home/gyasis/Downloads/Dark0101.srt')
# %%
from pysubparser import parser

subtitles = parser.parse('/home/gyasis/Downloads/Dark0101.srt')

for subtitle in subtitles:
    print(subtitle.text)
# %%
import subtitle_parser

with open('/home/gyasis/Downloads/Dark0101.srt', 'r') as input_file:
    parser = subtitle_parser.SrtParser(input_file)
    parser.parse()
    
parser.print_warnings()

for subtitles in parser.subtitles:
    print(subtitles.text)
# %%
#drop list elements that have part of a string
oak = [x for x in oak if "-->" not in x]
# %%
oak = oak[2:]
# %%
oak = [x for x in oak if "" not in x]
# %%
for item in oak:
    print(type(item))
# %%
#change elements in list to int with try and except
willow = []
for x in oak:
    try:
        willow.append(int(x))
    except:
        willow.append(x)
# %%
#if lenght of element is 0, delete element from list

oak = [x for x in oak if len(x) != 0]
# %%

# %%
#loop through elements in list and if element is int creat new list and append every element after int to new list until then next int is found


# %%
def listsoflist(originallist):
    newlist = []
    intermediatelist = []
    for element in originallist:
        if type(element) == int:
            try:
                newlist.append(intermediatelist)
                intermediatelist = []
                intermediatelist.append(element)
            except:
                print('error')
                intermediatelist =[]
                intermediatelist.append(element)
                
        else:
            intermediatelist.append(element)
    newlist.append(intermediatelist)
    return newlist
            
            
            
    
# %%
#remove all int from list
def removeint(list1):
    newlist = []
    for element in list1:
        if type(element) != int:
            newlist.append(element)
    return newlist
# %%
pine = removeint(willow)
# %%
def translatelist(alist):
    from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForCausalLM, pipeline

    model = AutoModelWithLMHead.from_pretrained("facebook/wmt19-de-en")
    tokenizer = AutoTokenizer.from_pretrained("facebook/wmt19-de-en")
    translation = pipeline("translation_de_to_en", model=model, tokenizer=tokenizer)

    list1 = []
    list2 = []
    for element in alist:
        
        list1.append(element)
        try:
            list2.append(translation(element)[0]['translation_text'])
        except:
            list2.append("null")
            
    return lists2df(list1, list2,"German", "English")
    
# %%
a = willow[pd.isnull(willow).any(axis=1)]
a# %%

# %%
def nans(df): return df[df.isnull().any(axis=1)]
# %%
nans(willow)
# %%
willow = willow.dropna()
# %%
def check_nulls(dataframe):
    length = len(dataframe)
    list1 = []
   
    for column in (dataframe.columns):
        print(column)
          
        for i, element in enumerate(dataframe[column]):
            try:
                if len(dataframe[column][i]) < 1:
                    list1.append(i)
            except:
                print('error')
    list1 = [int(x) for x in list1]
    return list1
                
# %%
tree = [int(x) for x in tree]
# %%
willow.iloc[tree]
# %%
# select rows with not index in list
df_new = willow[~willow.index.isin(tree)]
# %%
df_new.to_csv('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/doc/german_1.csv')
# %%
df2 = check_nulls(pine)
# %%
df2 = [int(x) for x in df2]
# %%
pine.iloc[df2]
# %%
pine = pine[~pine.index.isin(df2)]
# %%
pine.to_csv('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/doc/german_2.csv')
# %%
df3 = delete_row(maple, "German", "From")
# %%
li = check_nulls(df3)
# %%
maple = maple[~maple.index.isin(li)]
# %%
maple = delete_row(maple, "German", "From")
# %%
maple.to_csv('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/doc/german_3.csv')
# %%
