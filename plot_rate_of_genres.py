from Merged_data import combined_data
import matplotlib.pyplot as plt

genres = []

def split_genres(vr_df):
    """
    Splits the genres within each row in the 'Genres' column of the data frame into individual genres
    and tracks them in a created dictionary.

    Args:
    vr_df (DataFrame): A cleaned and merged Dataframe which contains a 'Genres' column.

    Returns:
    dict: A dictionary with genres as keys and their initialized values set to 0.
    """

    #Creates a genres list
    genres = []
    #Creates a dictionary
    dictionary = {}

    #Places each found genre within the 'Genres' column into a list, ensuring no duplicates.
    for genre_list in vr_df['Genres']:
        for genre in genre_list.split(','):
            genre = genre.strip()
            if genre not in genres:
                genres.append(genre)

    #Initializes the values for each key in the dictionary to 0.
    for key in genres:
        dictionary[key] = 0

    return dictionary
  
def increase_count(vr_df, dictionary):
    """
    Increases the count of the value of each specific genre key in the dictionary based on how many
    times the occurance was found within the 'Genres' column in the given dataframe.

    Args:
    vr_df (DataFrame): A DataFrame containing a 'Genres' column.
    dictionary (dictionary): A dictionary with genres as keys and their counts as values (initially set to 0).

    Returns:
    dictionary: A dictionary with the updated number of occurances of each genre in the DataFrame.
    """
    for row in vr_df['Genres']:
        for genre in dictionary:
            if genre in row:
                dictionary[genre] += 1
    return dictionary

#Split the genres and count their occurances
genre_value_dict = split_genres(combined_data)
filled_genre_value_dict = increase_count(combined_data, genre_value_dict)

#Extract the list of keys and list of values from the dictionary
keys = list(filled_genre_value_dict.keys())
values = list(filled_genre_value_dict.values())
    
#Create a pie chart of the apperance rate of each genre
plt.figure(figsize=(10, 10))
plt.pie(values, labels=keys, autopct='%1.1f%%')
plt.title('Appearance Rate of Genres from the Most Popular Steam Games')
plt.show()