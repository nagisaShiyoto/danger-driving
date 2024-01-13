import sqlite3
import random


class Database_Manger:
    X_TABLE_NAME = "x_data"
    Y_TABLE_NAME = "y_data"

    def __init__(self, database_name):
        # Establishing a connection to the database (or creating it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)
        # Creating a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()
        collectDataAnswer = input("do you want to collect data?")
        # check if you want to collect data
        self.collect_data = True
        if collectDataAnswer == "n":
            self.collect_data = False
        self.formerXData = 0
        self.formerYData = 0

    def __del__(self):
        self.close_connection()

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
            "answer" FLOAT
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
            "answer" FLOAT
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
        create_table_query = f"""INSERT INTO {table_name} ("angle", "speed", "acceleration", "amount_of_cars", "Average_speed_of_cars", "road_angle", "stop_sign", "time_passed", "answer")
        VALUES( {inputData[0]}, {inputData[1]}, {inputData[2]},{inputData[3]},{inputData[4]}, {inputData[5]},{inputData[6]}, {inputData[7]}, {answer});"""
        self.cursor.execute(create_table_query)
        self.conn.commit()
