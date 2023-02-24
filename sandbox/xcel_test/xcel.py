# %%
# Processing
from datetime import date, timedelta
import pandas as pd
import datetime
df = pd.read_excel('~/Downloads/Team_Calender.xlsx', header=None)

# This needs to be a function
tree = [date(2023, 1, 2) + timedelta(days=i) for i in range(0, 365, 7)]
headers = ['Associates'] + tree[0:52]
df = df.rename(columns=dict(zip(df.columns, headers)))

df= df.drop([0,1])
df = df.reset_index(drop=True)

# %%



# %%
import re
import multiprocessing
import torch
from tqdm import tqdm_notebook as tqdm
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def tokenize_text(line):
    return list(map(str, nlp(line)))

# Load the text data into a list
with open('/gdrive/MyDrive/WorksWS_noheader.txt', 'r') as f:
    text_data = [line.strip() for line in f if not re.search(r'\d', line) and len(line.strip()) > 0]


# Tokenize the text data using spaCy and multiprocessing
with multiprocessing.Pool() as p:
    tokenized_lines = list(tqdm(p.imap(tokenize_text, text_data), total=len(text_data), desc="Tokenizing text data"))

# Define the vocabulary
vocab = set([word for line in tokenized_lines for word in line])
word_to_index = {word: index for index, word in enumerate(vocab)}

def one_hot_encode_line(line):
    one_hot_line = [0] * len(vocab)
    for word in line:
        one_hot_line[word_to_index[word]] = 1
    return one_hot_line

# One-hot encode the tokenized lines using multiprocessing
with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
    one_hot_lines = list(tqdm(pool.imap(one_hot_encode_line, tokenized_lines), total=len(tokenized_lines)))
    