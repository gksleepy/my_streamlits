import streamlit as st
import pandas as pd
import numpy as np

st.title('1Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data #พัก data ไม่ต้องโหลดใหม่ทุกครั้ง
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower() #function ไม่มีชื่อ
    data.rename(lowercase, axis='columns', inplace=True) #แก้ไขแล้วแทนที่ข้อมูลเดิม
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#ใน if ให้เปลี่ยนตามที่ checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
    #st.table(data)
    #st.dataframe(data)

#histrogram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] #index[1]-จำนวนชม,0 จำนวนความถี่ในแต่ละชมว่าใช้รถเท่าไหร่ 
st.bar_chart(hist_values)
#hist_values #tuple array

'''
import plotly.express as px
fig = px.histrogram(
    x=np.histrogram(data[DATE_COLUMN].dt.hour,
                    bins = 24, range=(0.24))[1][0:24],
    y = hist_values, nbins=24)
st.ployly_chart(fig)
'''

#map
st.subheader('Map of all pickups')
st.map(data)

#อยากรู้ 5pm
#hour_to_filter = 17 
#slider - slicer date ให้เลือก
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)



