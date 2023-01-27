# %%

!pip install transformers
!wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-pytorch_model.bin

# %%
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        converter = TextConverter(rsrcmgr, sio, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, converter)
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
        text = sio.getvalue()
        converter.close()
        sio.close()
        return text

pdf_text = extract_text_from_pdf('/home/gyasis/Downloads/Payment-Policies-for-Rural-Hospitals.December-2022.2.pdf')
# print(pdf_text)

 # %%
 import torch
import transformers

model = transformers.GPT2Model.from_pretrained('gpt2-pytorch_model.bin')

def generate_summary(text, max_length=120):
    input_ids = torch.tensor(model.tokenizer.encode(text)).unsqueeze(0)
    summary_ids = model.generate(input_ids, max_length=max_length, temperature=0.5, top_p=0.9, top_k=20)
    summary = model.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

pdf_text = extract_text_from_pdf('path/to/pdf.pdf')
summary = generate_summary(pdf_text, max_length=120)
print(summary)

# %%
