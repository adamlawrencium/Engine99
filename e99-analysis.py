
# coding: utf-8

# In[1]:


# !pip3 install xmltodict
# !pip3 install untangle
# !pip3 install nameparser
# !pip3 install pandas

import turicreate as gl
from turicreate import SFrame
import xmltodict, untangle
from nameparser import HumanName
import pandas as pd


# In[3]:


def get_forms(x):
    utp = untangle.parse(x)
    rdlist = dir(utp.Return.ReturnData)
    return [str(item) for item in rdlist]

def get_header_type(x):
    utp = untangle.parse(x)
    return utp.Return.ReturnHeader.ReturnType.cdata.encode('ascii')

def load_value(x,field):
    try:
        utp = untangle.parse(x)
        utp_data = utp.Return.ReturnData
        return get_value(utp_data.IRS990,field)
    except:
        return None
def get_value(source,field):
    try:
        return getattr(source,field).cdata
    except:
        return None
    
    
def get_peoplenames(x):
    try:
        utp = untangle.parse(x)
        utp_data = utp.Return.ReturnData.IRS990.Form990PartVIISectionA
        namelist = []
        for i in utp_data:
            raw_name = i.NamePerson.cdata
            name = HumanName(raw_name)
            namelist.append(str(name))
        return namelist
    except:
        print('nothin')
        return None

def get_charity_from_return_info(xml):
    dic = xmltodict.parses(xml)


# LOAD 990 DATA
sfm = SFrame('sfmain_saved/')
print(sfm['RETURN_TYPE'].unique())

# sfm['rd_type'] = sfm['return_info'].apply(lambda x: get_header_type(x))

sft = sfm.head(4000)['TAXPAYER_NAME', 'return_info']

print(sfm)

# sfbp = SFrame()
# for i in sft:
#     taxpayer_name = i['TAXPAYER_NAME']
#     peoplenames = get_peoplenames(i['return_info'])
#     if peoplenames is not None:
#         for person in peoplenames:
#             tsf = SFrame({'company': [taxpayer_name],'person':[person]})
#             sfbp = sfbp.append(tsf)

# meta = list(zip(sfm.column_names(), sfm.column_types()))

# troy = sfm.filter_by('12180','zip_code')
for filing in sfm:
	print(filing['zip_code'])



# charity = xmltodict.parse(troy[0]['return_info'])['Return']['ReturnData']

# list(charity.keys())


# xmltodict.parse(base_xml)['Return']['ReturnData']['IRS990']['Form990PartVIISectionA']