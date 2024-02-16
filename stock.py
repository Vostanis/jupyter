import sys
from dashboard import dashboard

ticker = sys.argv[1]
date = sys.argv[2]
dashboard(ticker, date)