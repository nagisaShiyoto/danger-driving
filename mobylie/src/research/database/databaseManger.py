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
        x_dict = {} # createing the dict

        # add the data to the dict
        x_dict["angle"] = self.fetchData(tableName,"angle")
        x_dict["speed"] = self.fetchData(tableName,"speed")
        x_dict["acceleration"] = self.fetchData(tableName,"acceleration")
        x_dict["amount_of_cars"] = self.fetchData(tableName,"amount_of_cars")
        x_dict["average_speed_of_cars"] = self.fetchData(tableName,"average_speed_of_cars")
        x_dict["stop_sign"] = self.fetchData(tableName,"stop_sign")
        x_dict["road_angle"] = self.fetchData(tableName,"road_angle")
        x_dict["slow_sign"] = self.fetchData(tableName,"slow_sign")
        x_dict["answer"] = self.fetchData(tableName,"answer")

        y_dict = {} # createing the dict

        # add the data to the dict
        y_dict["angle"] = self.fetchData(tableName,"angle")
        y_dict["speed"] = self.fetchData(tableName,"speed")
        y_dict["acceleration"] = self.fetchData(tableName,"acceleration")
        y_dict["amount_of_cars"] = self.fetchData(tableName,"amount_of_cars")
        y_dict["average_speed_of_cars"] = self.fetchData(tableName,"average_speed_of_cars")
        y_dict["stop_sign"] = self.fetchData(tableName,"stop_sign")
        y_dict["road_angle"] = self.fetchData(tableName,"road_angle")
        y_dict["slow_sign"] = self.fetchData(tableName,"slow_sign")
        y_dict["answer"] = self.fetchData(tableName,"answer")

        return (x_dict, y_dict)

    def close_connection(self):
        # Closing the connection
        self.conn.close()

    def insertRandomData(self):
        for b in range(1,11):
            i=random. randint(1, 10)
            self.insert_X_Data(i*10,i*20,i*5,i,i*20,i*10,i%2,i%2,i*2)
            #self.insert_Y_Data(i*10,i*20,i*5,i,i*20,i*10,i%2,i%2,i*2)

    def insert_X_Data(self,angle, speed, acceleration, amount_of_cars, average_speed_of_cars, road_angle, stop_sign, slow_sign, answer):
        create_table_query=f"""INSERT INTO x_data ("angle", "speed", "acceleration", "amount_of_cars", "Average_speed_of_cars", "road_angle", "stop_sign", "slow_sign", "answer")
        VALUES( {angle}, {speed}, {acceleration},{amount_of_cars},{ average_speed_of_cars}, {road_angle},{stop_sign}, {slow_sign}, {answer});"""
        print(create_table_query)
        self.cursor.execute(create_table_query)
        self.conn.commit()
