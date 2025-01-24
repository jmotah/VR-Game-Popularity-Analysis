from Merged_data import combined_data
import pandas as pd
import plotly.express as px

def price_vs_num_review_plot(vr_games_df):
    """
    Creates and displays a scatter plot expressing the relationship between the price of VR games and
    the number of reviews they have.

    Args:
    vr_games_df (DataFrame): A cleaned DataFrame containing VR game data. Crucially, this contains the
                             columns named 'Name' for the Name of the VR game, 'Price' for the price 
                             of the game, and 'Number_of_Reviews' for the number of reviews the game
                             has received.

    Returns:
    Doesn't return an individual value, but displays a scatter plot.
    """

    #Converts the values within the 'Price_x' column adn the 'Number of Reviews' column to a numeric value.
    #In addition, converts any price of 'Free' to 0 and and price including the dollar sign to remove it.
    vr_games_df['Price'] = vr_games_df['Price'].replace('Free', 0).replace(r'[\$,]', '', regex=True)
    vr_games_df['Price'] = pd.to_numeric(vr_games_df['Price'])
    vr_games_df['Number_of_Reviews'] = pd.to_numeric(vr_games_df['Number_of_Reviews'])

    #Creates a scatter plot with specified data.
    plot = px.scatter(
        vr_games_df,
        x='Price',
        y='Number_of_Reviews',
        hover_data=['Name', 'Price', 'Number_of_Reviews'],
        labels={'Price': 'Price (in $)', 'Number_of_Reviews': 'Number of Reviews'},
        title='The Price of VR Games vs Number of Reviews They Receive',
        height=500
    )
    
    #Updates the layout of the plot by centering the title and setting the text for the title
    plot.update_layout(
        title={
            'text': "Price vs Number of Reviews for VR Games",
            'x': 0.5,
        }
    )
    #Displays the plot
    plot.show()

#Calls the function to show the scatter plot with the combined_data cleaned data set
price_vs_num_review_plot(combined_data)