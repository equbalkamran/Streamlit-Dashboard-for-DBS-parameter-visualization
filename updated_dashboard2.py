# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:55:09 2022

@author: Dell
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")
xlsx = pd.ExcelFile('Masked_dataset.xlsx')
all_batteries = pd.read_excel(xlsx,'All Batteries')
pd_demographics=pd.read_excel(xlsx,'PD_Demographics')
mdt_workflow= pd.read_excel(xlsx,'MDT_Workflow')
et_motor= pd.read_excel(xlsx,'ET_Motor')
pd_postop_outcomes= pd.read_excel(xlsx,'PD_Postop_outcomes')
all_physio_outcomes= pd.read_excel(xlsx,'All_Physio_outcomes')
neuropsych_outcomes= pd.read_excel(xlsx,'Neuropsych_outcomes')

#all_batteries.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)
#all_batteries.rename({'Unnamed: 7':'Comments'},axis=1,inplace=True)
#pd_demographics.rename({'Mater MRN':'MRN'},axis=1,inplace=True)
#pd_postop_outcomes.rename({'MMUH MRN':'MRN'},axis=1,inplace=True)

#%% 
'Streamlit Design'
st.header("Individual Patient Information Visualisation")
st.write("This application shows the data of one individual patient based on the MRN Number given by the user.")
st.subheader(" School of Electronics Engineering, University College Dublin and The Mater Misericordiae University Hospital")
#%%
#list of sidebars
battery=st.sidebar.checkbox('Show Battery Information')
demo=st.sidebar.checkbox('Show Demographic Information')
dashboard=st.sidebar.checkbox('Dashboard')
edit=st.sidebar.checkbox('Edit Patient Data')
mrn = st.sidebar.text_input("Enter the MRN no of the patient:", "0096")
mrn=int(mrn)
col1, col2 = st.columns(2)
if battery:    
    try:
        col1.subheader('Patient Details')
        n1=all_batteries.index[all_batteries['MRN'] == mrn][0]
        col1.write('**Name: John/Jane Doe**')
        col1.write('**Disgnosis : **'+all_batteries.iloc[n1]['Diagnosis']+'**                       Manufacturer:**'+all_batteries.iloc[n1]['Manufacturer'])
        col1.write('**Battery details:**')
        col1.write(all_batteries.iloc[n1]['V'])
        col1.write(all_batteries.iloc[n1]['Details'])
        col1.write(all_batteries.iloc[n1]['Unnamed: 7'])
    except IndexError:
        col1.error("Patient's battery details could not be located. Please confirm in sheet 'All Batteries'")
if demo:
    try:
        col2.subheader('Demographic Information')
        n2=pd_demographics.index[pd_demographics['MRN'] == mrn][0]
        col2.write('**Year of Diagnosis :** '+str(pd_demographics.iloc[n2]['Year Dx']))
        col2.write('**Age at Diagnosis :**  '+str(pd_demographics.iloc[n2]['Age Dx']))
        col2.write('**Year of DBS :** '+str(pd_demographics.iloc[n2]['Year of DBS']))
        col2.write('**Age at DBS :**  '+str(pd_demographics.iloc[n2]['Year Dx']))
        col2.write('**Year of Diagnosis to DBS :** '+str(pd_demographics.iloc[n2]['Yrs Dx to DBS'])+" Years")
        col2.write('**Surgical Site :** '+str(pd_demographics.iloc[n2]['Surgical site']))
        col2.write('**Diagnosis :** '+str(pd_demographics.iloc[n2]['Diagnosis.1']))
    except IndexError:
        col2.error("Patient's Demographics information could not be located. Please confirm in sheet 'PD_Demographics'")
st.write('_____________________________________________________________________________________________________________________________')

if dashboard:
    st.subheader('Dashboard')
    photos=st.sidebar.checkbox('View Images')
    try:
        n3=pd_postop_outcomes.index[pd_postop_outcomes['MRN'] == mrn][0]
        if type(pd_postop_outcomes.iloc[n3]['Surgical date'])!=str:
            st.write('**Date of Surgery : **'+pd_postop_outcomes.iloc[n3]['Surgical date'].strftime("%m/%d/%Y"))
        else:
            st.write('Date of SUrgery : Not Available ')
        timeline=["Post Surgery","6 months","1 year"]
        updrs1=pd_postop_outcomes[["UPDRS I","UPDRS I.1","UPDRS I.2"]].iloc[n3]
        updrs2=pd_postop_outcomes[["UPDRS II","UPDRS II.1","UPDRS II.2"]].iloc[n3]
        pdq39=pd_postop_outcomes[["PDQ39 pre","6 mon PDQ39","1 yr PDQ39"]].iloc[n3]
        minibest=pd_postop_outcomes[["Balance:MiniBest","MiniBest @6mon","MiniBest @1yr"]].iloc[n3]
        sltdemo=[15,20,25]
        updrs1=[pd_postop_outcomes.iloc[n3][5],pd_postop_outcomes.iloc[n3][20],pd_postop_outcomes.iloc[n3][38]]
        updrs2=[pd_postop_outcomes.iloc[n3][6],pd_postop_outcomes.iloc[n3][21],pd_postop_outcomes.iloc[n3][39]]
        updrs_off_off=[pd_postop_outcomes.iloc[n3][7],pd_postop_outcomes.iloc[n3][22],pd_postop_outcomes.iloc[n3][40]]
        updrs_off_on=[np.nan,pd_postop_outcomes.iloc[n3][23],pd_postop_outcomes.iloc[n3][41]]
        updrs_on_off=[np.nan,pd_postop_outcomes.iloc[n3][24],pd_postop_outcomes.iloc[n3][42]]
        updrs_on_on=[pd_postop_outcomes.iloc[n3][8],pd_postop_outcomes.iloc[n3][25],pd_postop_outcomes.iloc[n3][43]]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=timeline, y=updrs_off_off,mode='lines+markers',name='UPDRS III OFF/OFF'))
        fig.add_trace(go.Scatter(x=timeline, y=updrs_on_on,mode='lines+markers',name='UPDRS III ON/ON'))
        fig.add_trace(go.Scatter(x=timeline, y=updrs_off_on,mode='lines+markers',name='UPDRS III OFF/ON'))
        fig.add_trace(go.Scatter(x=timeline, y=updrs_on_off,mode='lines+markers',name='UPDRS III ON/OFF'))
        col1, col2,col3 = st.columns(3)
        #w=615
        w=450
        fig.update_layout(title="UPDRS III Scores",xaxis_title="Timeframe",yaxis_title="Score",width=w,height=400)
        col3.plotly_chart(fig)
        col3.write("*Cohort count : Too many values to count*")
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=timeline,y=updrs2,mode='lines+markers',name='Patient Score'))
        fig.add_trace(go.Scatter(x=timeline, 
                                 y=[pd_postop_outcomes['UPDRS II'].mean(),pd_postop_outcomes['UPDRS II.1'].mean(),pd_postop_outcomes['UPDRS II.2'].mean()]
                                 ,mode='lines+markers',name='Average Score'))
        fig.update_layout(title="UPDRS II Scores",xaxis_title="Timeframe",yaxis_title="Score",width=w,height=400)
        col2.plotly_chart(fig)
        col2.write('*Cohort count:*'+str([pd_postop_outcomes['UPDRS II'].count(),pd_postop_outcomes['UPDRS II.1'].count(),pd_postop_outcomes['UPDRS II.2'].count()]))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=timeline,y=updrs1,mode='lines+markers',name='Patient Score'))
        fig.add_trace(go.Scatter(x=timeline, 
                                 y=[pd_postop_outcomes['UPDRS I'].mean(),pd_postop_outcomes['UPDRS I.1'].mean(),pd_postop_outcomes['UPDRS I.2'].mean()]
                                 ,mode='lines+markers',name='Average Score'))
        fig.update_layout(title="UPDRS I Scores",xaxis_title="Timeframe",yaxis_title="Score",width=w,height=400)
        col1.plotly_chart(fig)
        col1.write('*Cohort count:*'+str([pd_postop_outcomes['UPDRS I'].count(),pd_postop_outcomes['UPDRS I.1'].count(),pd_postop_outcomes['UPDRS I.2'].count()]))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=timeline,y=pdq39,mode='lines+markers',name='Patient Score'))
        fig.add_trace(go.Scatter(x=timeline, y=[pd_postop_outcomes['PDQ39 pre'].mean(),pd_postop_outcomes['6 mon PDQ39'].mean(),pd_postop_outcomes['1 yr PDQ39'].mean()]
                                 ,mode='lines+markers',name='Average Score'))
        fig.update_layout(title="PDQ39 Results",xaxis_title="Timeframe",yaxis_title="Score",width=w,height=400)
        col1.plotly_chart(fig)
        col1.write('*Cohort count:*'+str([pd_postop_outcomes['PDQ39 pre'].count(),pd_postop_outcomes['6 mon PDQ39'].count(),pd_postop_outcomes['1 yr PDQ39'].count()]))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=timeline,y=minibest,mode='lines+markers',name='Patient Score'))
        fig.add_trace(go.Scatter(x=timeline, y=[pd_postop_outcomes['Balance:MiniBest'].mean(),pd_postop_outcomes['MiniBest @6mon'].mean(),pd_postop_outcomes['MiniBest @1yr'].mean()]
                                 ,mode='lines+markers',name='Average Score'))
        fig.update_layout(title="MiniBest (Balance) Results",xaxis_title="Timeframe",yaxis_title="Score",width=w,height=400)
        col2.plotly_chart(fig)
        col2.write('*Cohort count:*'+str([pd_postop_outcomes['Balance:MiniBest'].count(),pd_postop_outcomes['MiniBest @6mon'].count(),pd_postop_outcomes['MiniBest @1yr'].count()]))
        fig=px.line(y=sltdemo,x=timeline)
        fig.update_layout(title="SLT Demo Results",xaxis_title="TimeFrame",yaxis_title="Score",width=w,height=400)
        col3.plotly_chart(fig)
        col3.write("*Cohort Count : Dummy values*")
        col1,col2=st.columns(2)
        img1 = Image.open('G:\Shared drives\DBS Data Visualization\img1.png')
        img2=Image.open('G:\Shared drives\DBS Data Visualization\img2.png')
        if photos:
            col1.image(img1,caption='Shared Image 1')
            col2.image(img2,caption='Shared Image 2')
    except IndexError:
        st.error("Patient's PD Outcomes data could not be located. Please comfirn in sheet 'PD_Outcomes.'")
if edit:
    st.header('Modification of existing patient data')
    #rawdata.replace('Not available',np.nan,inplace=True)
    edit_sheet=st.selectbox(
        label='Select the excel sheet to be edited',
        options=('Battery','Demographics','MDT Workflow','ET Motor','Physio Outcomes','Neuro Outcomes'))
    modification_form=st.form('Modification of exisiting patient data')
    if edit_sheet=='Battery':
        edit_param=modification_form.selectbox('Select the parameter to edit',all_batteries.columns)
    elif edit_sheet=='Demographics':
        edit_param=modification_form.selectbox('Select the parameter to edit',pd_demographics.columns)
    elif edit_sheet=='MDT Workflow':
        edit_param=modification_form.selectbox('Select the parameter to edit',mdt_workflow.columns)
    elif edit_sheet=='ET Motor':
        edit_param=modification_form.selectbox('Select the parameter to edit',et_motor.columns)
    elif edit_sheet=='Physio Outcomes':
        edit_param=modification_form.selectbox('Select the parameter to edit',all_physio_outcomes.columns)
    elif edit_sheet=='Neuro Outcomes':
        edit_param=modification_form.selectbox('Select the parameter to edit',neuropsych_outcomes.columns)
    new_param=modification_form.number_input(
        label='Enter the new value for '+edit_param,
        value=0)#rawdata.iloc[n][edit_param])
    #rawdata.at[n,edit_param]=new_param
    save_data=modification_form.form_submit_button()
    if save_data:
        #rawdata.to_csv('G:\Shared drives\DBS Data Visualization\DBS outcomes sheet_deidentified.csv',index=False)
        st.experimental_rerun()        
