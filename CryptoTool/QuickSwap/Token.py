from enum import Enum
import json

from eth_utils import address
from W3Connector import W3Connector
from decimal import Decimal
import copy

class TokenType(Enum):
    MATIC = 0
    USDC = 1
    USDT = 2
    DAI = 3
    OQUICK = 4
    NQUICK = 5

class TokenData:

    __connector = W3Connector.GetInstance()
    __w3 = W3Connector.GetInstance().W3
    
    USDC_TOKEN_ADDR="0x2791bca1f2de4661ed88a30c99a7a9449aa84174"
    USDC_ABI = json.load(open('contract/usdc.json', 'r'))

    USDT_TOKEN_ADDR="0xc2132d05d31c914a87c6611c10748aeb04b58e8f"
    USDT_ABI = json.load(open('contract/usdt.json', 'r'))

    DAI_TOKEN_ADDR="0x8f3cf7ad23cd3cadbd9735aff958023239c6a063"
    DAI_ABI = json.load(open('contract/dai.json', 'r'))

    OQUICK_TOKEN_ADDR="0x831753dd7087cac61ab5644b308642cc1c33dc13"
    OQUICK_ABI = json.load(open('contract/oldQuick.json', 'r'))

    NQUICK_TOKEN_ADDR="0xb5c064f955d8e7f38fe0460c556a72987494ee17"
    NQUICK_ABI = json.load(open('contract/newQuick.json', 'r'))

    AUGUSTUSSWAPPER_ABI = json.load(open('contract/paraswapaugustus.json', 'r'))

    ETH_TOKEN_ADDR="0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"

    MATIC_TOKEN_ADDR="0x0000000000000000000000000000000000001010"
    
    def __init__(self, addr, abiFile):       
        if addr == "":
            self.__abi = None
            self.__addr = "0xmatic"
            self.__addrCk = "0xmatic"
            self.__contract = None
            self.__decimal = 18
            #self.__symbol = "MATIC"
            self.__fUpdateBalance = self.__UpdateMaticBalance
            
        else:
            self.__abi = abiFile
            self.__addr = addr
            self.__addrCk = TokenData.__connector.AddrCk(addr)
            self.__contract = TokenData.__w3.eth.contract(address=self.__addrCk, abi=self.__abi)
            #self.__symbol = self.__contract.functions.symbol().call()
            self.__decimal = Decimal(self.__contract.functions.decimals().call())
            self.__fUpdateBalance = self.__UpdateGenericTokenBalance
        self.__balance = 0

    def __UpdateMaticBalance(self, walletAddr):
        balance = TokenData.__w3.eth.get_balance(walletAddr)
        # INFO: 'ether' as same number of decimal as matic (and we are on matic network)
        balance = self.__w3.fromWei(balance, 'ether')
        return balance

    def __UpdateGenericTokenBalance(self, walletAddr):
        balance = Decimal(self.__contract.caller.balanceOf(walletAddr))
        balance /= pow(10, self.__decimal)
        return balance

    def UpdateBlanceFromWalletAddr(self, walletAddr):
        self.__balance = self.__fUpdateBalance(walletAddr)

    def GetBalance(self):
        return self.__balance
    
    def GetAddr(self):
        return self.__addr

    def GetDecimal(self):
        return self.__decimal

    # def GetSymbol(self):
    #     return self.__symbol

class TokenManager:

    __instance = None
    def GetInstance():
        if (TokenManager.__instance == None):
            TokenManager.__instance = TokenManager()
        return TokenManager.__instance


    def __init__(self):
        if (TokenManager.__instance != None):
            raise("TokenManager already exist, call TokenManager.GetInstance instead")
        self.__tokenList = {}
        self.__tokenList[TokenType.MATIC] = ("", '')
        self.__tokenList[TokenType.USDC] = (TokenData.USDC_TOKEN_ADDR, TokenData.USDC_ABI)
        self.__tokenList[TokenType.USDT] = (TokenData.USDT_TOKEN_ADDR, TokenData.USDT_ABI)
        self.__tokenList[TokenType.DAI] = (TokenData.DAI_TOKEN_ADDR, TokenData.DAI_ABI)
        self.__tokenList[TokenType.OQUICK] = (TokenData.OQUICK_TOKEN_ADDR, TokenData.OQUICK_ABI)
        self.__tokenList[TokenType.NQUICK] = (TokenData.NQUICK_TOKEN_ADDR, TokenData.NQUICK_ABI)

    def GetToken(self, id):
        # INFO: token factory
        addr, abi = self.__tokenList[id]
        return TokenData(addr, abi)
