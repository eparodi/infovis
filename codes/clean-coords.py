import pandas as pd

def to_coordinates(r, idx):
    if type(r) != str:
        return None
    r = r.replace('(', '').replace(')', '').replace('POINT', '')
    r = r.split(' ')[1:]
    if len(r) != 2:
        return None
    return float(r[idx])

df = pd.read_csv('../SF_Eviction_Notices.csv')
df['lat'] = df['Location'].apply(lambda r: to_coordinates(r, 1))
df['lng'] = df['Location'].apply(lambda r: to_coordinates(r, 0))
df = df[df['lat'].notnull()]

df.to_csv (r'../clean-sf.csv', index = None, header=True)
