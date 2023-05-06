from WalletEngine import WalletEngine
from ParaswapConnector import ParaswapConnector
from pprint import pprint
#PolyFunc.GetMaticBalance()


walletE = WalletEngine()
usdc = walletE.GetUsdcBalance()
usdt = walletE.GetUsdtBalance()
dai = walletE.GetDaiBalance()
matic = walletE.GetMaticBalance()

paraSwap = ParaswapConnector.GetInstance()
paraSwap.GetTokenList()
value = paraSwap.GetPriceSwap(walletE.GetUsdt(), 1000, walletE.GetDai())
pprint(value)
print("toto")
