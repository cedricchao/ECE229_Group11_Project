import os

import pandas as pd

"""
Combination of data collected for a dataframe
"""
if __name__ == "__main__":
    file_dir = 'data_collection'  # the path to data_collection file
    files = os.listdir(file_dir)
    df1 = pd.read_csv(os.path.join(file_dir, files[0])).set_index('Unnamed: 0', drop=True).reset_index(drop=True)
    for e in files[1:]:
        if '.csv' in e:
            df2 = pd.read_csv(os.path.join(file_dir, e), encoding='utf-8').set_index('Unnamed: 0',
                                                                                     drop=True).reset_index(drop=True)
            df1 = pd.concat([df1, df2],axis=0)
    print(df1)
    df1.to_csv('dataframe_comb.csv') # the path to store the combined dataframe csv
