import webbrowser
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import folium


def top_ties(data, num, sort_by='summ'):
    """
    A function that handles top ties problem.
    :param sort_by: the name of columns which dataframe was sorted by
    :param data: pandas dataframe type that contains sorted value
    :param num: the number of values that we want to get
    :return: a pandas dataframe type contains top nums number of value with ties
    """
    while True:
        if num == len(data):
            return data
        # check nth value with n+1th value, if they are equal, consider a tie
        if data.iloc[num - 1][sort_by] != data.iloc[num][sort_by]:
            break
        else:
            num += 1
    return data.iloc[:num]


def task1():
    """
    Task 1 implement a function that allow users to enter the range of year
    and crime type.
    the program will generate a bar plot to show the month-wise total count of
    the user input crime type
    
    """

    start_year = int(input("Enter start year (YYYY):"))
    end_year = int(input("Enter end year (YYYY):"))
    crime_type = input("Enter crime type:")
    crime_type = "\'" + crime_type + "\'"
    command = "select crime_incidents.Month, sum(crime_incidents.Incidents_Count) as count " \
              "from crime_incidents " \
              "where crime_incidents.Crime_Type = {} and crime_incidents.Year >= {} and crime_incidents.Year <= {} " \
              "group by crime_incidents.Month;".format(crime_type, start_year, end_year)
    data = pd.read_sql_query(command, conn)
    # add month with count = 0 into data frame at correct position ( from 1 to 12)
    for i in range(1, 13):
        if not any(data.Month == i):
            insert_row = pd.DataFrame([[i, 0]], columns=['Month', 'count'])
            # split the data frame at the position where we want to insert a new row
            # then concat them together
            if i > 1:
                above = data.loc[:i - 1]
                below = data.loc[i:]
                data = pd.concat([above, insert_row, below], ignore_index=True)
            elif i == 1:
                below = data.loc[0:]
                data = pd.concat([insert_row, below], ignore_index=True)

    data.plot.bar(x="Month")
    plt.plot()
    plt.show()


def task2():
    """
    Task 2 implement a function that allow users to enter a integer 
    the program will generate a map to show the top n populous and 
    the lowest n not populous along with their population count.
    
    """

    m = folium.Map(location=[53.5444, -113.323], zoom_start=11)
    num = int(input('Enter number of locations:'))
    # this sql query gives us n area with most population and n area with lowest population
    command1 = 'select Latitude,Longitude,population.Neighbourhood_Name,' \
               '(CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE)as summ ' \
               'from population,coordinates ' \
               'where summ != 0 and population.Neighbourhood_Name=coordinates.Neighbourhood_Name ' \
               'and coordinates.Latitude!=0 and coordinates.Longitude!=0 ' \
               'group by population.Neighbourhood_Name ' \
               'order by summ;'
    command2 = 'select Latitude,Longitude,population.Neighbourhood_Name,' \
               '(CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN+NO_RESPONSE)as summ ' \
               'from population,coordinates ' \
               'where summ != 0 and population.Neighbourhood_Name=coordinates.Neighbourhood_Name ' \
               'and coordinates.Latitude!=0 and coordinates.Longitude!=0 ' \
               'group by population.Neighbourhood_Name ' \
               'order by summ DESC ; '
    data1 = pd.read_sql_query(command1, conn)
    data2 = pd.read_sql_query(command2, conn)
    while num > len(data1):
        print('The number you input is larger than the number of actual locations({})! '
              'Please input a new value!'.format(len(data1)))
        num = int(input("Enter number of locations:"))
    data1 = top_ties(data1, num)
    data2 = top_ties(data2, num)
    data = pd.concat([data1, data2], ignore_index=True)
    for i in range(0, len(data)):
        row = data.iloc[i]
        folium.Circle(location=[row["Latitude"], row["Longitude"]],
                      popup="{} <br> Population: {}".format(row["Neighbourhood_Name"], row["summ"]),
                      radius=int(row["summ"]) / 10, color="crimson", fill=True, fill_color="crimson").add_to(m)
    m.save('task2.html')
    # open html file
    webbrowser.open("task2.html")


def task3():
    """
    Task 3 implement a function that allow users to enter the range of years
    ,crime type and also the number of the neighborhoods.
    the program will generate a map to show the top n neighborhoods and their 
    crime count where the given crime type occurred most within the given range
    
    """

    start_year = int(input("Enter start year (YYYY):"))
    end_year = int(input("Enter end year (YYYY):"))
    crime_type = input("Enter crime type:")
    crime_type = "\'" + crime_type + "\'"
    num = int(input("Enter number of neighborhood:"))
    m = folium.Map(location=[53.5444, -113.323], zoom_start=11)

    '''
    This is the version without ties handling.
    command = 'select crime_incidents.Neighbourhood_Name,sum(crime_incidents.Incidents_Count)' \
              'as summ, coordinates.Latitude, coordinates.Longitude ' \
              'from crime_incidents, coordinates ' \
              'where crime_incidents.Crime_Type = {}  and crime_incidents.Year between {} and {} ' \
              'and coordinates.Neighbourhood_Name=crime_incidents.Neighbourhood_Name ' \
              'group by crime_incidents.Neighbourhood_Name ' \
              'order by summ DESC ' \
              'limit {}'.format(crime_type, start_year, end_year, num)
    '''

    command = 'select crime_incidents.Neighbourhood_Name,sum(crime_incidents.Incidents_Count)' \
              'as summ, coordinates.Latitude, coordinates.Longitude ' \
              'from crime_incidents, coordinates ' \
              'where crime_incidents.Crime_Type = {}  and crime_incidents.Year between {} and {} ' \
              'and coordinates.Neighbourhood_Name=crime_incidents.Neighbourhood_Name ' \
              'and coordinates.Latitude!=0 and coordinates.Longitude!=0 ' \
              'group by crime_incidents.Neighbourhood_Name ' \
              'order by summ DESC ' \
              ';'.format(crime_type, start_year, end_year)
    data = pd.read_sql_query(command, conn)
    '''
    # check nth value with n+1th value, if they are equal, consider a tie
    while True:
        if data.iloc[num - 1]['summ'] != data.iloc[num]['summ']:
            break
        else:
            num += 1
    data = data.iloc[:num]
    '''
    # check if user input is too big
    while num > len(data):
        print('The number you input is larger than the number of actual neighborhoods({})! '
              'Please input a new value!'.format(len(data)))
        num = int(input("Enter number of neighborhood:"))
    data = top_ties(data, num)
    # print(data)
    for i in range(0, len(data)):
        row = data.iloc[i]
        folium.Circle(location=[row["Latitude"], row["Longitude"]],
                      popup="{} <br> Population: {}".format(row["Neighbourhood_Name"], row["summ"]),
                      radius=int(row["summ"]), color="crimson", fill=True, fill_color="crimson").add_to(m)
    m.save('task3.html')
    # open html file
    webbrowser.open("task3.html")


def task4():
    """
    Task 4 implement a function that allow users to enter the range of years
    and also the number of the neighborhoods.
    the program will generate a map to show the top n neighborhoods to show 
    population ratio within the provided range
    also the map will the also showed the most frequent crime type in each of 
    these neighborhoods
    """

    start_year = int(input("Enter start year (YYYY):"))
    end_year = int(input("Enter end year (YYYY):"))
    num = int(input("Enter number of neighborhood:"))
    m = folium.Map(location=[53.5444, -113.323], zoom_start=11)
    command = 'select population.Neighbourhood_Name,(population.CANADIAN_CITIZEN+' \
              'population.NON_CANADIAN_CITIZEN+population.NO_RESPONSE)as summ,' \
              'sum(crime_incidents.Incidents_Count) as summ_c,coordinates.Latitude,coordinates.Longitude ' \
              'from population, crime_incidents,coordinates ' \
              'where summ != 0 and crime_incidents.Year between {} and {} ' \
              'and population.Neighbourhood_Name = crime_incidents.Neighbourhood_Name' \
              ' and population.Neighbourhood_Name=coordinates.Neighbourhood_Name ' \
              'and coordinates.Latitude!=0 and coordinates.Longitude!=0 ' \
              'group by population.Neighbourhood_Name'.format(start_year, end_year)

    data = pd.read_sql_query(command, conn)
    while num > len(data):
        print('The number you input is larger than the number of actual neighborhoods({})! '
              'Please input a new value!'.format(len(data)))
        num = int(input("Enter number of neighborhood:"))
    data['summ'] = data['summ'].astype(int)
    data['summ_c'] = data['summ_c'].astype(int)
    data['c_rate'] = data['summ_c'] / data['summ']
    # print(data)
    # sort the data by c_rate with descending order
    data.sort_values(by=['c_rate'], inplace=True, ascending=False)
    """
    while True:
        if data.iloc[num - 1]['c_rate'] != data.iloc[num]['c_rate']:
            break
        else:
            num += 1
    data = data.iloc[:num]
    """
    data = top_ties(data, num, sort_by='c_rate')
    for i in range(0, len(data)):
        row = data.iloc[i]
        # crime_type = data2[data2['Neighbourhood_Name'] == row["Neighbourhood_Name"]].Crime_Type.item()
        crime_type = get_crime_type(row["Neighbourhood_Name"], start_year, end_year)
        name = row["Neighbourhood_Name"]
        folium.Circle(location=[row["Latitude"], row["Longitude"]],
                      popup="{}<br>{}<br>{}".format(name, crime_type, row["c_rate"]),
                      radius=row["c_rate"] * 1000, color="crimson", fill=True, fill_color="crimson").add_to(m)
    m.save('task4.html')
    webbrowser.open("task4.html")


def get_crime_type(neighborhood, start_year, end_year):
    """
    This function returns a string that indicate most frequent crime type with ties
    (returns all if the count of a crime type is the same) of a certain area.
    :param neighborhood: a string type param which is the name of an area
    :param start_year: start_year for query
    :param end_year: end_year for query
    :return: a string that indicate crime type
    """
    nei_name = "\'" + neighborhood + "\'"
    command = 'select t1.Neighbourhood_Name as Neighbourhood_Name,t1.Crime_Type as Crime_Type,t1.summ as summ ' \
              'from(select crime_incidents.Neighbourhood_Name,crime_incidents.' \
              'Crime_Type,sum( crime_incidents.Incidents_Count)as summ ' \
              'from crime_incidents ' \
              'where crime_incidents.Year between {} and {} ' \
              'group by  crime_incidents.Neighbourhood_Name,crime_incidents.Crime_Type)as t1 ' \
              'where t1.Neighbourhood_Name={} ' \
              'order by t1.summ desc'.format(start_year, end_year, nei_name)
    data = pd.read_sql_query(command, conn)
    data = top_ties(data, 1)
    crime_type = ''
    for i in range(0, len(data)):
        row = data.iloc[i]
        crime_type += row['Crime_Type']  # data[row['Neighbourhood_Name'] == neighborhood].Crime_Type.item()
    return crime_type


if __name__ == '__main__':
    db_name = input("Please input database file name:\n")
    conn = sqlite3.connect(db_name)
    # connect to sqlite database,open a database in the path

    while True:
        user_input = input("1: Q1\n2: Q2\n3: Q3\n4: Q4\nE: Exit\nEnter your choice:")
        if user_input == '1':
            task1()
        elif user_input == '2':
            task2()
        elif user_input == '3':
            task3()
        elif user_input == '4':
            task4()
        elif user_input.upper() == "E":
            exit()
        else:
            print("Invalid user input!!!")
