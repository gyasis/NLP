# %%
import pandas as pd
import numpy as np

df = pd.read_csv("/media/gyasis/Drive 2/Data/taxonomy_all.csv", header=None)
# %%
df.columns=['Category','Description']
df.head(10)
# %%
#erase any rows with NaN
df = df.dropna(axis=0, how='any')
df = df.reset_index(drop=True)

# %%
# Keeping Main Codes to look through categories quickly
# Take a list of sentences check and check each sentence has either a Capital B or H at the beginning, and add the first 3 characters of this sentence to the beginning of the next sentence if it does not in a for loop

def check_and_add(sentences):
    i=0
    
    for i in range(len(sentences)):
        if sentences[i][0] == 'B':
            temp = sentences[i][0:3]
        elif sentences[i][0] == 'H':
            temp = sentences[i][0:3]
        else:
            sentences[i] = temp +"-"+sentences[i]  
    new_sentences = sentences
    return new_sentences

df["Category"] = check_and_add(df['Category'].tolist())
df.head()
# %%
#Combine 2 columns into 1 with a space separator
df['combined'] = df['Category'] + " " + df['Description']

# %%
subjectlist= list(df.combined)

# %%[markup]
#### End processing
# %%
sentences = subjectlist

# take input from user and determine similarity to other sentences
def similarity_class(sentencesstore,dataframe):
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    
    len(sentencesstore)
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    user_input = input("Enter a sentence: ")
    
    # torch empty cache
    torch.cuda.empty_cache()
    

    sentencesstore.append(user_input)
    len(sentencesstore)
    sentence_embeddings = model.encode(sentencesstore)
    results  = cosine_similarity(
                  [sentence_embeddings[-1]], sentence_embeddings[0:-1])
    results = list(results[0])
    dataframe['similarity'] = results
    dataframe = dataframe.sort_values(by='similarity', ascending=False)
    # grab values greater than .6
    dataframe = dataframe[dataframe['similarity'] > .6]
    print(f"There are {len(dataframe)} results greater than 60%\nThe top 10 category suggestions: {dataframe.Category.head(10)}")
    
    print(user_input)
    return dataframe

# %%
similarity_class(sentences,df)
# %%


