from FetchPopularGames import vr_games_df
from GetReview import df_vr_apps
import pandas as pd

def merge_vr_data (vr_data_1, vr_data_2):
    '''

    Combine the known two original data into one data and delete the duplicate columns

    Args:
        vr_data_1（DataFrame): the first original data
        vr_data_2 (DataFrame): the second original data

    Returns:
        combined_df (DataFrame): The combined data table
    '''

    # try convert list data to str
    try:
        vr_data_1['Genres'] = vr_data_1['Genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    except:
        pass
    try:
        vr_data_1['Developers'] = vr_data_1['Developers'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    except:
        pass
    try:
        vr_data_2['Genres'] = vr_data_2['Genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    except:
        pass
    try:
        vr_data_2['Developers'] = vr_data_2['Developers'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    except:
        pass

    # Merge two Dataframes
    combined_df = pd.merge(vr_data_1, vr_data_2, on='Name', how='outer')
    combined_df = combined_df.drop_duplicates(subset=['Name'])

    return combined_df

def calculate_mean_number (combined_df, mean_column):
    '''

    Calculate the average of specific column

    Args:
        combined_df（DataFrame): The combined data table
        mean_column (list): The title of the column to be evaluated

    Returns:
        Mean_date (Float): the mean of specific column
    '''
    # For a sum of non-null data
    total_data = 0
    # How many non-empty data there are
    total_number = 0

    # Loop through to get the desired data
    for index, column_data in combined_df[f'{mean_column}'].items():
        # Filter non-empty data. If it is empty data, skip it
        if column_data == 'N/A' or column_data == 'Free' or column_data == '' or column_data == 'None':
            continue
        else:
            # Troubleshoot abnormal characters that may occur in the data
            if '$' in column_data:
                column_data = column_data.replace('$', '')
                total_number += 1
                total_data += float(column_data)
            else:
                total_number += 1
                total_data += float(column_data)

    mean_data = round(total_data/ total_number, 3)

    return mean_data

def fill_data (combined_df, column_to_fill, input_data):
    '''

    A place to fill specific data into empty data for a specific column

    Args:
        combined_df（DataFrame): The combined data table
        column_to_fill (list): The title of the column to be filled
        input_data (float): Specific data to fill in
    Returns:
        combined_df（DataFrame): A new table filled with data
    '''

    # Use loop to find empty data for a particular column and fill in the data
    for index, column_data in combined_df[f'{column_to_fill}'].items():
        if column_data == 'N/A' or column_data == 'Free' or column_data == '' or column_data == 'None':
            combined_df.loc[index, f'{column_to_fill}'] = input_data

    return combined_df


combined_df = merge_vr_data (df_vr_apps, vr_games_df)
combined_df = merge_vr_data (df_vr_apps, vr_games_df)
print(combined_df.T)
mean_number_of_reviews = calculate_mean_number (combined_df, 'Number_of_Reviews')
mean_price = calculate_mean_number (combined_df, 'Price')
combined_data = fill_data (combined_df, 'Number_of_Reviews', mean_number_of_reviews)
combined_data = fill_data (combined_df, 'Price', 'Free')
print(combined_data.T)

