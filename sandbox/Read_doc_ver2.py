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
    time.sleep(0.5)
    
    
    
    
    
    
    
    
    
# %%
punc
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
from transformers import pipeline
model_checkpoint = "malloc/OpenNMT-py-German-English-2-layer-BiLSTM"
translator = pipeline("translation_en_to_de", model=model_checkpoint)
# %%



# %%
