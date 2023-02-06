import time
import json
import csv
from decimal import Decimal
from web3 import Web3

def start():
    w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
    tickLower=Decimal("-887270")
    tickUpper=Decimal("887270")

    calcAbi=json.load(open('abis/S4Calc.json','r'))
    calcAddress="0xF9f0cD938abceDF6d1BCED6ABeccDE843c80e648"
    calc=w3.eth.contract(address=calcAddress, abi=calcAbi)

    # Get liquidity
    xsgdUsdcV3Pool="0x6279653c28f138C8B31b8A0F6F8cD2C58E8c1705"
    usdcUsdtV3Pool="0x3416cF6C708Da44DB2624D63ea0AAef7113527C6"
    # res=calc.functions.getV3TokenAmountsByLiquidity(usdcUsdtV3Pool, int(tickLower), int(tickUpper), 2484764).call()
    res = calc.functions.getV3TokenAmountsByLiquidity(xsgdUsdcV3Pool, int(tickLower), int(tickUpper), 1*10**6).call()
    # res=calc.functions.getV3TokenAmounts(423437).call()
    if len(res)>1:
        with open('liquidityAmounts.csv','a') as f:
            r=[str(i) for i in res]
            f.write(','.join(r)+'\n')
    else:
        print('error')

if __name__=='__main__':
    start()