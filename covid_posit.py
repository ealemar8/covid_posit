#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import json
import pandas as pd
import requests
from datetime import datetime
import re
import string
import timestamp

# In[]:

# get test data
resp=requests.get('https://bioportal.salud.gov.pr/api/administration/reports/orders/basic')
pruebas = pd.DataFrame(resp.json(), columns = ['patientId', 'collectedDate', 'reportedDate', 
                                            'ageRange', 'testType', 'result', 'region', 
                                             'orderCreatedAt', 'resultCreatedAt'])
                                             
# positivity variables
pruebas['positivity_bin']='Negative'
pruebas.loc[pruebas['result'].str.contains('Positive'), 'positivity_bin'] = 'Positive'

# date and year column
pruebas['date']=pruebas['reportedDate'].str.extract(pat='(\d\d\d\d-\d\d-\d\d)')
pruebas['year'] = pruebas['date'].astype(str).str[:4]

# filter out no-sense years
years = ['2020', '2021']
pruebas = pruebas[pruebas.year.isin(years)]

# format as date
pruebas['date']=pd.to_datetime(pruebas['date'], infer_datetime_format=True)

# time series of results
posit_dat = pd.crosstab(pruebas['date'], pruebas['result'].fillna('n/a'))

# positivity rate
#posit_dat['posit_rate'] = (posit_dat['Positive']/(posit_dat['Positive']+posit_dat['Negative']))*100 

 # upload
import ezsheets
ss = ezsheets.Spreadsheet('1tOJT0haxfLiUE9o0SXworIsthL0-gw_3sNnOI2o-0OA')
sheet = ss[0]

# names
rows = sheet.getRows()
rows[0][1:]=posit_dat.columns.tolist()

# update
length = range(len(posit_dat))
for i in length:
    rows[i+1][1:]=posit_dat.iloc[i].tolist()
sheet.updateRows(rows)



# %%
