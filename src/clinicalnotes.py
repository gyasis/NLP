# %%    
#practice 

from clinitokenizer.tokenize import clini_tokenize

test = "Patient is a 34 yo male with history of COPD, w/ complaints of SOB. AOx4 with a SP02 of 91. Patient is wheezing, and speaks in two word sentences. No current history of COvid. HR 94, BP 100/80. Temp 98.6. "


sents = clini_tokenize(test)

# %%
print(sents)
# %%
