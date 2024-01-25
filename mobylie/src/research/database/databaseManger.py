import sqlite3
import random


class Database_Manger:
    X_TABLE_NAME = "x_data"
    Y_TABLE_NAME = "y_data"
    def __init__(self, database_name):
        self.vid_num=0
        # Establishing a connection to the database (or creating it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)
        # Creating a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()
        collectDataAnswer = input("do you want to collect data?")
        # check if you want to collect data
        self.collect_data = False
        self.crateDatabase()
        if collectDataAnswer != "n":
            self.collect_data = True
            self.vid_num=self.fetchVidNum()
            #add the defult name of map
            self.addMap("map"+str(self.vid_num))
        self.formerXData = 0
        self.formerYData = 0




    def fetchVidNum(self):
        """get the map key
        output:mapKey"""
        self.cursor.execute(f"SELECT map_num FROM mapKey ORDER BY map_num DESC LIMIT 1")
        data = self.cursor.fetchall()
        if(len(data)==0):
            return 0
        return data[0][0]+1

    def __del__(self):
        self.close_connection()

    def addMap(self,name):
        """add map name and his key so i we can take it after
            name:the name of the map"""
        add_map = f"""INSERT INTO mapKey ("map_name","map_num")
        VALUES( "{name}",{self.vid_num});"""
        self.cursor.execute(add_map)
        self.conn.commit()

    def crateDatabase(self):
        # SQL query to create a table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.X_TABLE_NAME} (
            "angle" FLOAT,
            "speed" FLOAT,
            "acceleration" FLOAT,
            "amount_of_cars" INTEGER,
            "average_speed_of_cars" FLOAT,
            "road_angle" FLOAT,
            "stop_sign" INTEGER,
            "time_passed" INTEGER,
            "answer" FLOAT,
            "vid_num" INTEGER 
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.Y_TABLE_NAME} (
            "angle" FLOAT,
            "speed" FLOAT,
            "acceleration" FLOAT,
            "amount_of_cars" INTEGER,
            "average_speed_of_cars" FLOAT,
            "road_angle" FLOAT,
            "stop_sign" INTEGER,
            "time_passed" INTEGER,
            "answer" FLOAT,
            "vid_num" INTEGER
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS mapKey (
            "map_name" STRING,
            "map_num" INTEGER PRIMARY KEY
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

    def fetchData(self, tableName, rowName):
        # Execute the query to fetch all data from the 'speed' column
        self.cursor.execute(f"SELECT {rowName} FROM {tableName}")
        data = self.cursor.fetchall()

        # Extract 'speed' values into a list
        i = 0
        data_list = []
        while i < len(data):
            data_list.append(data[i][0])
            i += 1

        return data_list

    def create_dictionary(self, tableName):
        dictinary = {"angle": self.fetchData(tableName, "angle"), "speed": self.fetchData(tableName, "speed"),
                     "acceleration": self.fetchData(tableName, "acceleration"),
                     "amount_of_cars": self.fetchData(tableName, "amount_of_cars"),
                     "average_speed_of_cars": self.fetchData(tableName, "average_speed_of_cars"),
                     "stop_sign": self.fetchData(tableName, "stop_sign"),
                     "road_angle": self.fetchData(tableName, "road_angle"),
                     "time_passed": self.fetchData(tableName, "time_passed"),
                     "answer": self.fetchData(tableName, "answer")}  # createing the dict

        # add the data to the dict

        return dictinary

    def close_connection(self):
        # Closing the connection
        self.conn.close()

    def insertRandomData(self):
        for b in range(1, 11):
            i = random.randint(1, 10)
            self.insert_Data(self.X_TABLE_NAME, (i * 10, i * 20, i * 5, i, i * 20, i * 10, i % 2, i % 2), i * 2)
            self.insert_Data(self.Y_TABLE_NAME, (i * 10, i * 20, i * 5, i, i * 20, i * 10, i % 2, i % 2), i * 2)

    def insert_Data(self, table_name, inputData,answer):
        add_table_query = f"""INSERT INTO {table_name} ("angle", "speed", "acceleration", "amount_of_cars", "Average_speed_of_cars", "road_angle", "stop_sign", "time_passed", "answer","vid_num")
        VALUES( {inputData[0]}, {inputData[1]}, {inputData[2]},{inputData[3]},{inputData[4]}, {inputData[5]},{inputData[6]}, {inputData[7]}, {answer},{self.vid_num});"""
        self.cursor.execute(add_table_query)
        self.conn.commit()
