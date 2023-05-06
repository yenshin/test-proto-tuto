from W3Connector import W3Connector
from Token import *

class WalletEngine:
    
    METAMASK_ADDRESS = ""
    
    def __init__(self):
        '''
        prepare data
        '''
        self.__w3 = W3Connector.GetInstance().W3
        self.__tokenMgr = TokenManager.GetInstance()
        self.__matic = self.__tokenMgr.GetToken(TokenType.MATIC)
        self.__usdc = self.__tokenMgr.GetToken(TokenType.USDC)
        self.__usdt = self.__tokenMgr.GetToken(TokenType.USDT)
        self.__dai = self.__tokenMgr.GetToken(TokenType.DAI)
        
        self.UpdateBalance()
        
    

    def UpdateBalance(self):
        self.__matic.UpdateBlanceFromWalletAddr(WalletEngine.METAMASK_ADDRESS)
        self.__usdc.UpdateBlanceFromWalletAddr(WalletEngine.METAMASK_ADDRESS)
        self.__usdt.UpdateBlanceFromWalletAddr(WalletEngine.METAMASK_ADDRESS)
        self.__dai.UpdateBlanceFromWalletAddr(WalletEngine.METAMASK_ADDRESS)

    def GetMatic(self):
        return self.__matic

    def GetUsdc(self):
        return self.__usdc
    
    def GetUsdt(self):
        return self.__usdt

    def GetDai(self):
        return self.__dai

    def GetMaticBalance(self):
        return self.__matic.GetBalance()

    def GetUsdcBalance(self):
        return self.__usdc.GetBalance()
    
    def GetUsdtBalance(self):
        return self.__usdt.GetBalance()

    def GetDaiBalance(self):
        return self.__dai.GetBalance()