import arrow
import csv
import json
import pandas as pd

def run():
    liquidity_df = pd.read_csv('liquidityAmounts.csv')
    for index, row in liquidity_df.iterrows():
        date = arrow.get(int(row.blockTimestamp)).format('YYYYMMDD')
        blockNumber = row.blockNumber
        user_csv_name = f"userData/{date}.csv"
        user_df=pd.read_csv(user_csv_name)
        user_df['blockNumber']=blockNumber
        user_df.to_csv(user_csv_name, index=False)



    

if __name__=='__main__':
    run()