import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_data = [ 'january', 'february', 'march', 'april', 'may', 'june' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    days_data = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]
    filter_option = [ 'month', 'day', 'both', 'none']

    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        while True:
            city = input('Type the city that you would like to explore '\
                '(Chicago / New York City / Washington)\n: ').lower()
            if city not in CITY_DATA.keys():
                print('It\'s not a valid city name, please try again.')
            else:
                break

        print('\n')

        # get user input for filter by month, day, both, or none
        while True:
            filter_selection = input('Would you like to filter by '\
                'month, day, both, or none at all?\n'\
                'Please type month/day/both/none for your selection.\n: ').lower()
            if filter_selection not in filter_option:
                print('It is not a valid input, please try again.\n')
            else:
                break

        if filter_selection in ('month','none'):
            day = 'all'
        if filter_selection in ('day','none'):
            month = 'all'

        # get user input for month (all, january, february, ... , june)
        if filter_selection in ('both','month'):
            while True:
                month = input('\nPlease type the month to filter\n: ').lower()
                if month not in months_data:
                    print('It\'s not a valid day, please try again.\n')
                else:
                    break

        # get user input for day of week (all, monday, tuesday, ... sunday)
        if filter_selection in ('both','day'):
            while True:
                day = input('\nPlease type the day to filter\n: ').lower()
                if day not in days_data:
                    print('It\'s not a valid day, please try again.\n')
                else:
                    break

        print('\nYou would like to explore city of {}, with following filter:'.format(city.title()))
        print('  Filter: {}'.format(filter_selection))
        print('  Month: {}'.format(month.title()))
        print('  Day: {}'.format(day.title()))
        confirm = input('Is that correct? If that is not correct, please type NO, '\
            'or if it\'s correct please ENTER to continue\n: ').lower()
        if confirm == 'no':
            print('Alright, let\'s restart\n')
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # converrt the Birth Year to integer
    # df['Birth Year'] = df['Birth Year'].apply(int)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months_data list to get the corresponding int
        month = months_data.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_comm_month = months_data[df['month'].mode()[0] - 1]
    print('Most common month is {}'.format(most_comm_month.title()))

    # display the most common day of week
    print('Most common day of the week is {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common hour is {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is '\
        '{}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most commonly used end station is '\
        '{}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    print('Most frequent combination of start station and end station trip is '\
        '\n    {}'.format(df['Route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time = df['Trip Duration'].sum()

    # calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # count trip
    trip_count = df['Trip Duration'].count()

    # display total, mean travel time, and count of trip
    print("Total travel time is {:,}, mean is {:,}, and trip count is {:,}"\
        .format(total_travel_time, mean_travel_time, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUsers count by types:')
    print(df['User Type'].value_counts())

    # display counts of gender and birth year except for Washington
    # that has no gender and year of birth data
    if city != 'washington':
        # Display counts of gender
        print('\nUsers count by gender:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        mode_year = df['Birth Year'].mode()[0]

        print('\nUsers by Year of Birth:')
        print('Earliest Year of Birth is {:.0f}'.format(min_year))
        print('Most Recent Year of Birth is {:.0f}'.format(max_year))
        print('Most Common Year of Birth is {:.0f}'.format(mode_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def slicer(df, rows):
    """Yield number of rows from dataframe."""
    for i in range(0, len(df), rows):
        yield df[i:i + rows]

# MAIN function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        view_df = input('\nWould you like to view the raw data? Enter yes or no.\n: ')
        if view_df.lower() == 'yes':
            for slice in slicer(df, 5):
                print(slice)
                view_next = input('\nWould you like to view next 5 rows? Enter yes or no.\n: ')
                if view_next != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n: ')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
