# %%
try:
    %load_ext autotime
except: 
    print("Not right architecture, \nJupyter Notebook is needed\nConsider deleting this code block")
# %%
# 1. read file (logic to determine file type)
# 2. remove duplicates and translate
# 3. export as csv file (use same file name with different extension)


# %%
#THIS SECTIONS READS THE FILE AND CREATES A LIST OF SENTENCES
# read files choices(PDF, TXT, DOCX, SRT)

# function to open and parse pdf, save to a variable for further processing
def ingest_pdf(path):
    Print("Treating this file as a pdf")
    import pdftotext
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
    pdftotext_text = "\n\n".join(pdf)
    pdftotext_text = pdftotext_text.split("\n")
    return pdftotext_text

# function to open and read txt file, save to a variable for further processing
def ingest_txt(filename):
    Print("Treating this file as a txt")
    with open(filename, encoding = "ISO-8859-1") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

# function to open word docs 
def ingest_doc(path):
    print("Treating this file as a doc")
    import docx
    #ingest document
    return docx.Document(path)
    #docx.Document("/home/gyasis/Downloads/sich.docx")

#function to read subtitle file
def ingest_srt(path):
    print("Treating this file as a srt")
    from pysubparser import parser
    subtitles = parser.parse(path)
    templist=[]
    for subtitle in subtitles:
        templist.append(subtitle.text)
    return templist

# function to read any type of file using the above functions
def ingest_text(type, path):
    if type == ".pdf":
        return ingest_pdf(path)
    elif type == ".txt":
        return ingest_txt(path)
    elif type == ".docx":
        return ingest_doc(path)
    elif type == ".srt":
        return ingest_srt(path)



# %%
# PROCESSING SECTION
# ACTUAL NLP
# So far there are two choices to translate DE and IT

def lists2df(list1, list2, title1, title2):
    df = pd.DataFrame(zip(list1, list2), columns =[title1, title2])
    return df

def translatetext(examplelist,languagetotranslate):
    from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForCausalLM, pipeline
    
    if languagetotranslate == "DE":
        model = AutoModelWithLMHead.from_pretrained("facebook/wmt19-de-en")
        tokenizer = AutoTokenizer.from_pretrained("facebook/wmt19-de-en")
        translation = pipeline("translation_de_to_en", model=model, tokenizer=tokenizer)
        
    elif languagetotranslate =="IT":
        model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-it-en")
        tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-it-en")
        translation = pipeline("translation_it_to_en", model=model, tokenizer=tokenizer)
    
    # model = AutoModelWithLMHead.from_pretrained("facebook/wmt19-de-en")
    # tokenizer = AutoTokenizer.from_pretrained("facebook/wmt19-de-en")
    # translation = pipeline("translation_de_to_en", model=model, tokenizer=tokenizer)
    
    list1 = []
    list2 = []
    
    for element in examplelist:
        list1.append(element)
        try:
            list2.append(translation(element)[0]['translation_text'])
        except:
            list2.append("null")
            
    return lists2df(list1, list2, languagetotranslate, "English")

# Now we can use spacy for NER and other NLP tasks

def n_process(x):
    import spacy
    nlp = spacy.load("de_core_news_sm")
    return nlp(x)

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
                #translation1 = (translation(token.lemma_)['translation_text'])
                return rootverb # -*- coding: utf-8 -*-, translation1
                break
            except:
                print('translation error')
                translation1 = "null"
            
            
        else:
            pass


def createrootverbcolumn(x):
        x['rootverb'] = x['German'].apply(findtypeinstring, args=("VERB",))


#split text by sentences using NLTK
def getallverbs(examplelist):
    list1=[]
    for x in examplelist:
        for  token in nlp(x):
            if token.pos_ == "VERB":
                list1.append(token.lemma_)
    
    return list1
    
def unique(examplelist):
    import numpy as np
    x = np.array(examplelist)
    x = np.unique(x)
    return x.tolist()
    

# %%
#TRANSLATION Section

def trans_todf(templist, languagetotranslate):
    
    #check for duplicates and remove
    print(f"Number of lines before removing duplicates: {len(templist)}")
    templist = unique(templist)
    print(f"Number of lines after removing duplicates: {len(templist)}")
    #check for empty strings and and print count and warning if found
    if "" in templist:
        print("Empty string found")
        templist.remove("")
    tempdf = translatetext(templist, languagetotranslate)
    
    #check dataframe for null values warn and remove row
    if tempdf['English'].isnull().values.any():
        print(f"null values found\n{tempdf[tempdf['English'].isnull().count()]}\nLength of dataframe before removing null values: {len(tempdf)}")
        tempdf = tempdf.dropna()
        print(f"Length of dataframe after removing null values: {len(tempdf)}")
        
    else:
        print("No null values found!")
    
    return tempdf

#EXPORT Section

# Export to csv
def exportcsv(df, filename):
    df.to_csv(filename, index = False, header=True)



# %%
def translate_(path,language):
    #read file
    import os
    #get filename and extension
    filename = os.path.basename(path)
    #os.path without basename
    
    file_ = os.path.splitext(filename)[0]
    fileext = os.path.splitext(filename)[1]
    text = ingest_text(fileext, path)
    path = os.path.dirname(path)
    import time
    print("Starting translation")
    print("This may take a while")
    print(path)
    
    # print(file_)
    # time.sleep(2)
    # print(fileext)
    # time.sleep(2)
    # print(text)
    # time.sleep(2)
    # print(type(text))
    #translate
    df = trans_todf(text, language)
    
    #export
    print(f"The path is {path}")
    print(f"Exporting to {path}/{file_}_{language}.csv")
    
    exportcsv(df, f"{path}/{filename}_{language}.csv")
# %%
