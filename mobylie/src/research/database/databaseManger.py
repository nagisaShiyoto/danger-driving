import sqlite3
import random
import mobylie.src.research.CCA_model as CCA

class Database_Manger:
    X_TABLE_NAME = "x_data"
    Y_TABLE_NAME = "y_data"
    def __init__(self, database_name,saveData):
        """
        create the satabase file if not exist
        input:database_name-the name of the file
        output:none
        """
        self.vid_num=0
        # Establishing a connection to the database (or creating it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)
        # Creating a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()
        # check if you want to collect data
        self.collect_data = False
        self.crateDatabase()
        if saveData:
            self.vid_num=self.fetchVidNum()
            #add the defult name of map
            self.addMap("map"+str(self.vid_num))
        self.formerXData = 0
        self.formerYData = 0




    def fetchVidNum(self):
        """get the map key
        input:none
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
            input:name-the name of the map
            output:none
            """
        add_map = f"""INSERT INTO mapKey ("map_name","map_num")
        VALUES( "{name}",{self.vid_num});"""
        self.cursor.execute(add_map)
        self.conn.commit()

    def crateDatabase(self):
        """
        create the tables
        input:none
        output:none
        """
        # SQL query to create the X table
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

        # SQL query to create the y table
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

        #sql to create the mapping table
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
        """
        gets a specific row data from a table
        input: tableName-the table of the name
                rowName-the name of the row
        retutn: all the data of the wanted row
        """
        # Execute the query to fetch all data from the 'speed' column
        self.cursor.execute(f"SELECT {rowName} FROM {tableName}")
        data = self.cursor.fetchall()

        # Extract 'speed' values into a list
        i = 0
        data_list = []
        #for loop?
        while i < len(data):
            data_list.append(data[i][0])
            i += 1

        return data_list

    def create_dictionary(self, tableName):
        """create a dictinary with all the data ordered by categories
        input:tableName- the name of the table to take all the data
        output:dict of all data"""
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

    def insert_Data(self, table_name, inputData,answer):
        """insert data to the x\y data table
        input: table_name-the name of the table(x/y)
                inputData-array of the data to predict from
                answer-what happened
            output:none"""
        add_table_query = f"""INSERT INTO {table_name} ("angle", "speed", "acceleration", "amount_of_cars", "Average_speed_of_cars", "road_angle", "stop_sign", "time_passed", "answer","vid_num")
        VALUES( {inputData[0]}, {inputData[1]}, {inputData[2]},{inputData[3]},{inputData[4]}, {inputData[5]},{inputData[6]}, {inputData[7]}, {answer},{self.vid_num});"""
        self.cursor.execute(add_table_query)
        self.conn.commit()
    def save_Data(self,detector,time_passed):
        """save all the data collected while driving
        input: dettector- all the data about what happned
                time passed- to save for calc
        output: none"""
        if self.formerXData != 0 and self.formerYData != 0:
            #saves data in database
            self.insert_Data(self.X_TABLE_NAME, self.formerXData[0],
                                    detector.ourCar.data.position.x - self.formerXData[1])
            self.insert_Data(self.Y_TABLE_NAME, self.formerYData[0],
                                    detector.ourCar.data.position.y - self.formerYData[1])
        #save the last way
        self.formerXData = (
            CCA.cca_model.getValues(detector, 0, time_passed)
            , detector.ourCar.data.position.x)
        self.formerYData = (
            CCA.cca_model.getValues(detector, 1, time_passed)
            , detector.ourCar.data.position.y)