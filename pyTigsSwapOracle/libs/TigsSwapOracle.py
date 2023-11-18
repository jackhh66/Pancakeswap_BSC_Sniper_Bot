from pyTigsSwapOracle.imports import *


class TigsSwapOracle:
    """
    """
    def __init__(self, settings, w3, IERC20, w3U):
        self.settings, self.user_address, self.priv_key, self.w3, self.IERC20, self.w3U = settings, settings.settings["metamask_address"], settings.settings["metamask_private_key"], w3, IERC20, w3U
        self.constants = constant(self.w3.eth.chain_id)
        self.TigsSwapOracle = self.initRouter()

    def initRouter(self):
        with open("./pyTigsSwapOracle/ABIS/TigsSwapOracleV1.json") as f:
            contract_abi = json.load(f)
        TigsSwapOracle = self.w3.eth.contract(
            address=self.constants.TigsSwapOracle, abi=contract_abi)
        return TigsSwapOracle
    
    def getAmountsOutV3(self, pools, path, amountIn):
        return self.TigsSwapOracle.functions.getAmountsOutV3(
            pools, path, amountIn
            ).call()
    
    def getAmountsOutV2(self, amountIn, path, dexPath):
        return self.TigsSwapOracle.functions.getAmountsOutV2(
            amountIn, path, dexPath
            ).call()
    
    def getUSDPrice(self):
        return self.TigsSwapOracle.functions.getUSDPrice(
            self.IERC20.get_token_address()
            ).call()
    
    def getWBNBPrice(self):
        return self.TigsSwapOracle.functions.getUSDPrice(
            self.constants.WETH).call()
    
    def getAmountsOutTokenToBNB(self, inputAmount:int):
        return self.TigsSwapOracle.functions.getAmountsOut(
            self.IERC20.get_token_address(),
            self.constants.WETH,
            inputAmount
        ).call()

    def getAmountsOutBNBToToken(self, inputAmount:int):
        return self.TigsSwapOracle.functions.getAmountsOut(
            self.constants.WETH,
            self.IERC20.get_token_address(),
            inputAmount
        ).call()
    
    def getAmountsOutTokenToToken(self, tokenIn, tokenOut, inputAmount:int):
        return self.TigsSwapOracle.functions.getAmountsOut(
            Web3.toChecksumAddress(tokenIn),
            Web3.toChecksumAddress(tokenOut),
            inputAmount
        ).call()
    
    def getLiquidityUSD(self):
        return self.TigsSwapOracle.functions.getLiquidity(
            self.IERC20.get_token_address()
        ).call()


    def getSwapProtocollVersionEthToken(self):
        return self.TigsSwapOracle.functions.checkVersion(self.constants.WETH, self.IERC20.get_token_address()).call()
    def getSwapProtocollVersionTokenETH(self):
        return self.TigsSwapOracle.functions.checkVersion(self.IERC20.get_token_address(), self.constants.WETH).call()
    def getSwapProtocollVersionTokenToken(self, TokenIn, TokenOut):
        return self.TigsSwapOracle.functions.checkVersion(Web3.toChecksumAddress(TokenIn), Web3.toChecksumAddress(TokenOut)).call()

    def getTokenInfos(self):
        function_signature = self.TigsSwapOracle.encodeABI(fn_name="getTokenInfos", args=[self.IERC20.get_token_address()])
        data = {
            "to": self.TigsSwapOracle.address,
            "data": function_signature,
            "from": self.constants.ZERO
        }
        _data = self.w3.eth.call(data)
        call = abi.decode(
            ['uint256', 'uint256', 'uint256', 'uint256', 'bool', 'bool', 'bool', 'bool', 'string'],
            _data
        )
        buy_tax = round(
            ((call[0] - call[1]) / (call[0]) * 100) - 0.77, 3)
        sell_tax = round(
            ((call[2] - call[3]) / (call[2]) * 100) - 0.77, 3)

        if call[4] and call[5] and call[6] and call[7] == True:
            honeypot = False
        else:
            honeypot = True
        return buy_tax, sell_tax, honeypot
    
    def getWalletTokenDATA(self, tokenList):
        tokenList = [Web3.toChecksumAddress(address) for address in tokenList]
        tokenBalances ,tokenDecimals ,tokenPrice ,tokensVersion ,tokenAddress = self.TigsSwapOracle.functions.getWalletTokenDATA(self.user_address, tokenList).call()
        return tokenBalances ,tokenDecimals ,tokenPrice ,tokensVersion ,tokenAddress
    
    def getETHtoTokenPathV3(self):
        return self.TigsSwapOracle.functions.getSwapPathV3(self.constants.WETH, self.IERC20.get_token_address()).call()
    
    def getTokentoETHPathV3(self):
        return self.TigsSwapOracle.functions.getSwapPathV3(self.IERC20.get_token_address(),self.constants.WETH).call()
        
    def getTokentoTokenPathV3(self, tokenIn, tokenOut):
        return self.TigsSwapOracle.functions.getSwapPathV3(
                Web3.toChecksumAddress(tokenIn),
                Web3.toChecksumAddress(tokenOut)
            ).call()
    
    
    def getETHtoTokenPathV2(self):
        return self.TigsSwapOracle.functions.getSwapPathV2(self.constants.WETH, self.IERC20.get_token_address()).call()
    
    def getTokentoETHPathV2(self):
        return self.TigsSwapOracle.functions.getSwapPathV2(self.IERC20.get_token_address(),self.constants.WETH).call()
        
    def getTokentoTokenPathV2(self, tokenIn, tokenOut):
        return self.TigsSwapOracle.functions.getSwapPathV2(
                Web3.toChecksumAddress(tokenIn),
                Web3.toChecksumAddress(tokenOut)
            ).call()
    
    def getBNBBalance(self):
        return self.w3.eth.getBalance(self.user_address)

    def sendBNB(self, recipient_address, amount_BNB):
        try:
            amount_wei = self.w3U.to_wei(amount_BNB, 18)
            transaction = {
                'to': self.w3.toChecksumAddress(recipient_address),
                'value': amount_wei,
                'gasPrice': self.w3.eth.gasPrice + self.w3.to_wei(int(self.settings.settings["GWEI_OFFSET"]), 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(self.user_address),
                'gas': 210000
            }
            transaction['gas'], maxGasETH, notExtendMax = self.w3U.estimateGas(transaction)
            signed_txn = self.w3.eth.account.signTransaction(transaction, self.priv_key)
            if notExtendMax:
                txn_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
                txn_receipt = self.w3.eth.waitForTransactionReceipt(txn_hash, timeout=int(self.settings.settings["timeout"]))
            else:
                return False, maxGasETH, txn_hash.hex(), False
            if txn_receipt["status"] == 1:
                return True, maxGasETH, txn_hash.hex(), False
            else:
                return False,0, txn_hash.hex(), False
        except Exception as e:
            return False,0, "", e
        

    def TestSwapETHtoToken(self, inputAmount: float):
        try:
            v = self.getSwapProtocollVersionEthToken()
            inputBNB = self.w3U.to_wei(inputAmount, 18)
            if int(v) == 2:
                if self.SwapFromETHtoTokenV2(inputBNB):
                    return True
            elif int(v) == 3:
               if self.SwapFromETHtoTokenV3(inputBNB):
                    return True
        except:
            return False


    def TestSwapFromETHtoTokenV2(self, inputAmount: int):
        path, dexIdents  = self.getETHtoTokenPathV2()
        amountOut = self.getAmountsOutV2(inputAmount, path, dexIdents)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapETHtoTokenV2(
            path,
            dexIdents,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]) ,"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': int(inputAmount)}
        )
        return True


    def TestSwapFromETHtoTokenV3(self, inputAmount: int):
        path, _, pools, poolFees = self.getETHtoTokenPathV3()
        amountOut = self.getAmountsOutV3(pools, path, inputAmount)[-1]
        minOutput = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapETHtoTokenV3(
            path,
            pools,
            poolFees,
            minOutput
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': int(self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]), "gwei")),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': int(inputAmount)}
        )
        return True
    

    def SwapETHtoToken(self, inputAmount: float, trys: int):
        while trys:
            try:
                v = self.getSwapProtocollVersionEthToken()
                inputBNB = self.w3U.to_wei(inputAmount, 18)
                if int(v) == 2:
                    return self.SwapFromETHtoTokenV2(inputBNB)
                elif int(v) == 3:
                    return self.SwapFromETHtoTokenV3(inputBNB)
            except Exception as e:
                print(e)
                trys -= 1
                time.sleep(1)

    def SwapFromETHtoTokenV2(self, inputAmount: int):
        path, dexIdents  = self.getETHtoTokenPathV2()
        amountOut = self.getAmountsOutV2(inputAmount, path, dexIdents)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapETHtoTokenV2(
            path,
            dexIdents,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]) ,"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': int(inputAmount)}
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]
                



    def SwapFromETHtoTokenV3(self, inputAmount: int):
        path, dexIdents, pools, poolFees = self.getETHtoTokenPathV3()
        amountOut = self.getAmountsOutV3(pools, path, inputAmount)[-1]
        minOutput = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapETHtoTokenV3(
            path,
            pools,
            poolFees,
            minOutput
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': int(self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]), "gwei")),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': int(inputAmount)}
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]




    def SwapTokentoETH(self, inputAmount: float, trys: int = 1):
        while trys:
            try:
                v = self.getSwapProtocollVersionEthToken()
                inputToken = self.w3U.to_wei(inputAmount, self.IERC20.get_token_decimals())
                if int(v) == 2:
                    return self.SwapFromTokentoETHV2(inputToken)
                elif int(v) == 3:
                    return self.SwapFromTokentoETHV3(inputToken)
            except Exception as e:
                print(e)
                trys -= 1
                time.sleep(1)
        


    def SwapFromTokentoETHV3(self, inputAmount: int,):
        path, _, pools, poolFees = self.getTokentoETHPathV3()
        amountOut = self.getAmountsOutV3(pools, path, inputAmount)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapTokenToETHV3(
            path,
            pools,
            poolFees,
            inputAmount,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]),"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': 0
             }
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]



    def SwapFromTokentoTokenV3(self, tokenIn, tokenOut, inputAmount: int):
        path, dexIdents, pools, poolFees = self.getTokentoTokenPathV3(tokenIn, tokenOut)
        amountOut = self.getAmountsOutV3(pools, path, inputAmount)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapTokentoTokenV3(
            path,
            pools,
            poolFees,
            inputAmount,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]),"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': 0}
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]

    


    def SwapFromTokentoETHV2(self, inputAmount: int, trys: int = 1):
        path, dexIdents = self.getTokentoETHPathV2()
        amountOut = self.getAmountsOutV2(inputAmount, path, dexIdents)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapTokentoETHV2(
            path,
            dexIdents,
            inputAmount,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]),"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': 0}
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]


    def SwapFromTokentoTokenV2(self, tokenIn, tokenOut, inputAmount: int, trys: int = 1):
        path, dexIdents = self.getTokentoTokenPathV2(tokenIn, tokenOut)
        amountOut = self.getAmountsOutV2(inputAmount, path, dexIdents)[-1]
        amountOutMinimum = int(amountOut - (amountOut * int(self.settings.settings["Slippage"])) / 100)
        txn = self.TigsSwapOracle.functions.swapTokentoTokenV2(
            path,
            dexIdents,
            inputAmount,
            amountOutMinimum
        ).build_transaction(
            {'from': self.user_address,
             'gasPrice': self.w3.eth.gasPrice + Web3.toWei(int(self.settings.settings["GWEI_OFFSET"]),"gwei"),
             'nonce': self.w3.eth.getTransactionCount(self.user_address),
             'value': 0}
        )
        gas = self.w3U.estimateGas(txn)
        txn.update({'gas': gas[0]})
        signed_txn = self.w3.eth.account.signTransaction(
            txn,
            self.priv_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt = self.w3.eth.waitForTransactionReceipt(
            txn, timeout=self.settings.settings["timeout"])
        if txn_receipt["status"] == 1:
            return True, txn.hex(), gas[1]
        else:
            return False, txn.hex(), gas[1]
