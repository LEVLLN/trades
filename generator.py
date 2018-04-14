tickers = []
TICKERS_FILE_NAME = 'tickers.txt'

file = open(TICKERS_FILE_NAME,'r')
for line in file:
    tickers.append(line.replace('\n',''))
print(tickers)

