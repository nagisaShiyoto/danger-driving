import sqlite3
import random
class Database_Manger:
    X_TABLE_NAME="x_data"
    Y_TABLE_NAME="y_data"
    def __init__(self, database_name):
        # Establishing a connection to the database (or creating it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)

        # Creating a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()
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
            "slow_sign" INTEGER,
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
            "slow_sign" INTEGER,
            "answer" FLOAT
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

    def fetchData(self, tableName,rowName):
        # Execute the query to fetch all data from the 'speed' column
        self.cursor.execute(f"SELECT {rowName} FROM {tableName}")
        data = self.cursor.fetchall()

        # Extract 'speed' values into a list
        i = 0
        data_list = []
        while(i < len(data)):
            data_list.append(data[i][0])
            i += 1

        return data_list

    def create_dictionary(self,tableName):
        dictinary = {} # createing the dict

        # add the data to the dict
        dictinary["angle"] = self.fetchData(tableName,"angle")
        dictinary["speed"] = self.fetchData(tableName,"speed")
        dictinary["acceleration"] = self.fetchData(tableName,"acceleration")
        dictinary["amount_of_cars"] = self.fetchData(tableName,"amount_of_cars")
        dictinary["average_speed_of_cars"] = self.fetchData(tableName,"average_speed_of_cars")
        dictinary["stop_sign"] = self.fetchData(tableName,"stop_sign")
        dictinary["road_angle"] = self.fetchData(tableName,"road_angle")
        dictinary["slow_sign"] = self.fetchData(tableName,"slow_sign")
        dictinary["answer"] = self.fetchData(tableName,"answer")

        return dictinary

    def close_connection(self):
        # Closing the connection
        self.conn.close()

    def insertRandomData(self):
        for b in range(1,11):
            i=random. randint(1, 10)
            self.insert_Data(self.X_TABLE_NAME,i*10,i*20,i*5,i,i*20,i*10,i%2,i%2,i*2)
            self.insert_Data(self.Y_TABLE_NAME,i*10,i*20,i*5,i,i*20,i*10,i%2,i%2,i*2)

    def insert_Data(self,table_name,angle, speed, acceleration, amount_of_cars, average_speed_of_cars, road_angle, stop_sign, slow_sign, answer):
        create_table_query=f"""INSERT INTO {table_name} ("angle", "speed", "acceleration", "amount_of_cars", "Average_speed_of_cars", "road_angle", "stop_sign", "slow_sign", "answer")
        VALUES( {angle}, {speed}, {acceleration},{amount_of_cars},{ average_speed_of_cars}, {road_angle},{stop_sign}, {slow_sign}, {answer});"""
        self.cursor.execute(create_table_query)
        self.conn.commit()
