import time

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython import embed
import csv
from datetime import datetime

def read_data():
    data = []

    with open('best_selling_switch_games.csv', 'r') as games_csv:
        spreadsheet = csv.DictReader(games_csv)
        for row in spreadsheet:
            data.append(row)

    return data


def determine_overall_total(data):
    total_copies_sold = []
    for row in data:
        copiesSold = float(row['copies_sold'])
        total_copies_sold.append(copiesSold)

    total = sum(total_copies_sold)
    print(
        f"The total number of copies of the top Switch games sold between Mar 2017 and Nov 2022 equals: {total:,.0f} \n")


def total_per_genre(data):
    genres = {}

    for row in data:
        genre_type = row['genre']
        if genre_type in genres:
            genres[genre_type] += float(row['copies_sold'])
        else:
            genres[genre_type] = float(row['copies_sold'])

    sorted_genres_by_value = dict(sorted(genres.items(), key=lambda item: item[1]))

    print(f"Total copies sold by genre between Mar 2017 and Nov 2022, from least to greatest: ")

    for genre in sorted_genres_by_value:
        print(f"{genre}: {sorted_genres_by_value[genre]:,.0f}")

    with open('genre_totals.csv', 'w+', newline='') as csv_file:
        field_names = ['genre', 'copies_sold']
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
        spreadsheet.writeheader()

        for genre, copies_sold in genres.items():
            spreadsheet.writerow({'genre': genre, 'copies_sold': copies_sold})

    graph_option = input("Would you like to see a graph of this data? y/n ").lower()
    if graph_option == 'y':
        data_csv = pd.read_csv(r'genre_totals.csv')
        plt.figure(figsize=(12,8))
        sns.barplot(x='genre', y='copies_sold', hue='genre', data=data_csv)
        plt.title("Copies Sold by Genre")

        #rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        #set logarithic scale for y-axis since scope of values is so broad of 1M to 70M
        plt.yscale('log')
        #customize yaxis ticks and labels
        ticks = [1e5, 1e6, 1e7, 1e8]
        labels = ['100K', '1M', '10M', '100M']
        plt.yticks(ticks, labels)
        plt.show()


    print('\n \n')


def total_per_year(data):
    years = {}

    for row in data:
        specific_year = datetime.strptime(row['release_date'], '%Y-%m-%d').year
        if specific_year in years:
            years[specific_year] += float(row['copies_sold'])
        else:
            years[specific_year] = float(row['copies_sold'])
    # embed()
    sorted_years_by_key = dict(sorted(years.items()))
    print(f"Total copies sold by year: ")

    for year in sorted_years_by_key:
        print(f"{year}: {years[year]:,.0f}")

    max_pair = max(years.items(), key=lambda item: item[1])
    max_key, max_value = max_pair

    min_pair = min(years.items(), key=lambda item: item[1])
    min_key, min_value = min_pair
    print(f"The year {max_key} sold the most copies of best selling switch games with {max_value:,.0f} copies. "
          f"And the year {min_key} sold the least amount of switch games with only {min_value:,.0f} copies sold. \n")


def copies_by_year(data):
    year = input("What year between 2017-2022 would you like to see the highest and lowest copies sold by month? ")

    if not (2017 <= int(year) <= 2022):
        print("We do not have data for that year.\n")
        year = input("What year between 2017-2022 would you like to see the highest and lowest copies sold by month? ")

    copies_by_month = {}

    for row in data:
        date_object = datetime.strptime(row['release_date'], '%Y-%m-%d')
        specific_year = str(date_object.year)
        specific_month = str(date_object.month)

        if year == specific_year:
            if specific_month in copies_by_month:
                copies_by_month[specific_month] += float(row['copies_sold'])
            else:
                copies_by_month[specific_month] = float(row['copies_sold'])

    sorted_months_by_key = dict(sorted(copies_by_month.items()))

    determine_max_min(sorted_months_by_key, year)


def determine_max_min(copies, year):
    months = {
        '1': "January",
        '2': "February",
        '3': "March",
        '4': "April",
        '5': "May",
        '6': "June",
        '7': "July",
        '8': "August",
        '9': "September",
        '10': "October",
        '11': "November",
        '12': "December"
    }

    max_pair = max(copies.items(), key=lambda item: item[1])
    max_key, max_value = max_pair

    min_pair = min(copies.items(), key=lambda item: item[1])
    min_key, min_value = min_pair

    print(f"In {year}, {months[max_key]} had the most with {max_value:,.0f} switch games sold "
          f"and {months[min_key]} had the least with {min_value:,.0f} switch game copies sold.\n")

    graph_option = input(f"Would you like to see a graph of all months within {year}? y/n ").lower()
    if graph_option == 'y':

        with open('monthly_sales.csv', 'w+', newline='') as csv_file:
            field_names = ['month', 'copies_sold']
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
            spreadsheet.writeheader()

            for month, copies_sold in copies.items():
                spreadsheet.writerow({'month': months[month], 'copies_sold': copies_sold})

        data_csv = pd.read_csv(r'monthly_sales.csv')

        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                       'November', 'December']
        # Convert 'month' column to categorical with the specified order
        data_csv['month'] = pd.Categorical(data_csv['month'], categories=month_order, ordered=True)

        sns.barplot(x='month', y='copies_sold', hue='month', data=data_csv, dodge=False)
        plt.title(f"Copies Sold by Month in {year}")

        # rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        # # set logarithic scale for y-axis since scope of values is so broad of 1M to 70M
        plt.yscale('log')
        # # customize yaxis ticks and labels
        ticks = [1e5, 1e6, 1e7, 50e6]
        labels = ['100K', '1M', '10M', '50M']
        plt.yticks(ticks, labels)

        plt.show()


    print("\n")


def best_game_by_year(data):
    year = input("Enter a year between 2017-2022 to see the best selling game of that year: ")

    if not (2017 <= int(year) <= 2022):
        print("We do not have data for that year.\n")
        year = input("Enter a year between 2017-2022 to see the best selling game of that year: ")

    games = games_by_year(data)[year]
    sorted_games = dict(sorted(games.items(), key=lambda item: item[1]))
    max_pair = max(sorted_games.items(), key=lambda item: item[1])
    max_key, max_value = max_pair

    print(f"Best selling game for {year} was {max_key}, with {float(max_value):,.0f} copies sold \n")


def games_by_year(data):
    games = {}

    for row in data:
        date_object = datetime.strptime(row['release_date'], '%Y-%m-%d')
        specific_year = str(date_object.year)

        if specific_year in games:
            # if year exists, add game title as a key with the copies sold as value
            games[specific_year][row['title']] = float(row['copies_sold'])
        else:
            # If the year doesn't exist, create a new year with the game
            games[specific_year] = {row['title']: float(row['copies_sold'])}

    with open('total_per_year.csv', 'w+', newline='') as csv_file:
        field_names = ['Year', 'Title', 'Copies Sold']
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
        spreadsheet.writeheader()

        for year, games_data in games.items():
            for title, copies_sold in games_data.items():
                spreadsheet.writerow({'Year': year, 'Title': title, 'Copies Sold': copies_sold})

    return games


def best_selling_game(data):
    top_games = {}

    all_data = games_by_year(data)

    for year in all_data:
        max_pair = max(all_data[year].items(), key=lambda item: item[1])
        max_key, max_value = max_pair

        top_games[max_key] = max_value

    max_pair = max(top_games.items(), key=lambda item: item[1])
    max_key, max_value = max_pair

    for row in data:
        if row['title'] == max_key:
            developer = row['developer']
            publisher = row['publisher']

    print(f"The overall best selling game between 2017-2022 was {max_key} with {float(max_value):,.0f} copies sold. "
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
        user_selection = input(f"Please input one of the following options: {', '.join(options)}. Your selection:  ").title()
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
#
# data_csv = pd.read_csv(r'total_per_year.csv')
# sns.barplot(x='Year', y='Copies Sold', hue='Title', data=data_csv)
# plt.title("Copies Sold by Year")
# plt.show()