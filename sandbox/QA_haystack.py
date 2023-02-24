# %%
from haystack.file_converter import PDFToTextConverter
 
pdf_converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=['en'])
converted = pdf_converter.convert(file_path = '/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/data/GSH_CA_OPT-0297804_Q-105749.1_LA-0000064050_Cerner Sales Order (1).pdf', meta = { 'company': 'Company_1', 'processed': False })
# %%
