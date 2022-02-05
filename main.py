from lib2to3.pgen2.pgen import generate_grammar
import quantlib.data_utils as du
import quantlib.general_utils as gu

#df, instruments = du.get_sp500_df()
#df = du.extend_dataframe(traded=instruments, df=df)

#gu.save_file("./Data/historical_df.obj", (df, instruments))

(df, instruments) = gu.load_file("./Data/historical_df.obj")
print(df)