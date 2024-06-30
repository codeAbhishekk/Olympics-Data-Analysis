import pandas as pd




def preprocess(df,region_df):

    df = df[df['Season'] == 'Summer']

    # Merge with region
    df = df.merge(region_df, on='NOC', how='left')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One Hot Encoding
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)

    return df


# # Call the preprocess function
# processed_df = preprocess()

