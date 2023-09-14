#standard libs
import pandas as pd
import numpy as np
import os
import re
import time

#tesseract libs
import fitz
# for OCR using PyTesseract
import cv2                              # pre-processing images
import pytesseract                      # extracting text from images
import numpy as np
import matplotlib.pyplot as plt         # displaying output images
from PIL import Image
import regex
import io
from pathlib import Path

# Answer key:
# 1 : Yes to footnote
# 3 : References or Bibliography or Sources of data title present
# a : appendix title present
# e : equations
# t : tables
# f : figures
# end : ends and saves

count=0

# inputs: change accordingly
journal=pd.read_csv(Path('tb_pp.csv'))
path=Path('D:\docs\Masters\Data')
#year=1946
#ofile_name='abc'+str(year)+'.csv'

# alternative using year range
year=[1940, 1990]
ofile_name='tb_pp'+str(year[0])+'_'+str(year[1])+'.csv'

existing=pd.DataFrame(columns = ['pdf_url', 'year', 'journal', 'Answer', 'id', 'page'])
convert_dict = {'pdf_url': str,
                'year': "int64",
                'journal': str,
                'Answer': str,
                'id': str,
                'page': 'int64'
                }
if os.path.exists(ofile_name)==True:
    print("The file "+ofile_name+" exists in the current directory. \nWould you like to overwrite this file or continue from where this file left off before? \nEnter 1 for overwrite, 0 for continue where the file left off.")
    indicator=input()
    if indicator.strip()=='0':
        existing=pd.read_csv(ofile_name)
    elif indicator.strip()=='1':
        print("Okay, the file will be overwritten at the end of this session")
    else:
        print("Unknown entry, killing script")
        quit()
else:
    print(ofile_name + " does not exist yet. Output from this program will be appended in this file.")

existing=existing.astype(convert_dict)
start=time.time()

journal['id']=journal['pdf_url'].str.split('/').str[-1].str.split('_').str[0]
journal['journal']=journal['pdf_url'].str.split('/').str[-2].str.split('_').str[0]
journal['page']=journal['pdf_url'].str.split('/').str[-1].str.split('-').str[-1].str.split('.').str[0].astype(int)
journal['fp']=path/(journal['pdf_url'].str.split('amazonaws.com/').str[-1].str.split(".").str[0] +".pdf")


ids=pd.DataFrame(journal[['id','year']].value_counts()).sort_values('year', ascending=True)
zoom_x = 2.0 # horizontal zoom 
zoom_y = 2.0 # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)

#remainder=journal[journal['year']==year].shape[0]
remainder=journal[(journal['year']>=year[0])&(journal['year']<=year[1])].shape[0]

list=[]

plt.ion()
plt.figure(figsize=(10, 10))
answer=None
for j in ids.index:
    select=journal[journal['id']==j[0]].sort_values(['page'])
    for i in select.index:
        #if journal.loc[i,'year']!=year:
        #    break

        # alternative using full year range
        if ((journal.loc[i,'year']>=year[0])&(journal.loc[i,'year']<=year[1]))==False:
            break
        #print(year)
        if ((existing['id'] == j[0]) & (existing['page'] == journal.loc[i,'page'])).any()==True:
            print("page " + str(journal.loc[i,'page']) + " "+str(remainder)+" pages remaining")
            remainder=remainder-1 
            continue

        print(j)
        print(journal.loc[i,'fp'])
        pdf_file=fitz.open(journal.loc[i,'fp'])
        page=pdf_file[0]
        rgb=page.get_pixmap(matrix=mat)
        pil_image=Image.open(io.BytesIO(rgb.tobytes()))
        plt.clf()
        plt.imshow(pil_image.convert('RGB'))
        print("page " + str(journal.loc[i,'page']) + " "+str(remainder)+" pages remaining")
        answer=input()
        if answer=="end":
            break
        list.insert(i, {'pdf_url': journal.loc[i,'pdf_url'],
                     'year': journal.loc[i,'year'], 
                     'journal': journal.loc[i, 'journal'], 
                     'Answer': answer,
                     'id': journal.loc[i,'id'],
                     'page': journal.loc[i,'page']})  
        remainder=remainder-1   
        count=count+1 
    if answer=="end":
        break

pd.concat([existing, pd.DataFrame(list)], ignore_index=True).to_csv(ofile_name, index=False)
end=time.time()

print(end-start)
print(count)