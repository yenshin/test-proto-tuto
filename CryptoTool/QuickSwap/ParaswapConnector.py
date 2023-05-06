from WalletEngine import WalletEngine
import requests
from enum import Enum
from decimal import Decimal
from pprint import pprint
import math

# INFO: https://app.swaggerhub.com/apis/paraswapv5/api/1.0
class ParaswapNetwork(Enum):
    MAINNET = 1
    ROBSTEN = 3
    BSC = 56
    POLYGON = 137 
    

class SwapSide(Enum):
    SELL = "SELL"
    BUY = "BUY"

class ContractMethod(Enum):
    SWAP_ON_UNISWAP = "swapOnUniswap"
    BUY_ON_UNISWAP = "buyOnUniswap"
    SWAP_ON_UNISWAP_FORK = "swapOnUniswapFork"
    BUY_ON_UNISWAP_FORK = "buyOnUniswapFork"
    SWAP_ON_UNISWAP_V2FORK = "swapOnUniswapV2Fork"
    BUY_ON_UNISWAP_V2FORK = "buyOnUniswapV2Fork"
    SIMPLE_BUY = "simpleBuy"
    SIMPLE_SWAP = "simpleSwap"
    MULTI_SWAP = "multiSwap"
    MEGA_SWAP = "megaSwap"
    PROTECTED_MULTISWAP = "protectedMultiSwap"
    PROTECTED_MEGA_SWAP = "protectedMegaSwap"
    PROTECTED_SIMPLE_SWAP = "protectedSimpleSwap"
    PROTECTED_SIMPLE_BUY = "protectedSimpleBuy"
    SWAP_ON_ZEROXv2 = "swapOnZeroXv2"
    SWAP_ON_ZEROXv4 = "swapOnZeroXv4"
    BUY = "buy"

class ParaSwapPriceRoute:
    def __init__(self, jsonData):
        wallet = WalletEngine.GetInstance()
        self.__jsonData = jsonData
        self.__priceRoute = self.__jsonData['priceRoute']
        self.__srcAmount = Decimal(self.__priceRoute['srcAmount'])
        self.__srcDecimals =  Decimal(self.__priceRoute['srcDecimals'])
        self.__dstAmount = Decimal(self.__priceRoute['destAmount'])
        self.__dstDecimals =  Decimal(self.__priceRoute['destDecimals'])
        self.__srcUsd = self.__priceRoute['srcUSD']
        self.__dstUsd = self.__priceRoute['destUSD']
        self.__srcComputedAmount = self.__srcAmount / pow(10, self.__srcDecimals)
        self.__dstComputedAmount = self.__dstAmount / pow(10, self.__dstDecimals)
        self.__transactionData = {}
        self.__transactionData["srcToken"] = self.__priceRoute['srcToken']        
        self.__transactionData["destToken"] = self.__priceRoute['destToken']
        self.__transactionData["srcAmount"] = self.__priceRoute['srcAmount'] 
        self.__transactionData["destAmount"] = self.__priceRoute['destAmount']        
        self.__transactionData["srcDecimals"] = self.__priceRoute['srcDecimals']
        self.__transactionData["destDecimals"] = self.__priceRoute['destDecimals']
        self.__transactionData["userAddress"] = wallet.GetAddress()
        self.__transactionData["partner"] = "paraswap.io"
        self.__transactionData["priceRoute"] = self.__priceRoute
        #self.__transactionData = json.dumps(self.__transactionData, indent = 2) 



    def GetNbSourceToken(self):
        return self.__srcComputedAmount

    def GetNbDestToken(self):
        return self.__dstComputedAmount

    def GetSourceUsdValue(self):
        return self.__srcUsd

    def GetDestUsdValue(self):
        return self.__dstUsd

    def GetTransactionData(self):
        return self.__transactionData

class ParaTransaction:
    def __init__(self, jsonData):
        self.__jsonData = jsonData
        self.__from = self.__jsonData['from']
        self.__to = self.__jsonData['to']
        self.__value  = self.__jsonData['value']
        self.__data  = self.__jsonData['data']
        self.__gasPrice  = self.__jsonData['gasPrice']
        self.__gas  = self.__jsonData['gas']
        self.__chainId  = self.__jsonData['chainId']

    def GetFrom(self):
        return self.__from

    def GetTo(self):
        return self.__to

    def GetValue(self):
        return self.__value

    def GetData(self):
        return self.__data

    def GetGasPrice(self):
        return self.__gasPrice

    def GetGas(self):
        return self.__gas

    def GetChainId(self):
        return self.__chainId

class ParaswapConnector:
    BASE_URL = "https://apiv5.paraswap.io/"

    DEXLIST = "Uniswap,Kyber,Bancor,Oasis,Compound,Fulcrum,0x,MakerDAO,Chai,ParaSwapPool,Aave,Aave2,MultiPath,MegaPath,Curve,Curve3,Saddle,IronV2,BDai,idle,Weth,Beth,UniswapV2,Balancer,0xRFQt,ParaSwapPool2,ParaSwapPool3,ParaSwapPool4,ParaSwapPool5,ParaSwapPool6,SushiSwap,LINKSWAP,Synthetix,DefiSwap,Swerve,CoFiX,Shell,DODOV1,DODOV2,OnChainPricing,PancakeSwap,PancakeSwapV2,ApeSwap,Wbnb,acryptos,streetswap,bakeryswap,julswap,vswap,vpegswap,beltfi,ellipsis,QuickSwap,COMETH,Wmatic,Nerve,Dfyn,UniswapV3,Smoothy,PantherSwap,OMM1,OneInchLP,CurveV2,mStable,WaultFinance,MDEX,ShibaSwap,CoinSwap,SakeSwap,JetSwap,Biswap,BProtocol"
    #DEXLIST = "Uniswap,0x,MakerDAO,ParaSwapPool,MultiPath,MegaPath,IronV2,UniswapV2,ParaSwapPool2,ParaSwapPool3,ParaSwapPool4,ParaSwapPool5,ParaSwapPool6,SushiSwap,DODOV2,QuickSwap,Dfyn,UniswapV3,OneInchLP,CurveV2,JetSwap"
    __instance = None

    

    def GetInstance():
        if (ParaswapConnector.__instance == None):
            ParaswapConnector.__instance = ParaswapConnector()
        return ParaswapConnector.__instance

    def __init__(self):
        if (ParaswapConnector.__instance != None):
            raise("ParaswapConnector already exist, call ParaswapConnector.GetInstance instead")
        self.__pricesUrl = "prices"
        self.__tokensUrl = "tokens/"
        self.__transactionsUrl = "transactions/"
        self.__networkId = ParaswapNetwork.POLYGON.value
        self._tokenGlobalData = {}
        self.UpdateTokenList()

    def GetTokenGlobalData(self):
        return self._tokenGlobalData

    def UpdateTokenList(self):
        url = ParaswapConnector.BASE_URL
        url += self.__tokensUrl
        url += str(self.__networkId)
        params = {}       
        headers = {}
        headers['accept'] = 'application/json'
        response = requests.get(url, params = params, headers=headers)
        if response.status_code == 200:
            self._tokenGlobalData = response.json()
        return response

    def GetSwapPriceRoute(self, srcTkn, amount, destTkn):
        url = ParaswapConnector.BASE_URL
        url += self.__pricesUrl
        
        value =  Decimal(amount) * pow(10, srcTkn.GetDecimal())
        value = math.floor(value)

        params = {}
        params['srcToken'] = srcTkn.GetAddr()
        params['srcDecimals'] = srcTkn.GetDecimal()
        params['amount'] = str(value)
        params['destToken'] = destTkn.GetAddr()
        params['destDecimals'] = destTkn.GetDecimal()
        params['side'] = SwapSide.SELL.value
        params['network'] = self.__networkId    
        headers = {}
        headers['accept'] = 'application/json'
        response = requests.get(url, params = params, headers=headers)
        toReturn = ParaSwapPriceRoute(response.json())
        return toReturn

    def GenerateTransaction(self, priceRoute):
        url = ParaswapConnector.BASE_URL
        url += self.__transactionsUrl
        url += str(self.__networkId)
        params = {}
        headers = {}
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        print(url)
        dataValue = priceRoute.GetTransactionData()
        response = requests.post(url, params = params, json=dataValue, headers=headers)  
        toReturn = ParaTransaction(response.json())
        return toReturn