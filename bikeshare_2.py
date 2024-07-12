import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    This function prompts the user to input their choice of city (from Chicago, New York City, and Washington),
    month (from January to December or "all" for no filter), and day of the week (Monday to Sunday or "all" for no filter).
    It uses a while loop to manage invalid inputs, ensuring that the user's choices are valid before proceeding.

    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the city name: ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Invalid city name. Please enter the city name again: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter the month name: ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                        'july', 'august', 'september', 'october', 'november', 'december']:
        month = input("Invalid month name. Please enter the month name again: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the day of the week: ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Invalid day of the week. Please enter the day of the week again: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    This function reads the city data file into a pandas DataFrame and applies filtering based on the specified month and day.
    It supports filtering by a specific month, a specific day of the week, both, or neither, allowing for a flexible analysis of the data.

    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv("chicago.csv")

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    This function calculates and prints the most common month, day of the week, and start hour for trips in the dataset.
    It leverages the pandas mode() function to find the most frequent values in the 'month', 'day_of_week', and 'hour' columns.
    The start hour is extracted from the 'Start Time' column, which is assumed to be in datetime format.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.

    Prints:
        The most popular month, day of the week, and start hour for trips in the dataset.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    This function calculates and prints the most commonly used start station, end station, and the most frequent combination
    of start and end stations for trips in the dataset. It uses the mode() function to identify these popular stations and
    combinations, and constructs a new 'Start End Station' column to facilitate the calculation of the most popular trip.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.

    Prints:
        The most popular start station, end station, and combination of start and end stations for trips in the dataset.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print('Most Popular Start End Station:', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    This function calculates the total travel time and the average travel time for trips in the dataset using the 'Trip Duration' column.
    It then converts these durations from seconds into more readable formats (hours, minutes, and seconds) for display.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.

    Prints:
        The total travel time and the average travel time for trips, formatted in hours, minutes, and seconds.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    This function calculates and prints counts of user types, gender distribution, and the earliest, most recent, and most common
    years of birth among users. It handles datasets with missing 'Gender' or 'Birth Year' columns by skipping these calculations
    if the columns are not present.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.

    Prints:
        Counts of user types (Subscriber, Customer).
        Gender distribution (Male, Female) if gender data is available.
        The earliest (oldest), most recent (youngest), and most common year of birth among users if birth year data is available.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:', user_types)

    # Display counts of gender
    genders = df['Gender'].value_counts()
    print('Genders:', genders)

    # Display earliest, most recent, and most common year of birth
    earliest_birth_year = df['Birth Year'].min()
    print('Earliest Birth Year:', earliest_birth_year)

    most_recent_birth_year = df['Birth Year'].max()
    print('Most Recent Birth Year:', most_recent_birth_year)

    most_common_birth_year = df['Birth Year'].mode()[0]
    print('Most Common Birth Year:', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Displays raw data to the user upon request.

    This function iteratively prompts the user to decide if they want to see 5 lines of raw data from the dataset at a time.
    It continues to display the next 5 lines of data upon each "yes" response until the user responds with a "no" or until all
    data has been displayed. The function ensures user input is validated for a clear yes/no response to continue or stop
    displaying raw data.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.

    Behavior:
        Iteratively displays 5 rows of raw data from the DataFrame on each iteration, based on user input.
        Continues until the user inputs 'no' or all data rows have been displayed.
    """
    
    print('\nWould you like to see raw data? Enter yes or no.')
    start_loc = 0
    while True:
        response = input().lower()
        if response == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if start_loc >= len(df):
                print("You've reached the end of the data.")
                break
            print('\nWould you like to see more raw data? Enter yes or no.')
        elif response == 'no':
            break
        else:
            print("Sorry, I didn't understand that. Please type 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)  # Call the function to display raw data
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
