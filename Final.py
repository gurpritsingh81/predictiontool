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
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense,Dropout,LSTM
from tensorflow.keras.models import Sequential

"""# Setting inicial"""

user_crypto=st.selectbox("Enter the Currency :", ('BTC', 'ETH','ADA','MANA','XRP','BAT','DOGE','ZIL','DENT','WIN','SHIB','BTTC'))
#user_crypto = st.text_input("Enter the Currency :")
user_against=st.selectbox("Which Currecy Do you want to use for reference :", ('INR', 'USD','CAD','EUR','AUD'))
#user_against = st.text_input("Which Currecy Do you want to use for reference :")
crypro_currency=user_crypto
against_currency=user_against

start_date=dt.datetime(2016,1,1)
end_date=dt.datetime.now()
st.write('You selected:', crypro_currency,'Against',against_currency)


if user_crypto:
    
    if user_against:
        y=crypro_currency + "-" + against_currency
        x=str(y)
        currency_name=crypro_currency

        type(x)

        data = yf.download(x,start_date,end_date)
        data1=data

        data.to_csv (r'New_Products.csv', index=None)

        data.head()

        """# Data Representation """

        print(data.head())
        st.dataframe(data.tail(n=10))
        
        with st.expander("See explanation"):
             st.write("""
                1) Here, you can see how the data looks, and also, whenever the app runs, you can see the date on which the data is processed.
                2) User can also see the recorded measures like Open, High, Low, Close, Adj Close(Adjusted Close), and Volume.
                """)
    
        """# Scaling the Data"""

        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(data['Close'].values.reshape(-1,1))

        print(scaled_data)
        st.write(scaled_data)
        with st.expander("See explanation"):
             st.write("""
                1) Here, the data is called so that it we=ill become easy for the Neural network to process the data, and therefore it can easily use ML algorithms.
                2) User can also see all the variables from the beginning of the time to the latest.
                3) This is just for the user's reference that the process is working and the data visualization is also taking place.  
                """)

        """For prediction we will be using 2 years in the past """

        prediction_days=60
        future_day=30

        x_train,y_train=[],[]

        for x in range(prediction_days,len(scaled_data)-future_day):
            x_train.append(scaled_data[x-prediction_days:x,0])
            y_train.append(scaled_data[x+future_day,0])

        x_train,y_train=np.array(x_train),np.array(y_train)

        x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1], 1))

        """ Create the Neural Network for Prediction"""
        with st.expander("See explanation"):
             st.write("""
                1) Please wait as the data is being processed.
                2) You can see the progress bar for the reference.  
                """)

        model = Sequential()

        model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam',loss='mean_squared_error')
        my_bar = st.progress(0)
        
        class CustomCallback(keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs=None):
                my_bar.progress(epoch*4) 
               
         # keys = list(logs.keys())print("End epoch {} of training; got log keys: {}".format(epoch, keys))
        
        model.fit(x_train,y_train,epochs=25, batch_size=32,callbacks=[CustomCallback()])
        st.success('Model Develpmet Sucessfull !')
        """#  Testing the Model"""
        with st.expander("See explanation"):
             st.write("""
                1) Please wait as the Model is being processed 
                """)
        
        st.snow()
        import pandas as pd

        start = dt.datetime(2020,1,1)
        end =dt.datetime(2022,4,21)

        # stock = input("Enter stock symbol or ticket symbol (Exp. General Electric is 'GE'): ")

        test_data = yf.download(y,start,end)

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

        """# Plot"""

        fig, ax = plt.subplots()
          # ax.plot(line_1, color = 'green', label = 'Line 1')
         # ax.plot(line_2, color = 'red', label = 'Line 2')
         # ax.set_title('Two Trig Functions') ax.legend(['sin','cos']) ax.xaxis.set_label_text('Angle ΘΘ') ax.yaxis.set_label_text('Sine and Cosine')
            
          # plt.subplots()
        ax.plot(actual_price,color='red',label='Actuatl Prices')
        ax.plot(prediction_prices,color='green',label='Prediction Prices')
        ax.set_title(f'{crypro_currency} Price Prediction')
        ax.xaxis.set_label_text('Date')
        ax.yaxis.set_label_text('Price')
        ax.legend(loc='upper left')
        
        st.pyplot(fig)
        
        linedata = pd.DataFrame([actual_price,prediction_prices]).T.rename(columns={0:'actual_price', 1:'prediction_prices'})
        st.line_chart(linedata)
       
        
        with st.expander("See explanation"):
             st.write("""
                1) This Image depicts how the actual prices and predictions work.
                2) As the Green Line represents the future predictions, there is a gap between both the lines.
                3) The initial objective is to forecast the prices one week prior.
                4) Since the Cryptocurrency is a very volatile market therefore, we can expect drastic changes in the actual prices, and at those points of times the tool becomes ineffective
                """)

        """# Predict Next Day"""

        real_data=[modle_inputs[len(modle_inputs)- prediction_days:len(modle_inputs)]]
        real_data=np.array(real_data)
        real_data=np.reshape(real_data,(real_data.shape[0],real_data.shape[1],1))

        prediction=model.predict(real_data)
        prediction=scaler.inverse_transform(prediction)
        print(prediction)
        st.write(prediction)

        """# When To buy and when to sell"""
        

        import pandas
        import math
        import pandas_datareader as web
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import MinMaxScaler
        from keras.models import Sequential
        from keras.layers import Dense, LSTM
        import matplotlib.pyplot as plt
        plt.style.use('fivethirtyeight')

    

        # Importing dask dataframe
        import os
        import datetime
        import dask
        import dask.dataframe as dd

        ## Get the stock quote
        start_time = datetime.datetime.now()
        df = yf.download(y,start,end)
        #time_elapsed = datetime.datetime.now() - start_time
        #print('Time elapsed (hh:mm:ss:ms) {}'.format(time_elapsed))
        df.head()

        df_10 = pd.DataFrame()
        df_10['Close'] = df['Close'].rolling(window=10).mean()
        df_20 = pd.DataFrame()
        df_20['Close'] = df['Close'].rolling(window=20).mean()
        df_30 = pd.DataFrame()
        df_30['Close'] = df['Close'].rolling(window=30).mean()
        df_40 = pd.DataFrame()
        df_40['Close'] = df['Close'].rolling(window=40).mean()

        data = pd.DataFrame()
        data[str(x)] = df['Close']
        data['df_10'] = df_10['Close']
        data['df_20'] = df_20['Close']
        data['df_30'] = df_30['Close']
        data['df_40'] = df_40['Close']
        data
        st.write(data)

        def buy_sell(data):
          signalPriceBuy = []
          signalPriceSell = []
          flag = -1

          for i in range(len(data)):
            if data['df_20'][i] > data['df_10'][i]:
              if flag != 1:
                signalPriceBuy.append(data[str(x)][i])
                signalPriceSell.append(np.nan)
                flag = 1
              else:
                signalPriceBuy.append(np.nan)
                signalPriceSell.append(np.nan)
            elif data['df_20'][i] < data['df_10'][i]:
              if flag != 0:
                signalPriceBuy.append(np.nan)
                signalPriceSell.append(data[str(x)][i])
                flag=0
              else:
                signalPriceBuy.append(np.nan)
                signalPriceSell.append(np.nan)
            else:
                signalPriceBuy.append(np.nan)
                signalPriceSell.append(np.nan)

          return (signalPriceBuy, signalPriceSell)

        # Store the buy and sell data into a variable
        buy_sell = buy_sell(data)
        data['Buy_signal_Price'] = buy_sell[0]
        data['Sell_signal_Price'] = buy_sell[1]

        #Show the data
        data
        st.write(data)

        from datetime import datetime
        now = datetime.now()
        now1 = now.strftime("%d/%m/%Y")

        past=dt.datetime(2016,1,1)
        past1=past.strftime("%d/%m/%Y")
        str3=past1+'-'+now1

        
        """# Visualize the data and the strategy to buy and sell the Currency"""
        fig2, ax = plt.subplots()
        #ax.figure(figsize=(12.6,4.6))
        ax.plot(data[str(x)][0:500], label=str(currency_name), alpha=0.35)
        ax.plot(data['df_10'][0:500], label='LSTM', alpha=.35)
        ax.plot(data['df_20'][0:500], label='FbProphet',alpha=0.35)
        ax.plot(data['df_30'][0:500], label='Deep AR',alpha=0.35)
        ax.scatter(data.index, data['Buy_signal_Price'], label='Buy',marker='^',color='green')
        ax.scatter(data.index, data['Sell_signal_Price'], label='Sell',marker='v',color='red')
        ax.set_title(currency_name.upper()+' Closeing price History Buy and Sell Signals')
        ax.xaxis.set_label_text(str3)
        ax.yaxis.set_label_text('Closeing Price in '+against_currency.upper())
        ax.legend(loc='upper left')
        st.pyplot(fig2)
        st.balloons()
