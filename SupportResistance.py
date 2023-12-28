import yfinance as yf
import numpy as np


def support_resistance(symbol, start_date, end_date, interval):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    lows = np.array(data['Low'].values)
    highs = np.array(data['High'].values)
    prices = np.concatenate((lows, highs))

    prices.sort()

    i = 0
    j = 0

    srTotalArray = []
    while i < len(prices) - 1:
        j = i + 1
        bottom = prices[i]

        srArray = [bottom]
        top = prices[j]

        while top <= bottom * 1.02 and j < len(prices):
            top = prices[j]
            if top <= bottom * 1.02:
                srArray.append(top)
                j += 1
            else:
                break

        if len(srArray) >= 3:
            srArray = [min(srArray), max(srArray)]
            srTotalArray.append(srArray)
            i = j + 1

        else:
            i += 1

    print(srTotalArray)

    return srTotalArray
