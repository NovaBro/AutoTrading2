import torch, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def candleSticks(panData:pd.DataFrame, ax:plt.Axes):
    wick = 0.25
    wax = 0.5
    upPrice = panData[panData["Open"] <= panData["Close"]]
    downPrice = panData[panData["Open"] > panData["Close"]]
    
    ax.bar(upPrice.index, height=(upPrice.loc[:, "Open"] - upPrice.loc[:, "Close"]), bottom=upPrice.loc[:, "Close"], width=wax, color = "Green")
    ax.bar(upPrice.index, height=(upPrice.loc[:, "High"] - upPrice.loc[:, "Low"]), bottom=upPrice.loc[:, "Low"], width=wick, color = "Green")

    ax.bar(downPrice.index, height=(downPrice.loc[:, "Open"] - downPrice.loc[:, "Close"]), bottom=downPrice.loc[:, "Close"], width= wax, color = "Red")
    ax.bar(downPrice.index, height=(downPrice.loc[:, "High"] - downPrice.loc[:, "Low"]), bottom=downPrice.loc[:, "Low"], width= wick, color = "Red")

def normalize(data):
    return (data - data.min())/(data.max() - data.min())

def movingAvg(length, data:np.ndarray, feature:str = None, displace = None):
    if feature == None and displace == None:
        movingAvgArr = np.zeros(data.size)
        for day in range(data.size - length):
            tempTotal = 0
            for l in range(length):
                tempTotal += data[data.size - (l + day) - 1]
            tempAvg = tempTotal / length
            movingAvgArr[data.size - day - 1] = tempAvg
        return movingAvgArr
    
def movAvgDF(length, dataFrame:pd.DataFrame, feature:str, displace = None):
    if displace == None:
        movingAvgArr = np.zeros(len(dataFrame.index))
        for day in range(len(dataFrame.index) - length):
            tempTotal = 0
            for l in range(length):
                tempTotal += dataFrame.loc[(len(dataFrame.index) - (l + day) - 1), feature]
            tempAvg = tempTotal / length
            movingAvgArr[len(dataFrame.index) - day - 1] = tempAvg
        return movingAvgArr

dataPath = "/Users/williamzheng/Documents/pthyon files workspace/STOCKNN/Trading Attempts/TradeAttempt2/AutoTrading2/"

amznDF = pd.read_csv(dataPath + "AMZN.csv")
applDF = pd.read_csv(dataPath + "AAPL.csv")

print(applDF)

fig0 = plt.figure()
ax0_0 = fig0.add_subplot()

candleSticks(applDF, ax0_0)
for i in range(1, 3):
    ax0_0.plot(movAvgDF(i * 7, applDF, "Close"))
day7 = movAvgDF(7, applDF, "Close")
day14 = movAvgDF(14, applDF, "Close")




plt.show()


