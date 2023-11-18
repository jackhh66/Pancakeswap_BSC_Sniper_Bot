


class constant:
    def __init__(self, chainID):
        #print(f"Connected to ChainID: {chainID}")
        self.TigsSwapOracle = None
        self.TigsFeeUtils = None
        self.ZERO = "0x0000000000000000000000000000000000000000"  # This is constant across all chains
        self.WETH = None
        self.TIGS = None

        if int(chainID) == 56:
            self.TigsSwapOracle = "0x402Ff4e38D860Ce8378ED84E71FD678D48d36Df5"
            self.TIGS = "0x34FaA80FEC0233e045eD4737cc152a71e490e2E3"
            self.WETH = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

        elif int(chainID) == 31337:
            self.TigsSwapOracle = "0x402Ff4e38D860Ce8378ED84E71FD678D48d36Df5"
            self.TIGS = "0x34FaA80FEC0233e045eD4737cc152a71e490e2E3"
            self.WETH = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
            
        else:
            raise SystemExit("ChainID not Supported!")

