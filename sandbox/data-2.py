
# %%
# Thats not working so we will now  use another dataset
# first import glob to seperate filetypes 
import glob
# grab just .al FileS an make sure they are in the right order
alignedset_en = glob.glob("/home/gyasis/Downloads/txt/*.en.al")
alignedset_de = glob.glob("/home/gyasis/Downloads/txt/*.de.al")

#for each element extract a datetime object and append to list
def get_datetime_from_filename(filename):
    import datefinder
    datetime = []
    for element in filename:
        datetime.append(next(datefinder.find_dates(element)))
    return datetime

# %%
# 
#put to lists into pandas dataframe
def lists2dataframe(list1, list2, title1, title2):
    df = pd.DataFrame(zip(list1, list2), columns =[title1, title2])
    return df
# %%
dframe = lists2dataframe(alignedset_de, alignedset_en, "German", "English")
# %%
#now we need to extract the date from the filename to make sure its they are sorted properly and matched
dframe['german_date'] = get_datetime_from_filename(alignedset_de)
dframe['english_date'] = get_datetime_from_filename(alignedset_en)

#quickly split the dataframe into two seperate dataframes
df1 = dframe[['german_date', 'German']]
df2 = dframe[['english_date', 'English']]
 # %%
#make sure the dates are datetime objects and sort dataframes by date

df1 = df1.sort_values(by='german_date')
df2 = df2.sort_values(by='english_date')
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

# concat the two dataframes 
sorted_data = pd.concat([df1, df2], axis=1)
sorted_data.head(10)
# %%
#open file and seperate each line into a list

def seperate_lines(filename):
    with open(filename, encoding = "ISO-8859-1") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content
# %%
seperate_lines(sorted_data.English[0])
# %%
def build_datalists(x):
    build_list = []
    for i in range(len(x)):
    
        for element in seperate_lines(x[i]):
            build_list.append(element)
    print(f"list has {len(build_list)} elements")        
    return build_list
# %%
German = build_datalists(sorted_data.German)
# %%
English = build_datalists(sorted_data.English)
# %%
thedataframe = lists2dataframe(German, English, "German", "English")
# %%
thedataframe = thedataframe[thedataframe["German"].str.contains("<DOC") == False]
# %%
thedataframe.head(20)
# %%
from transformers import pipeline
model_checkpoint = "facebook/wmt19-de-en"
translator = pipeline("translation_de_to_en", model=model_checkpoint, tokenizer=model_checkpoint)
# %%
# %%
#use transformers to translate the german text to english

# %%
from transformers import AutoModelWithLMHead, AutoTokenizer, AutoModelForCausalLM, pipeline

model = AutoModelWithLMHead.from_pretrained("facebook/wmt19-de-en")
tokenizer = AutoTokenizer.from_pretrained("facebook/wmt19-de-en")
translation = pipeline("translation_de_to_en", model=model, tokenizer=tokenizer)
# %%
