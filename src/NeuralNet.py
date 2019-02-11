import DataNeuralNet
from keras.models import Sequential
from keras.layers import Dense
import numpy
import datetime
from Asset import Asset
import numpy as np
from sklearn.model_selection import train_test_split


start_train = datetime.datetime(2019, 1, 1)
end_train   = datetime.datetime(2019, 1, 15)
interval    = datetime.timedelta(minutes =5)
asset       = Asset('ethereum', 'ETH')
metrics_list = [
"burn_rate"              ,
"transaction_volume"     ,
"exchange_funds_flow"    ,
"price"]

inputs, outputs = DataNeuralNet.train(start_train, end_train, interval, asset, metrics_list)
inputs = np.array(inputs)
print(inputs)

model = Sequential()
model.add(Dense(12, input_dim=4, activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='mean_squared_error',
              optimizer='sgd',
              metrics=['mae', 'acc'])
# Fit the model
model.fit(inputs, outputs, epochs=150, batch_size=10)
model.predict(inputs)
# evaluate the model
scores = model.evaluate(inputs, outputs)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
