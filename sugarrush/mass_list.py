import pandas as pd
from pathlib import Path

data_folder = str(Path(__file__).parents[0]) + '/data'

def load_mass_list(filename='mass_list.xlsx'):
    df = pd.read_excel(f'{data_folder}/{filename}')
    mass_list = {}
    for index, row in df.iterrows():
        mass_list[str(row['dp'])] = [row['low'], row['high']]
    return mass_list

if __name__ =='__main__':
    mass_list = load_mass_list()
    print(mass_list)
