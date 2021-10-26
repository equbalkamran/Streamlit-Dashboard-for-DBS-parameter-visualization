import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO
import numpy as np

z= pd.read_excel('Dummy dataset file example.xlsx')
z=z.transpose()
st.write("Patient Information")
st.write(z.index[0]+":"+z.index[1])
for i in range(0,9):
    if i==0 or i==1 or i==3:
        st.write(z[i][0]+": ",z[i][1].strftime('%Y-%m-%d'))
    else:
        st.write(z[i][0]+": ",z[i][1])
url1=z[9][1]
url2=z[10][1]
response1 = requests.get(url1)
img1 = Image.open(BytesIO(response1.content))
response2 = requests.get(url2)
img2 = Image.open(BytesIO(response2.content))
st.image([img1,img2],caption=["Pre-operative MRI"," Post Operative CT "],width=1000)
st.write(z[11][0],": "+str(z[11][1]))
z2= pd.read_excel('Dummy dataset file example.xlsx',sheet_name='Per session details')
fig0 = px.line(z2,x='Date', y='Weight')
st.write('Plot of weight of the patient')
st.plotly_chart(fig0)

z2_1=pd.melt(z2, id_vars=['Date'], value_vars=z2.columns[2:6])
fig1 = px.line(z2_1,x='Date', y='value', color='variable')
st.write('Plot of tuned parameters of the patient over time')
st.plotly_chart(fig1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=z2.Date, y=z2.Amplitude,name="Amplitude"))
fig.add_trace(go.Scatter(x=z2.Date, y=z2['Pulse Duration'],name="Pulse Duration",yaxis="y2"))
fig.add_trace(go.Scatter(x=z2.Date, y=z2['Pulse Frequency'],name="Pulse Frequency",yaxis="y3"))
fig.add_trace(go.Scatter(x=z2.Date, y=z2['Electrode Configuration'],name="Electrode Configuration",yaxis="y4"))
fig.update_layout(
    xaxis=dict(domain=[0.3, 0.7]),
    yaxis=dict(title="Amplitude",titlefont=dict(color="#1f77b4"),tickfont=dict(color="#1f77b4")),
    yaxis2=dict(title="Pulse Duration",titlefont=dict(color="#ff7f0e"),tickfont=dict(color="#ff7f0e"),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.15
    ),
    yaxis3=dict(title="Pulse Frequency",titlefont=dict(color="#d62728" ),tickfont=dict(color="#d62728"),
        anchor="x",
        overlaying="y",
        side="right"
    ),
    yaxis4=dict(title="Electrode Confiugration",titlefont=dict(color="#9467bd"),tickfont=dict(color="#9467bd"),
        anchor="free",
        overlaying="y",
        side="right",
        position=0.85
    )
)
fig.update_layout(title_text="Multi y axis plot of tuned parameters",width=800,)
st.plotly_chart(fig)
    


z2_2=pd.melt(z2, id_vars=['Date'], value_vars=z2.columns[7:14])
fig2 = px.line(z2_2,x='Date', y='value', color='variable')
st.write('Plot of symptom scores of the patient over time')
st.plotly_chart(fig2)

z2['Electrode Configuration'] = z2['Electrode Configuration'].apply(np.ceil) 
fig3d = px.scatter_3d(z2,x='Amplitude', y='Pulse Frequency', z='Pulse Duration',color='Electrode Configuration')
st.plotly_chart(fig3d)

option = st.selectbox('How would you rate this demo?',('1','2','3','4','5'))
st.write('You selected:', option)
st.button("Re-run")