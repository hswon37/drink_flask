#recommendation_engine.py
import numpy as np
import pandas as pd

def recommended_shows(target_name, matrix, shows_df, k=10):

    '''
    Recommends the top k(default 10) similar drinks to provided drink name.
            Arguments:
                    target_name (str): Drink name extracted from JSON API request
                    matrix (pandas.DataFrame): The similarity of cosine by drinks
                    shows_df (pandas.DataFrame): Dataframe of Netflix shows dataset
                    k (int): The number of drinks to recommend
            Returns:
                    response (dict): Recommended shows in JSON format
    '''

    try:

        title_iloc = shows_df.index[shows_df['name'] == target_name][0]

    except:

        return '현재 갖고 계신 주류는 추천이 불가능 합니다'

    recom_idx = matrix.loc[:, target_name].values.reshape(1, -1).argsort()[:, ::-1].flatten()[1:k+1]
    recom_name = shows_df.iloc[recom_idx, :].name.values
    recom_style = shows_df.iloc[recom_idx, :].styles.values
    target_name_list = np.full(len(range(k)), target_name)
    target_style_list = np.full(len(range(k)), shows_df[shows_df.name == target_name].styles.values)

    d = {
        'target_name':target_name_list,
        'target_style':target_style_list,
        'recom_name' : recom_name,
        'recom_style' : recom_style
    }

    response = pd.DataFrame(d).to_json(orient = 'columns')

    return response