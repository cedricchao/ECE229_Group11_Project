import pandas as pd
"""
small sample to use SEASCAPE data
download from https://github.com/dcao/seascape/tree/master/data
"""
if __name__ == "__main__":
    f_name = 'data.csv'
    df = pd.read_csv(f_name)
    dep = []
    for courses in df['course']:
        de = courses.split(' ')
        dep.append(de[0])
    df['department'] = dep
    # print(df.head(5))
    print(df.columns)
    """
    top five classes by gpaAvg
    """
    top_df = df.sort_values('gpaAvg', ascending=False).groupby('department').head(5)
    top_df = top_df.dropna()
    # print(top_df[['course', 'gpaAvg']])
    print(top_df.info)
