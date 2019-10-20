import pandas as pd

df = pd.read_csv('../london-population.csv')
df = df.melt(id_vars=["gss_code", "district", "component", "sex", "age"], 
        var_name="Date", 
        value_name="Population")
df.to_csv (r'../clean-london.csv', index = None, header=True)
