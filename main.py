import torch, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver

def normalize(data):
    return (data - data.min())/(data.max() - data.min())

dataPath = "/Users/williamzheng/Documents/pthyon files workspace/STOCKNN/Trading Attempts/TradeAttempt2/AutoTrading2/"

amznDF = pd.read_csv(dataPath + "AMZN.csv")
applDF = pd.read_csv(dataPath + "AAPL.csv")

print(amznDF.loc[:, ["Open", "High", "Low", "Close", "Volume"]])
#"Open", "High", "Low", "Close", "Volume"

applData = normalize(applDF["High"].to_numpy())
amznData = normalize(amznDF["High"].to_numpy())

class account():
    def __init__(self, Balance) -> None:
        self.balance = Balance
        self.numShares = 0
        self.numBuys = 0
        self.numSells = 0
    #True if transaction valid, False if transaction invalid
    def buy(self, sharesBought, sharePrice):
        if (sharesBought * sharePrice) > self.balance: return False
        self.balance -= (sharesBought * sharePrice)
        self.numShares += sharesBought
        return True
        
    def sell(self, sharesSold, sharePrice):
        if (sharesSold) > self.numShares: return False
        self.balance += (sharesSold * sharePrice)
        self.numShares -= sharesSold
        return True

class State():
    def __init__(self, balance, dataFile:str) -> None:
        self.prof = account(balance)
        self.readData = pd.read_csv(dataPath + dataFile)
        self.features = ["Open", "High", "Low", "Close", "Volume"]
        self.readData = self.readData.loc[:, self.features]
        for f in self.features:
            self.readData.loc[:, f] = normalize(self.readData.loc[:,f])

        
test = State(1000, "AMZN.csv")
print("test:\n",test.readData)

fig = plt.figure()
ax = fig.add_subplot()

ax.plot(applData)
ax.plot(amznData)

#plt.show()