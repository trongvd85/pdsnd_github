import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

MONTHS = {'january', 'february', 'march', 'april', 'may', 'june', 'all'}
DAYS = {'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington?\n')
       city = city.lower()
       if city not in CITY_DATA:
           print("Not found! Please try again.")
           continue
       else:
           break

    while True:
        month = input("Which month would you like to filter by? January, February, March, April, May, June or type 'all'?\n")
        month = month.lower()
        if month not in MONTHS:
            print("Not found! Please try again.")
            continue
        else:
            break

    while True:
        day = input("Are you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all'.\n")
        day = day.lower()
        if day not in DAYS:
            print("Not found! Please try again.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv("{}.csv".format(city.replace(" ", "_")))

    # Convert the Start and End Time columns to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    # Filter by month if applicable.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe.
        df = df.loc[df['month'] == month, :]

    # Filter by day of week if applicable.
    if day != 'all':
        # Filter by day of week to create the new dataframe.
        df = df.loc[df['day_of_week'] == day, :]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df["month"].mode()[0]
    print("Most Common Month:", common_month)

    common_day = df["day_of_week"].mode()[0]
    print("Most Common day:", common_day)

    df['hour'] = df["Start Time"].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    commonly_start_station = df["Start Station"].value_counts().idxmax()
    print("Most Commonly used start station:", commonly_start_station)

    commonly_end_station = df["End Station"].value_counts().idxmax()
    print("Most Commonly used end station:", commonly_end_station)

    combination_station = df.groupby(["Start Station", "End Station"]).count()
    print('Most Commonly used combination of start station and end station trip:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = sum(df['Trip Duration'])
    print("Total travel time:", total_travel_time / 86400, "Days")

    mean_travel_time = df["Trip Duration"].mean()
    print("Mean travel time:", mean_travel_time / 60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df["User Type"].value_counts()
    print("Users Types:", user_types)

    try:
        gender_types = df["Gender"].value_counts()
        print("Gender Types:", gender_types)
    except KeyError:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    try:
        earliest_year = df["Birth Year"].min()
        print("Earliest Year:", earliest_year)
    except KeyError:
        print('Birth Year stats cannot be calculated because Gender does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        counter1 = 0
        counter2 = 5

        while True:
            ch = input("Do you want to see raw data type yes or no?\n")
            ch = ch.lower()
            if ch == "yes":
                print(df.iloc[counter1:counter2])
                counter1 = counter1 + 5
                counter2 = counter2 + 5
            else:
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
