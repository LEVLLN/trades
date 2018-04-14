tickers = []
file = open('tickers.txt','r')
for line in file:
    tickers.append(line.replace('\n',''))
print(tickers)