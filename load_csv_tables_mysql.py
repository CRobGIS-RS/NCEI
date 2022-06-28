from importlib.resources import path
import pandas as pd
import os
import mysql.connector
from mysql.connector import errorcode

# Set up DB in MySQL Server
db_connection = mysql.connector.connect(user="mysqlusr", password="C0nn0rc@ll13!")
db_cursor = db_connection.cursor()
#db_cursor.execute("CREATE DATABASE USClimateAgDB;")
db_cursor.execute("USE USClimateAgDB;")

path = "/home/robinsonc6/data/climate/"

# list comprehension
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

print(csv_files)

for csv in csv_files:
    file = os.path.join(path, csv)
    theme = csv.replace('.csv','').rsplit('-',1)[1]
    data = pd.read_csv(file, sep=",", index_col=0)
    data = data[(data['Year'] < 2022) & (data['Year'] > 1996)]
    data['County'] = data['County'].str.replace("'s","s")
    print(len(data))
    print(f"Creating table for {theme}")

    db_cursor.execute(f"CREATE TABLE {theme}(Id int(11) NOT NULL AUTO_INCREMENT, State varchar(2) NOT NULL, County varchar(50) NOT NULL, Year int(4) NOT NULL,\
                    January FLOAT(6,2) NOT NULL, February FLOAT(6,2) NOT NULL, March FLOAT(6,2) NOT NULL, April FLOAT(6,2) NOT NULL, May FLOAT(6,2) NOT NULL,\
                    June FLOAT(6,2) NOT NULL, July FLOAT(6,2) NOT NULL, August FLOAT(6,2) NOT NULL, September FLOAT(6,2) NOT NULL, October FLOAT(6,2) NOT NULL,\
                    November FLOAT(6,2) NOT NULL, December FLOAT(6,2) NOT NULL, PRIMARY KEY (`Id`));")

    data_tuples = list(data.itertuples(index=False, name=None))
    for tup in data_tuples:
        print(tup)
        db_cursor.execute(f"INSERT INTO {theme}(State, County, Year, January, February, March, April, May, June, July, August, September,\
                            October, November, December) VALUES {tup} ;")

db_cursor.execute("FLUSH TABLES;")