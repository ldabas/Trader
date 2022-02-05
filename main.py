from lib2to3.pgen2.pgen import generate_grammar
import quantlib.data_utils as du
import quantlib.general_utils as gu

#df, instruments = du.get_sp500_df()
#df = du.extend_dataframe(traded=instruments, df=df)

#gu.save_file("./Data/historical_df.obj", (df, instruments))

(df, instruments) = gu.load_file("./Data/historical_df.obj")

import random

pairs = []

while len(pairs) <=20:
    pair = random.sample(list(range(16,300)),2)
    if pair[0]==pair[1]:continue
    else:
        pairs.append((min(pair[0], pair[1]),max(pair[0], pair[1])))

print(pairs)