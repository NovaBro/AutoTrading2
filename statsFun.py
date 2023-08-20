import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def showDist(df:pd.DataFrame):
    fig = plt.figure()
    for i in range(4):
        fig.add_subplot(2,2,(i + 1)).hist(df.loc[:, df.columns[i + 1]])

def showAllDist(listOfDF:[]):
    fig = plt.figure()
    for x in listOfDF:
        for i in range(4):
            ax = fig.add_subplot(2,2,(i + 1))
            ax.hist(x.loc[:, x.columns[i + 1]])

def stanDVec(df:pd.DataFrame, period:int, feature:str):
    dfLength = len(df.index)
    allStd = np.zeros(dfLength)
    for i in range(period, dfLength):
        variencSec = np.var(df.loc[(i - period):i, feature])
        allStd[i] = math.sqrt(variencSec)

    return allStd

def actionEvaluation(actions:np.ndarray, feature:str, df:pd.DataFrame):
    prevPrice = 10000
    dfLength = len(df.index)
    goodAct = 0
    badAct = 0
    actionMap = np.zeros(dfLength)
    for i in range(30, dfLength):
        if (actions[i] == 1 and prevPrice > df.loc[i, feature]) or \
           (actions[i] == -1 and prevPrice < df.loc[i, feature]):
            goodAct += 1

            if (prevPrice > df.loc[i, feature]):
                actionMap[i] = prevPrice - df.loc[i, feature]
            else:
                actionMap[i] = df.loc[i, feature] - prevPrice

            prevPrice = df.loc[i, feature]

        elif (actions[i] == 1 and prevPrice < df.loc[i, feature]) or \
             (actions[i] == -1 and prevPrice > df.loc[i, feature]):
            badAct += 1
            
            if (prevPrice < df.loc[i, feature]):
                actionMap[i] = prevPrice - df.loc[i, feature]
            else:
                actionMap[i] = df.loc[i, feature] - prevPrice
            
            prevPrice = df.loc[i, feature]
    
    return goodAct, badAct, actionMap

        
def statsVolitAction(begin:int, end:int, actionMap:np.ndarray, volitility:np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot()
    total = 0
    ax.axhline(np.average(actionMap))
    ax.scatter(volitility[begin:end], actionMap[begin:end])

