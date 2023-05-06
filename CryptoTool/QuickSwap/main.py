from WalletEngine import WalletEngine
from ParaswapConnector import ParaswapConnector
from pprint import pprint
#PolyFunc.GetMaticBalance()


walletE = WalletEngine.GetInstance()
usdc = walletE.GetUsdcBalance()
usdt = walletE.GetUsdtBalance()
dai = walletE.GetDaiBalance()
matic = walletE.GetMaticBalance()
nquick = walletE.GetNQuickBalance()
print("===========================================")
print("nquick= " + str(nquick))


paraSwap = ParaswapConnector.GetInstance()
tokenData = paraSwap.GetTokenGlobalData()
#print("===========================================")
#print(tokenData)
#value = paraSwap.GetPriceSwap(walletE.GetUsdt(), 1000, walletE.GetDai())
priceRoute = paraSwap.GetSwapPriceRoute(walletE.GetNQuick(), 0.1, walletE.GetOQuick())
transaction = paraSwap.GenerateTransaction(priceRoute)
walletE.DoTransaction(transaction)
print("===========================================")
print("nquick= " + str(nquick))

