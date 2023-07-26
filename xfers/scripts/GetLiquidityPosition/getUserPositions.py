import os
import arrow
import requests
import pandas as pd
import time
import json
import csv
from decimal import Decimal
from web3 import Web3


csv_name='liquidityAmounts.csv'
GQL_URL='https://api.studio.thegraph.com/query/39657/dzy-str-13/v0.0.10'
xsgdUsdcV3Pool="0x6279653c28f138C8B31b8A0F6F8cD2C58E8c1705"
usdcUsdtV3Pool="0x3416cF6C708Da44DB2624D63ea0AAef7113527C6"

def get_user_pos(res, csv_name):
    #Open yesterdays file
    yesterday=arrow.utcnow().shift(days=-2).format('YYYYMMDD')
    print(f"{arrow.get(yesterday)}")
    userLiquidityMap={}
    if (os.path.exists(f'userData/{yesterday}.csv')):
        with open(f'userData/{yesterday}.csv') as f:
            reader=csv.DictReader(f)
            for row in reader:                
                userLiquidityMap[row['address']]={
                    'timestamp':int(arrow.utcnow().shift(days=-1).timestamp()),
                    'nftId':int(row['nftId']),
                    'liquidity':int(row['liquidity']),
                    'blockNumber':int(row['blockNumber'])
                }
    df=pd.read_csv(csv_name)
    lastQueryTime=df.iloc[-1,1]
    depositBody='''
    {
        v3Deposits(where:{poolAddress:"0x6279653c28f138C8B31b8A0F6F8cD2C58E8c1705",blockTimestamp_gt:$lastQueryTime},orderBy:blockNumber,orderDirection:asc,) {
            transactionHash
            poolAddress
            depositor
            nftId
            liquidity
            blockTimestamp
            blockNumber
        }
    }
    '''.replace('$lastQueryTime',str(lastQueryTime))
    withdrawBody=depositBody.replace("v3Deposits","v3Withdraws")
    # variables={"lastQueryTime":lastQueryTime}
    depositRes=requests.post(GQL_URL, json={"query":depositBody})
    withdrawRes=requests.post(GQL_URL, json={"query":withdrawBody})    
    if not all([depositRes.ok, withdrawRes.ok]):
        print('error')
    depositRes=depositRes.json()['data']['v3Deposits']
    withdrawRes=withdrawRes.json()['data']['v3Withdraws']
    for res in [depositRes, withdrawRes]:
        for r in res:
            if not userLiquidityMap.get(r['depositor']) or int(r['blockTimestamp']) > userLiquidityMap[r['depositor']]['timestamp']:
                # We only take the latest liquidity
                userLiquidityMap[r['depositor']]={
                    'timestamp':int(r['blockTimestamp']),
                    'nftId':r['nftId'],
                    'liquidity':int(r['liquidity']),
                    'blockNumber':int(r['blockNumber'])
                }

    #Convert to column
    df_struct=[[k, v['nftId'], v['liquidity'], v['blockNumber']] for k,v in userLiquidityMap.items()]
    liquidity_df=pd.DataFrame(df_struct,columns=['address','nftId','liquidity','blockNumber'])
    liquidity_df['xsgd']=(int(df.iloc[-1,3])/10**6*liquidity_df['liquidity']).astype(int)
    liquidity_df=liquidity_df[['address','nftId','liquidity','xsgd','blockNumber']]
    filename=arrow.utcnow().shift(days=-1).format('YYYYMMDD')
    liquidity_df.to_csv(f'userData/{filename}.csv', index=False)




def start():    
    w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
    tickLower=Decimal("-887270")
    tickUpper=Decimal("887270")

    calcAbi=json.load(open('abis/S4Calc.json','r'))
    calcAddress="0xF9f0cD938abceDF6d1BCED6ABeccDE843c80e648"
    calc=w3.eth.contract(address=calcAddress, abi=calcAbi)

    # Get liquidity
    res = calc.functions.getV3TokenAmountsByLiquidity(xsgdUsdcV3Pool, int(tickLower), int(tickUpper), 1*10**6).call()    
    #Get user positions
    get_user_pos(res, csv_name)
    

if __name__=='__main__':
    start()
    # get_user_pos(1, csv_name)