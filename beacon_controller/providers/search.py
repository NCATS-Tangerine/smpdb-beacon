import pandas as pd
import re
from typing import List, Union, Dict


def search(df:pd.DataFrame, columns:Union[List[str], str], keywords:Union[List[str], str], min_score:int=0, column_multiplier:Dict[str, int]=None, unique_columns:Union[List[str], str]=None):
    if isinstance(columns, str):
        columns = [columns]
    elif not isinstance(columns, list):
        raise Exception(f'Columns must be of type string or list of strings, not {type(columns)}')

    if isinstance(keywords, str):
        keywords = [keywords]
    elif not isinstance(keywords, list):
        raise Exception(f'Keywords must be of type string or list of strings, not {type(columns)}')

    if not isinstance(column_multiplier, dict):
        column_multiplier = {}

    q = None

    for column in columns:
        for keyword in keywords:
            if q is None:
                q = df[column].str.contains(keyword, flags=re.IGNORECASE, regex=False)
            else:
                q |= df[column].str.contains(keyword, flags=re.IGNORECASE, regex=False)

    result = df[q == True]

    if len(result) == 0:
        return []

    result.drop_duplicates(subset=unique_columns, inplace=True)

    def count(row):
        c = 0
        for column in columns:
            m = 1 if column not in column_multiplier else column_multiplier[column]
            value = row[column]
            if isinstance(value, str):
                for keyword in keywords:
                    if keyword in value:
                        c += value.count(keyword) * m
        return c

    result['search_score'] = result.apply(count, axis=1)
    q = result['search_score'] >= min_score
    result = result[q == True]
    result.sort_values(by=['search_score'], ascending=False, inplace=True)

    return result.to_dict(orient='records')
