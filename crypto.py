# -*- coding: utf-8 -*-
"""Crypto.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eGWuUMSOtdqzGzSrf-snP7yAzTj0HRCv

# Libraries Used
"""



# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import pandas_datareader as web
import yfinance as yf
import streamlit as st
# %matplotlib inline
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense,Dropout,LSTM
from tensorflow.keras.models import Sequential

"""# Setting inicial"""
user_crypto = st.text_input("Enter the Currency :")
user_against = st.text_input("Which Currecy Do you want to use for reference :")
crypro_currency=user_crypto
against_currency=user_against

start=dt.datetime(2016,1,1)
end=dt.datetime.now()

y=crypro_currency + "-" + against_currency
x=str(y)

type(x)

data = yf.download(x,start,end)

data.head()

"""# How The Data Looks"""

st.print(data.head())

"""# sclaring the data from 0 to 1 """

scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(data['Close'].values.reshape(-1,1))

st.print(scaled_data)

"""# For prediction we will be using 60 days in the past """

prediction_days=60
st.print(prediction_days)
x_train,y_train=[],[]

for x in range(prediction_days,len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x,0])
    y_train.append(scaled_data[x,0])

x_train,y_train=np.array(x_train),np.array(y_train)

x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1], 1))



model = Sequential()

model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))
model.compile(optimizer='adam',loss='mean_squared_error')

model.fit(x_train,y_train,epochs=25, batch_size=32)

"""#  Testing the Model"""

import pandas as pd

start = pd.to_datetime(['2020-01-01']).astype(int)[0]//10**9 # convert to unix timestamp.
end = pd.to_datetime(['2022-04-18']).astype(int)[0]//10**9 # convert to unix timestamp.

# stock = input("Enter stock symbol or ticket symbol (Exp. General Electric is 'GE'): ")

url = 'https://query1.finance.yahoo.com/v7/finance/download/' + str(y) + '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
test_data = pd.read_csv(url)

actual_price=test_data['Close'].values

total_dataset=pd.concat((data['Close'],test_data['Close']),axis=0)

modle_inputs= total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values

modle_inputs=modle_inputs.reshape(-1,1)
modle_inputs=scaler.fit_transform(modle_inputs)

x_test=[]

for x in range(prediction_days,len(modle_inputs)):
    x_test.append(modle_inputs[x-prediction_days:x,0])

x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

prediction_prices=model.predict(x_test)
prediction_prices=scaler.inverse_transform(prediction_prices)

"""#  Root Mean Squared error(RMSE) and Mean Absolute Percentage Error(MAPE) 

"""

actual=actual_price
predicted=prediction_prices

from sklearn.metrics import mean_squared_error
import math

mse = sklearn.metrics.mean_squared_error(actual, predicted)

rmse = math.sqrt(mse)
print(rmse)

def mape(actual,pred):
    return np.mean(np.abs((actual - pred) / actual)) * 100

result = mape(actual,predicted)
print("The mean absolute percentage error: ",result)

"""# Plot"""

plt.plot(actual_price,color='black',label='Actuatl Prices')
plt.plot(prediction_prices,color='green',label='Prediction Prices')
plt.title(f'{crypro_currency} Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
st.pyplot()

"""# Predict Next Day"""

real_data=[modle_inputs[len(modle_inputs)+1- prediction_days:len(modle_inputs)+1,0]]
real_data=np.array(real_data)
real_data=np.reshape(real_data,(real_data.shape[0],real_data.shape[1],1))

prediction=model.predict(real_data)
prediction=scaler.inverse_transform(prediction)
st.print(prediction)
