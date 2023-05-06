from web3 import Web3
from web3.middleware import geth_poa_middleware

class W3Connector:
    POLYGON_PUBLIC_RPC_URL = "https://polygon-rpc.com"
    #API_URL = "https://api.polygonscan.com/api"
    #API_KEY = "BTFAIPAZQQ536C8MNJ36Z4NS93WCEDBFBY"

    __instance = None
    def GetInstance():
        if (W3Connector.__instance == None):
            W3Connector.__instance = W3Connector()
        return W3Connector.__instance

    def __init__(self):
        if (W3Connector.__instance != None):
            raise("W3Connector already exist, call W3Connector.GetInstance instead")
        self.__w3 = Web3(Web3.HTTPProvider(W3Connector.POLYGON_PUBLIC_RPC_URL))
        self.__w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    @property
    def W3(self):
        return self.__w3

    def AddrCk(self, addr):
        return Web3.toChecksumAddress(addr)