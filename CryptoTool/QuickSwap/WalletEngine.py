from pprint import pprint
from W3Connector import W3Connector
from Token import *
from os import path

class WalletEngine:

    __instance = None

    

    def GetInstance():
        if (WalletEngine.__instance == None):
            WalletEngine.__instance = WalletEngine()
        return WalletEngine.__instance

    def __init__(self):
        '''
        prepare data
        '''
        if (WalletEngine.__instance != None):
            raise("WalletEngine already exist, call WalletEngine.GetInstance instead")
        if (path.exist("../key.txt" == False):
            raise("../key.txt doesn't exist, it muse contains, wallet addr and wallet priv Key")
        keyFile = open("../key.txt", 'r')
        lines = keyFile.readlines()
        walletAddr = lines[0].strip()
        walletPrivKey = lines[1].strip()


        self.__w3 = W3Connector.GetInstance().W3
        self.__tokenMgr = TokenManager.GetInstance()
        self.__matic = self.__tokenMgr.GetToken(TokenType.MATIC)
        self.__usdc = self.__tokenMgr.GetToken(TokenType.USDC)
        self.__usdt = self.__tokenMgr.GetToken(TokenType.USDT)
        self.__dai = self.__tokenMgr.GetToken(TokenType.DAI)
        self.__oQuick = self.__tokenMgr.GetToken(TokenType.OQUICK)
        self.__nQuick = self.__tokenMgr.GetToken(TokenType.NQUICK)
        
        self.__ethAccount = self.__w3.eth.account.privateKeyToAccount(walletPrivKey)
        if (self.__ethAccount._address != walletAddr):
            print("error private key doesn't correspond to wallet " + walletAddr)
            raise ""
        #pprint(self.__ethAccount._private_key)
        self.UpdateBalance()
        
    
    def GetAddress(self):
        return self.__ethAccount._address

    def UpdateBalance(self):
        self.__matic.UpdateBlanceFromWalletAddr(self.__ethAccount._address)
        self.__usdc.UpdateBlanceFromWalletAddr(self.__ethAccount._address)
        self.__usdt.UpdateBlanceFromWalletAddr(self.__ethAccount._address)
        self.__dai.UpdateBlanceFromWalletAddr(self.__ethAccount._address)
        self.__oQuick.UpdateBlanceFromWalletAddr(self.__ethAccount._address)
        self.__nQuick.UpdateBlanceFromWalletAddr(self.__ethAccount._address)

    def GetMatic(self):
        return self.__matic

    def GetUsdc(self):
        return self.__usdc
    
    def GetUsdt(self):
        return self.__usdt

    def GetDai(self):
        return self.__dai

    def GetOQuick(self):
        return self.__oQuick

    def GetNQuick(self):
        return self.__nQuick


    def GetMaticBalance(self):
        return self.__matic.GetBalance()

    def GetUsdcBalance(self):
        return self.__usdc.GetBalance()
    
    def GetUsdtBalance(self):
        return self.__usdt.GetBalance()

    def GetDaiBalance(self):
        return self.__dai.GetBalance()

    def GetOQuickBalance(self):
        return self.__oQuick.GetBalance()

    def GetNQuickBalance(self):
        return self.__nQuick.GetBalance()

    def DoTransaction(self, transaction):
        transactionParam = {}
        transactionParam['chainId'] = transaction.GetChainId()
        transactionParam['gas'] = transaction.GetGas()
        transactionParam['gasPrice'] = transaction.GetGasPrice()
        transactionParam['from'] = transaction.GetFrom()
        contract = self.__w3.eth.contract(address=transaction.GetTo(), abi=TokenData.AUGUSTUSSWAPPER_ABI)
        contract.functions.set(transaction.GetData()).build_transaction(transactionParam)
        signedTrans = self.__w3.eth.account.signTransaction(contract, self.__ethAccount._private_key)
        self.__w3.eth.sendRawTransaction(signedTrans.rawTransaction)
