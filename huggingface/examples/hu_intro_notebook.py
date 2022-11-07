

# %% [markdown]
##### Hugging Faces Piplines are the easiest way to quick start some NLP work.</br> You can use them to train a model, or use them to predict on a dataset.
##### The following code will show you how to use the Hugging Faces pipelines.
# %%
from transformers import pipeline
generator = pipeline("text-generation")
# %% [markdown]
###### You should noticed the default model supplied was GPT, though we could change this is the args of the generator creation

# %%
generator("...I am learning NLP because...")
# %% [markdown]
##### The results may or may not be decent but Notice the warning that the attention mask and the pad token id were not set</br> The attention mask is used to mask the attention to the padding tokens as you would need if you have inputs that are of diffenrent lengths...remember networks need the same structure and size for the tensor operations. The pad token id is used to pad the input to the model
# %%
# you can also load any tokenizer or model that hugginface supports and load those in the pipeline
# like this
# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
# model = AutoModelForCausalLM.from_pretrained("distilgpt2")
# from transformers import pipeline
# generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
# %%
