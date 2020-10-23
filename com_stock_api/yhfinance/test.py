import pandas as pd

df = pd.read_csv('/Users/jeongminsol/stock_psychic_api/com_stock_api/yhfinance/data/TSLA.csv')
df.insert(0, "ticker", "TSLA")

df.to_csv('/Users/jeongminsol/stock_psychic_api/com_stock_api/yhfinance/data/TSLA_2.csv')
