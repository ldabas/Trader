from lib2to3.pgen2.pgen import generate_grammar
import quantlib.data_utils as du
import quantlib.general_utils as gu

from dateutil.relativedelta import relativedelta

#df, instruments = du.get_sp500_df()
#df = du.extend_dataframe(traded=instruments, df=df)

#gu.save_file("./Data/historical_df.obj", (df, instruments))

from subsystems.lbmom.subsys import Lbmom
(df, instruments) = gu.load_file("./Data/historical_df.obj")

print(instruments)

VOL_TARGET = 0.2
sim_start = df.index[-1] - relativedelta(year=5)
strat = Lbmom(instruments_config="./subsystems/lbmom/config.json", historical_df=df, \
    simulation_start=sim_start, vol_target=VOL_TARGET)


strat.get_subsys_pos()

""" import random

pairs = []

while len(pairs) <=20:
    pair = random.sample(list(range(16,300)),2)
    if pair[0]==pair[1]:continue
    else:
        pairs.append((min(pair[0], pair[1]),max(pair[0], pair[1])))

print(pairs) """