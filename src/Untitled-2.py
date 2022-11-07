
# %%
#open json file and save to variable
file = open('data/data.json')


#open text file and save to variable
raw_file = open('data/raw_data.txt')
#for loop for named element in json file and save to list
def convert_code (name, file):
    for i in file:
        if i['name'] == name:
            return i['code']