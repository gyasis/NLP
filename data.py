# %%
import pandas as pd
from pyforest import *
lazy_imports()
from transformers import AutoTokenizer

# %%
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# %%
#LOAD AND TRANSFORM DATA
df = pd.read_csv('/media/gyasis/Drive 2/Data/companies_sorted.csv')

df.head()
# %%
df2 = pd.read_csv('/media/gyasis/Drive 2/Data/us_companies.csv')
# %%

df2.head()
# %%
df2.columns
# %%
df2.description.head(10)
# %%

import re
from sklearn.model_selection import train_test_split


# # 
for i in range(len(df2)):
    df2['description'][i] = (df2['description'][i]).replace((df2['company_name'][i]), "Company")

# %%

train, test = train_test_split(df2, test_size=0.2)



# %%
# combine df2 description into text file
def build_text_file(x,y,path):
    f = open(path, "w")
    temp = x[y]
    #join all text in list into one variable as string with space between elements of list
    temp = ' '.join(temp)
    f.write(temp)
    return temp

build_text_file(train, 'description', 'train.txt')
build_text_file(test, 'description', 'test.txt')

# %%
print(f"Length of Train is {len(train)}\nLength of Test is {len(test)}")
# %%
#SETUP AND TRAIN
tokenizer = AutoTokenizer.from_pretrained("gpt2")

train_path = 'train.txt'
test_path = 'test.txt'

from transformers import GPT2Tokenizer, DataCollatorForLanguageModeling, DataProcessor, GPT2DoubleHeadsModel, TextDataset

def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(tokenizer, train_path, block_size=128)
    test_dataset = TextDataset(tokenizer, test_path,  block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm = False)
    return train_dataset, test_dataset, data_collator


train_dataset,test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)

# %% 
device = "cuda:1"
# %%
from transformers import Trainer, TrainingArguments, AutoModelWithLMHead

model = AutoModelWithLMHead.from_pretrained("gpt2")

training_args = TrainingArguments(
    output_dir="./gpt2-gerchef", #The output directory
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=30, # number of training epochs
    per_device_train_batch_size=64, # batch size for training
    per_device_eval_batch_size=64,  # batch size for evaluation
    eval_steps = 400, # Number of update steps between two evaluations.
    save_steps=800, # after # steps model is saved
    warmup_steps=500,# number of warmup steps for learning rate scheduler
    evaluation_strategy="epoch", # evaluation strategy, can be "steps" or "epochs"
    )

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    # prediction_loss_only=True,
)
# %%
trainer.train()
# %%
trainer.save_model()



# %%

from transformers import pipeline

chef = pipeline('text-generation',model='/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/sandbox/gpt2-gerchef',tokenizer='gpt2')


# %%
import numpy as np
from datasets import load_metric

metric = load_metric("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# %%
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics,
)
trainer.evaluate()