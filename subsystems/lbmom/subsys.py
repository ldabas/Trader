from dis import Instruction
import json
import quantlib.indicators_cal as indicators_cal
import pandas as pd


# hangukquant volatility targeting the asset level
# hangukquant volatility targeting the strategy
class Lbmom():
    
    def __init__(self, instruments_config, historical_df, simulation_start, vol_target):
        self.pairs = [(83, 94), (125, 207), (65, 183), (107, 169), (177, 273), (130, 194), (126, 297), (235, 236), (70, 259), (122, 139), (32, 95), (224, 252), (65, 67), (146, 157), (23, 39), (19, 98), (34, 216), (69, 230), (197, 264), (32, 291), (248, 288)]
        self.historical_df = historical_df
        self.simulation_start = simulation_start
        self.vol_target = vol_target
        with open(instruments_config) as f:
            self.instruments_config = json.load(f)
        self.sysname =="LBMOM"


    def extend_historical(self, instruments, historical_data):
        for inst in instruments:
            historical_data[f"{inst} adx"]=indicators_cal.adx_series(
                high = historical_data[inst + " high"],
                low = historical_data[inst + " low"],
                close = historical_data[inst + " close"],
                n = 14
            )

            for pair in self.pairs:
                historical_data[f"{inst} ema{str(pair)}"]= indicators_cal.ema_series(
                    series = historical_data[inst + " close"],
                    n = pair[0]
                ) - indicators_cal.ema_series(
                    series = historical_data[inst + " close"],
                    n = pair[1]
                )#fastMA - slowMA

        return historical_data

    def run_simulation(self, historical_data):
        #init parameters
        instruments = self.instruments_config["instruments"]
        #calculate indicators
        historical_data = self.extend_historical(instruments=instruments, historical_data=historical_data)
        #perform simlation
        portfolio_df = pd.DataFrame(index=historical_data[self.simulation_start:].index).reset_index()

        print(portfolio_df)

        
        
        pass
    
    def get_subsys_pos(self):
        self.run_simulation(historical_data=self.historical_df)

