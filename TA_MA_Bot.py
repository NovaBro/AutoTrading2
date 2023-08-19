import torch, os
import numpy as np
import pandas as pd
import main, math
import statsFun as stf
import matplotlib.pyplot as plt

dataPath = "/Users/williamzheng/Documents/pthyon files workspace/STOCKNN/Trading Attempts/TradeAttempt2/AutoTrading2/"

amznDF = pd.read_csv(dataPath + "AMZN.csv")
applDF = pd.read_csv(dataPath + "AAPL.csv")

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

def findCross(shortMA:pd.DataFrame, longMA:pd.DataFrame, longestPeriodLen, feature:str):
    #Finds when the moving averages cross
    actionTable = np.zeros((len(longMA.index)))
    temp = 0
    temp2 = 0
    for day in range((longestPeriodLen + 1), len(longMA.index)):
        
        if shortMA.loc[day -1, feature] > longMA.loc[day -1, feature] and shortMA.loc[day, feature] < longMA.loc[day, feature]:
            actionTable[day] = -1
            temp += 1
        elif shortMA.loc[day -1, feature] < longMA.loc[day -1, feature] and shortMA.loc[day, feature] > longMA.loc[day, feature]:
            actionTable[day] = 1
            temp2 += 1
        else:
            actionTable[day] = 0
    return actionTable

class testorBot():
    def __init__(self, shortMA:int, longMA:int, feature:str, stockDF:pd.DataFrame) -> None:
        self.dataFeature = feature
        self.selectedDF = stockDF
        self.dfLength = len(stockDF.index)
        self.MAshort = movAvgDF(shortMA, stockDF, feature)
        self.MAlong = movAvgDF(longMA, stockDF, feature)
        self.maShortDF = pd.DataFrame(data=self.MAshort, columns=[feature])
        self.maLongDF = pd.DataFrame(data=self.MAlong, columns=[feature])
        self.actionSequence = findCross(self.maShortDF, self.maLongDF, longMA, feature)

        self.balanceHist = np.zeros(self.dfLength)
        self.BH_Hist = np.zeros(self.dfLength)
    
    def runTest(self, startDay, endDay, startingAmount):
        bot1 = main.account(startingAmount)
        endPrice = self.selectedDF.loc[endDay, self.dataFeature]
        startPrice = self.selectedDF.loc[startDay, self.dataFeature]

        #Calculate Buy and Hold
        BH_Stocks = int((startingAmount / startPrice))
        leftOverBal = startingAmount - BH_Stocks * startPrice
        BH_balance = BH_Stocks * endPrice + leftOverBal

        #Run Simulation
        resulAct = stf.actionEvaluation(self.actionSequence, self.dataFeature, self.selectedDF)
        print(f"Result Action: \n  Good: {resulAct[0]}\n  Bad: {resulAct[1]}")
        #volit = stf.stanDVec(self.selectedDF, 10, self.dataFeature)
        #stf.statsVolitAction(50, 750, resulAct[2], self.selectedDF.loc[:, "Volume"])

        for day in range(startDay, endDay):
            self.BH_Hist[day] = leftOverBal + BH_Stocks * self.selectedDF.loc[day, self.dataFeature]
            self.balanceHist[day] = bot1.balance + self.selectedDF.loc[day, self.dataFeature] * bot1.numShares
            #scaling BalanceHist
            buyShareAmount = int(bot1.balance / self.selectedDF.loc[day, self.dataFeature])
            if self.actionSequence[day] == 1:
                bot1.buy(buyShareAmount, self.selectedDF.loc[day, self.dataFeature])
                """ print(botResult, 
                      f"  {bot1.numBuys}  {bot1.numSells}   \
                      {self.actionSequence[day]}   {day}   \
                      {self.selectedDF.loc[day, self.dataFeature]}") """
            elif self.actionSequence[day] == -1:
                bot1.sell(bot1.numShares, self.selectedDF.loc[day, self.dataFeature])
                """ print(botResult, 
                      f"  {bot1.numBuys}  {bot1.numSells}   \
                      {self.actionSequence[day]}   {day}   \
                      {self.selectedDF.loc[day, self.dataFeature]}") """
        
        #scale balance history for comparision 
        #NOTE: Normalize?
        if(False):
            if endPrice > startPrice:
                self.balanceHist = 10 * (self.balanceHist - startPrice) / (endPrice - startPrice)
            else:
                self.balanceHist = 10 * (self.balanceHist - endPrice) / (startPrice - endPrice) - 150
        print(f"Bot Wealth: {bot1.balance + endPrice * bot1.numShares}\nBH: {BH_balance}")


def plotData(axis:plt.Axes, testBot:testorBot):
    
    axis.plot(testBot.selectedDF.loc[:, testBot.dataFeature])
    axis.plot(testBot.MAshort)
    axis.plot(testBot.MAlong)
    axis.legend(["Stock Price", "MAshort", "MAlong", "Balance History"])

    #candleSticks(testBot.selectedDF, axis)
    if(False):
        for i in range(len(testBot.actionSequence)):
            if testBot.actionSequence[i] == 1:
                axis.axvline(i, color = "green")
            elif testBot.actionSequence[i] == -1:
                axis.axvline(i, color = "red")


appleTest = testorBot(8, 9, "Close", applDF) #8, 9
appleTest.runTest(50, 750, 1000)
amznTest = testorBot(11, 12, "Close", amznDF) #11, 12
amznTest.runTest(14, 750, 1000)

""" fig0 = plt.figure()
ax0_0 = fig0.add_subplot()
plotData(ax0_0, appleTest)
ax0_0.plot(stf.stanDVec(applDF, 7, "Close"))

fig1 = plt.figure()
ax1_0 = fig1.add_subplot()
plotData(ax1_0, amznTest) """
allFig = plt.figure()
ax1 = allFig.add_subplot(221)
ax2 = allFig.add_subplot(222)
ax3 = allFig.add_subplot(223)
ax4 = allFig.add_subplot(224)
plotData(ax1, appleTest)
plotData(ax2, amznTest)
ax3.plot(stf.stanDVec(applDF, 50, "Close"))
ax3.plot(stf.stanDVec(amznDF, 50, "Close"))
ax4.plot(appleTest.BH_Hist)
ax4.plot(appleTest.balanceHist)
ax4.plot(amznTest.BH_Hist)
ax4.plot(amznTest.balanceHist)


plt.show()

