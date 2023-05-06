import requests
from enum import Enum

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
        self.__pricesUrl = "prices/"
        self.__tokensUrl = "tokens/"
        self.__networkId = ParaswapNetwork.POLYGON.value

    def GetTokenList(self):
        url = ParaswapConnector.BASE_URL
        url += self.__tokensUrl
        url += str(self.__networkId)
        params = {}       
        headers = {}
        headers['accept'] = 'application/json'
        response = requests.get(url, params = params, headers=headers)
        return response

    def GetPriceSwap(self, srcTkn, amount, destTkn):
        url = ParaswapConnector.BASE_URL
        url += self.__pricesUrl
        params = {}
        params['srcToken'] = srcTkn.GetAddr()
        #params['srcToken'] = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
        params['srcDecimals'] = srcTkn.GetDecimal()
        params['amount'] = str(amount)
        params['destToken'] = destTkn.GetAddr()
        #params['destToken'] = '0xdac17f958d2ee523a2206206994597c13d831ec7é'
        params['destDecimals'] = destTkn.GetDecimal()
        params['side'] = SwapSide.SELL.value
        params['network'] = self.__networkId
        params['includeDEXS'] = ParaswapConnector.DEXLIST
        params['includeContractMethods']= ContractMethod.PROTECTED_MEGA_SWAP.value
        # params['srcToken'] = srcTkn.GetSymbol()
        # params['amount'] = str(amount)
        # params['destToken'] = destTkn.GetSymbol()
        # params['side'] = SwapSide.SELL.value
        # params['network'] = self.__networkId

        headers = {}
        headers['accept'] = 'application/json'
        response = requests.get(url, params = params, headers=headers)
        return response