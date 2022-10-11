# %%
import pandas as pd
# %%
# %%
import json
import pandas as pd


# %%
# print the json file and make it look pretty

def printprettyjson(filename):
    with open(filename) as f:
        data = json.load(f)
        print(json.dumps(data, indent=4, sort_keys=True))
        
# %%

printprettyjson("/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json")
# %%
with open("/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json") as f:
    data = json.load(f)
df = pd.DataFrame(data)
df.head(15)
    



# %%

tree = "/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json"
# %%
dataframe = pd.read_json("/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json")
# %%
dataframe.head(10)
# %%
len(dataframe)
# %%
dataframe.entry[0]
# %%
type(dataframe.entry[0])
# %%
len(dataframe.entry[0])
# %%
with open("/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json") as f:
    data = json.load(f)
    df1 = pd.json_normalize(data, sep = "_")
    oak = df1.to_dict(orient='records')[0]
# %%
len(df1[0])
# %%
type(df1)
# %%
df1.head(10)

# %%
len(oak)
# %%
oak(0)
# %%
type(oak)
# %%
#flatten dict(in_dict, values=, parent_key=, sep=)
for key, value in oak.items():
    print(key, value)
# %%
from collections import Mapping
from itertools import chain
from operator import add

_FLAG_FIRST = object()

def flattenDict(d, join=add, lift=lambda x:(x,)):
    results = []
    def visit(subdict, results, partialKey):
        for k,v in subdict.items():
            newKey = lift(k) if partialKey==_FLAG_FIRST else join(partialKey,lift(k))
            if isinstance(v,Mapping):
                visit(v, results, newKey)
            else:
                results.append((newKey,v))
    visit(d, results, _FLAG_FIRST)
    return results
# %%
x = flattenDict(oak)
# %%
type(x)
# len(x)
# %%
from pandas.io.json._normalize import nested_to_record
with open("/media/gyasis/Drive 2/Data/medical_data/fhir/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.json") as f:
    data = json.load(f)
    flat = nested_to_record(data, sep = "_")
# %%
print(flat)
# %%
type(flat)
# %%
len(flat)
len(flat[0])
# %%
#turn dict into pandas dataframe
df3 = pd.DataFrame.from_dict(flat)
# %%
df3.head(3)
# %%
len(df3.entry[0])
# %%
list_combined = []

for i in range(len(df3)):
    temp = flattenDict(df3.entry[i])
    list_combined.append(temp)
    # print(list_combined)
    
column1 = []
column2 = []
for x in list_combined:
    for b in range(len(x)):
        if type(x[b]) == tuple:
            print("tuple!!")
            for i in range(len(x)):
                if (i % 2) == 0:
                    column2.append(x[i])
                else:
                    column1.append(x[i])
#zip the two lists together
two = zip(column1, column2)

# two into a pandas dataframe with title and value as column names
df4 = pd.DataFrame(two, columns = ['title', 'value'])
# %%
df31 = flattenDict(df3.entry[0])
# %%
df31
# %%
len(df31)
# %%
type(df31)
# %%
for x in df31:
    print(x)
# %%
column1 = []
column2 = []
for x in df31:
    if type(x) == tuple:
        for i in range(len(x)):
            if i.odd:
                column1.append(x[i])
            elif i.even:
                column2.append(x[i])
           
            
# %%
#again to split value column into two columns
column1 = []
column2 = []
for x in df4.value:
    for b in range(len(x)):
        if type(x[b]) == tuple:
            print("tuple!!")
            for i in range(len(x)):
                if (i % 2) == 0:
                    column2.append(x[i])
                else:
                    column1.append(x[i])
#zip the two lists together
two = zip(column2, column1)
#make into a pandas dataframe
df5 = pd.DataFrame(two, columns = ['title2', 'value'])
#remove the value column and add the two new columns to the dataframe

df6 = df4.drop(columns = ['value'])
#merge dataframes df5 and df6

df7 = pd.merge(df6, df5, left_index=True, right_index=True)


# %%
#write dataframe to csv file
pd.DataFrame.to_csv(df7, "/media/gyasis/Drive 2/Data/medical_data/Alesia_Stokes_83455d94-948d-46c2-aaf0-25d07df42a68.csv")
# %%
