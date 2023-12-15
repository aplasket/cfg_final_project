import pandas as pd
from IPython import embed
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


def read_data():
    file_path = 'best_selling_switch_games.csv'
    games_data = pd.read_csv(file_path)

    return games_data

def determine_overall_total(data):
    total = sum(data.copies_sold)

    print(f"The total number of copies of the top Switch games sold between "
          f"Mar 2017 and Nov 2022 equals: {total:,.0f} \n")


# def total_per_genre(data):
#     print(f"Total copies sold by genre between Mar 2017 and Nov 2022, from least to greatest: ")

# def total_per_year(data):
# def copies_by_year(data):
# def best_game_by_year(data):
def best_selling_game(data):

    max_index = data['copies_sold'].idxmax()
    title = data.loc[max_index, 'title']
    copies_sold = data.loc[max_index, 'copies_sold']
    developer = data.loc[max_index, 'developer']
    publisher = data.loc[max_index, 'publisher']

    # max_copies_row = data[data['copies_sold'] == max(data['copies_sold'])]
    # title = max_copies_row['title'].values[0]
    # copies_sold = max_copies_row['copies_sold'].values[0]
    # developer = max_copies_row['developer'].values[0]
    # publisher = max_copies_row['publisher'].values[0]
    print(f"The overall best selling game between 2017-2022 was {title} with {copies_sold:,.0f} copies sold. "
          f"It was developed by {developer} and published by {publisher}. \n")


def run():
    data = read_data()

    options = ["Total", "Genre", "Year", "Month", "Best", "Game", "All"]
    print("We have data on the best selling Nintendo Switch games between Mar 2017 and Nov 2022. "
          "Here are the list of data options we have available: \n"
          "Total: overall total number of copies sold of all games across 2017-2022, \n"
          "Genre: total number of copies sold per genre between 2017- 2022, \n"
          "Year: total number of copies of all games sold within each year, \n"
          "Month: months with the highest and lowest copies sold, given the input of a year, \n"
          "Best: best selling game between 2017-2022, \n"
          "Game: input a year, we'll tell you the best selling game of that year, \n"
          "All: all the above data points \n")

    user_selection = input(f"What would you like to know? Please input one of the following options: {', '.join(options)}. Your selection:  ").title()
    print("\n")

    while user_selection not in options:
        print(f"That is not a valid option")
        user_selection = input(f"Please input one of the following options: {', '.join(options)}. "
                               f"Your selection:  ").title()
        print("\n")

    if user_selection in options:
        if user_selection == "All":
            determine_overall_total(data)
            total_per_genre(data)
            total_per_year(data)
            copies_by_year(data)
            best_game_by_year(data)
            best_selling_game(data)
        elif user_selection == 'Total':
            determine_overall_total(data)
        elif user_selection == 'Genre':
            total_per_genre(data)
        elif user_selection == 'Year':
            total_per_year(data)
        elif user_selection == 'Month':
            copies_by_year(data)
        elif user_selection == 'Game':
            best_game_by_year(data)
        elif user_selection == 'Best':
            best_selling_game(data)

run()