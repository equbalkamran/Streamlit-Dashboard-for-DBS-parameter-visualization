# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:09:04 2022

@author: Dell
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")
xlsx = pd.ExcelFile(r'C:\Users\Dell\Desktop\Masked_dataset2.xlsx')
all_batteries = pd.read_excel(xlsx,'All Batteries')
pd_demographics=pd.read_excel(xlsx,'PD_Demographics')
mdt_workflow= pd.read_excel(xlsx,'MDT_Workflow')
et_motor= pd.read_excel(xlsx,'ET_Motor')
pd_postop_outcomes= pd.read_excel(xlsx,'PD_Postop_outcomes')
all_physio_outcomes= pd.read_excel(xlsx,'All_Physio_outcomes')
neuropsych_outcomes= pd.read_excel(xlsx,'Neuropsych_outcomes')


all_batteries.rename({'Unnamed: 7':'Comments'},axis=1,inplace=True)
#pd_demographics.rename({'Mater MRN':'MRN'},axis=1,inplace=True)
#pd_postop_outcomes.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)


#%% 
'Streamlit Design'
st.header("Individual Patient Information Visualisation")
st.write("This application shows the data of one individual patient based on the MRN Number given by the user.")
st.subheader("The Mater Misericordiae University Hospital and School of Electronics Engineering, University College Dublin")

#%%
#list of sidebars
mrn = st.sidebar.text_input("Enter the MRN no of the patient:", "0096")
mrn=int(mrn)
col11,col12,col13,col14=st.columns(4)
col1, col2 = st.columns(2)
col11.subheader('Patient Name')
col12.subheader('MRN:'+str(mrn))
try:
    n1=all_batteries.index[all_batteries['MRN'] == mrn][0]
except IndexError:
    st.error("Patient's battery details could not be located. Please confirm in sheet 'All Batteries'")
try:
    n2=pd_demographics.index[pd_demographics['MRN'] == mrn][0]
except IndexError:
    st.error("Patient's Demographics information could not be located. Please confirm in sheet 'PD_Demographics'")
try:
    n3=pd_postop_outcomes.index[pd_postop_outcomes['MRN'] == mrn][0]
except IndexError:
    st.error("Patient's PD Outcomes data could not be located. Please comfirn in sheet 'PD_Outcomes.'")

col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write('**Age of the patient :**  '+str(pd_demographics.iloc[n2]['Age'])+' (Deidentified)')
col1.write('**Target :**  '+str(pd_postop_outcomes.iloc[n3]['Target']))
col1.write('**Age at Diagnosis :**  '+str(pd_demographics.iloc[n2]['Age Dx'])+' (Actual)')
col1.write('**Site of Surgery :**  '+str(pd_postop_outcomes.iloc[n3]['Centre']))
col1.write('**Years since Surgery :**  '+str(pd_demographics.iloc[n2]['Age']-pd_postop_outcomes.iloc[n3]['Age at surgery'])+' (negative as age is deidentified)')
col1.write('**Battery Manufacturer :**  '+str(all_batteries.iloc[n1]['Manufacturer']))

col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")
col1.write("")

timeline=["Baseline","6 months","1 year"]

w=550
h=500

led=[pd_postop_outcomes.iloc[n3]['Lpre-op LED'],pd_postop_outcomes.iloc[n3]['LED @ 6 mon'],pd_postop_outcomes.iloc[n3]['LED @ 1 yr']]
avgled=[pd_postop_outcomes['Lpre-op LED'].mean(),pd_postop_outcomes['LED @ 6 mon'].mean(),pd_postop_outcomes['LED @ 1 yr'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=led,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgled,mode='markers',name='Average Score'))
fig.update_layout(title="LED Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col2.plotly_chart(fig)


pdq=[pd_postop_outcomes.iloc[n3]['PDQ39 pre'],pd_postop_outcomes.iloc[n3]['6 mon PDQ39'],pd_postop_outcomes.iloc[n3]['1 yr PDQ39']]
avgpdq=[pd_postop_outcomes['PDQ39 pre'].mean(),pd_postop_outcomes['6 mon PDQ39'].mean(),pd_postop_outcomes['1 yr PDQ39'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=pdq,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgpdq,mode='markers',name='Average Score'))
fig.update_layout(title="PDQ 39 Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col1.plotly_chart(fig)

minibest=[pd_postop_outcomes.iloc[n3]['MiniBest'],pd_postop_outcomes.iloc[n3]['MiniBest @6mon'],pd_postop_outcomes.iloc[n3]['MiniBest @1yr']]
avgminibest=[pd_postop_outcomes['MiniBest'].mean(),pd_postop_outcomes['MiniBest @6mon'].mean(),pd_postop_outcomes['MiniBest @1yr'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=minibest,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgminibest,mode='markers',name='Average Score'))
fig.update_layout(title="Minibest Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col2.plotly_chart(fig)

off_offscore=[pd_postop_outcomes.iloc[n3]['6 mon OFF/OFF'],pd_postop_outcomes.iloc[n3]['1 yr OFF/OFF']]
avgoff_offscore=[pd_postop_outcomes['6 mon OFF/OFF'].mean(),pd_postop_outcomes['1 yr OFF/OFF'].mean()]
on_offmedscore=[pd_postop_outcomes.iloc[n3]['6 mon OFFm/Ons'],pd_postop_outcomes.iloc[n3]['1 yr on OFFm/Ons']]
avgon_offmedscore=[pd_postop_outcomes['6 mon OFFm/Ons'].mean(),pd_postop_outcomes['1 yr on OFFm/Ons'].mean()]
score= [100*(i-j)/i for i, j in zip(off_offscore, on_offmedscore)]
avgscore= [100*(i-j)/i for i, j in zip(avgoff_offscore, avgon_offmedscore)]
fig=go.Figure()
fig.add_trace(go.Scatter(x=["6 months","1 year"],y=score,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=["6 months","1 year"],y=avgscore,mode='markers',name='Average Score'))
fig.update_layout(title="Stim Only Response",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col1.plotly_chart(fig)

moca=[pd_postop_outcomes.iloc[n3]['MOCA'],pd_postop_outcomes.iloc[n3]['MOCA @ 6mon'],pd_postop_outcomes.iloc[n3]['MOCA @1yr']]
avgmoca=[pd_postop_outcomes['MOCA'].mean(),pd_postop_outcomes['MOCA @ 6mon'].mean(),pd_postop_outcomes['MOCA @1yr'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=moca,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgmoca,mode='markers',name='Average Score'))
fig.update_layout(title="MOCA Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col2.plotly_chart(fig)

offoff=[pd_postop_outcomes.iloc[n3]['UPDRS III OFF'],pd_postop_outcomes.iloc[n3]['6 mon OFF/OFF'],pd_postop_outcomes.iloc[n3]['1 yr OFF/OFF']]
avgoffoff=[pd_postop_outcomes['UPDRS III OFF'].mean(),pd_postop_outcomes['6 mon OFF/OFF'].mean(),pd_postop_outcomes['1 yr OFF/OFF'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=offoff,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgoffoff,mode='markers',name='Average Score'))
fig.update_layout(title="UPDRS III OFF/OFF Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col1.plotly_chart(fig)


pd_postop_outcomes['AIDS %'] = pd_postop_outcomes['AIDS %'].apply(pd.to_numeric, args=('coerce',))
pd_postop_outcomes['AIDS % @ 6mon'] = pd_postop_outcomes['AIDS % @ 6mon'].apply(pd.to_numeric, args=('coerce',))
pd_postop_outcomes['AIDS % @1yr'] = pd_postop_outcomes['AIDS % @1yr'].apply(pd.to_numeric, args=('coerce',))
aids=[pd_postop_outcomes.iloc[n3]['AIDS %'],pd_postop_outcomes.iloc[n3]['AIDS % @ 6mon'],pd_postop_outcomes.iloc[n3]['AIDS % @1yr']]
avgaids=[pd_postop_outcomes['AIDS %'].mean(),pd_postop_outcomes['AIDS % @ 6mon'].mean(),pd_postop_outcomes['AIDS % @1yr'].mean()]
fig=go.Figure()
fig.add_trace(go.Scatter(x=timeline,y=aids,mode='lines+markers',name='Patient Score'))
fig.add_trace(go.Scatter(x=timeline,y=avgaids,mode='markers',name='Average Score'))
fig.update_layout(title="AIDS Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=h)
col2.plotly_chart(fig)
st.warning('Some of the AIDS Scores were not available. They have been converted to 0.')

img1 = Image.open('G:\Shared drives\DBS Data Visualization\img1.png')
img2=Image.open('G:\Shared drives\DBS Data Visualization\img2.png')
col1.image(img1,caption='Shared Image 1')
col2.image(img2,caption='Shared Image 2')