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
#translate German to English
from transformers import MarianTokenizer, AutoModelForSeq2SeqLM

text = mainlist[0]
mname = 'malloc/OpenNMT-py-German-English-2-layer-BiLSTM'
tokenizer = MarianTokenizer.from_pretrained(mname)
model = AutoModelForSeq2SeqLM.from_pretrained(mname)
input_ids = tokenizer.encode(text, return_tensors="pt")
outputs = model.generate(input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded) #Nice to meet you
# %%
from transformers import AutoModelWithLMHead, AutoTokenizer
model = AutoModelWithLMHead.from_pretrained("malloc/OpenNMT-py-German-English-2-layer-BiLSTM")
tokenizer = AutoTokenizer.from_pretrained("malloc/OpenNMT-py-German-English-2-layer-BiLSTM")
# %%
from transformers import AutoModelWithLMHead, AutoTokenizer
model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
# %%
