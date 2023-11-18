from .imports import *
from .libs.W3Utils import *
from .libs.IERC20 import *
from .libs.TigsSwapOracle import *


class initSettings():
    def __init__(self):
        self.settings = self.initSettings()

    def reinitSettings(self):
        self.settings = self.initSettings()

    def initSettings(self):
        with open("./Settings.json") as f:
            keys = json.load(f)
        return keys
    
    def checkSettings(self):
        pass

    def updateSettings(self, new_settings):
        self.settings.update(new_settings)
        with open("./Settings.json", "w") as f:
            json.dump(self.settings, f)


class SwapOracle:
    def __init__(self, token):

        self.settings = initSettings()
        self.w3 = self.connect()

        self.w3U = W3Utils(self.settings, self.w3)
        if Web3.isAddress(token):
            pass
        else:
            token = constant(self.w3.eth.chain_id).TIGS
            
        self.IERC20 = IERC20(self.settings, self.w3, Web3.toChecksumAddress(token), self.w3U)
        self.SwapContract = TigsSwapOracle(self.settings, self.w3, self.IERC20, self.w3U)
        
        
    def connect(self):
        keys = self.settings.settings
        if keys["RPC"][:2].lower() == "ws":
            w3 = Web3(Web3.WebsocketProvider(keys["RPC"],request_kwargs={'timeout': int(keys["timeout"])}))
        else:
            w3 = Web3(Web3.HTTPProvider(keys["RPC"], request_kwargs={'timeout': int(keys["timeout"])}))
        return w3
    

    








