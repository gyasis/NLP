# %%
#time  each notebook cell execution time
%load_ext autotime

#import pyforest and other libraries    
import pyforest
# %%

df = pd.read_csv('data/train.csv')
# %%
from clinitokenizer.tokenize import clini_tokenize
 # %%
text = df.text[2]
sents = clini_tokenize(text)
# %%
def observable_tokenize(text):
    sents = clini_tokenize(text)
    print(text)
    for line in sents:
        print(line)
    return sents
# %%
#give the stats of the df like variables types, number of variables, number of observations
df.info()
# %%
#how many unique values in each text and list of unique values
print(df.label.nunique())
print(df.label.unique())
# %%
