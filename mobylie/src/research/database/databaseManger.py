import sqlite3

class Database_Manger:
    def __init__(self, database_name):
        # Establishing a connection to the database (or creating it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)

        # Creating a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()

    def crateDatabase(self):
        # SQL query to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS x_data (
            "angle" FLOAT,
            "speed" FLOAT,
            "acceleration" FLOAT,
            "amount of cars" INTEGER,
            "Average speed of cars" FLOAT,
            "road angle" FLOAT,
            "stop sign" INTEGER,
            "slow sign" INTEGER,
            "answer" FLOAT
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS Y_data (
            "angle" FLOAT,
            "speed" FLOAT,
            "acceleration" FLOAT,
            "amount of cars" INTEGER,
            "Average speed of cars" FLOAT,
            "road angle" FLOAT,
            "stop sign" INTEGER,
            "slow sign" INTEGER,
            "answer" FLOAT
        );
        """

        # Executing the query
        self.cursor.execute(create_table_query)

        # Committing the changes
        self.conn.commit()

    def fetchData(self, tableName):
        # Execute the query to fetch all data from the 'speed' column
        self.cursor.execute(f"SELECT {tableName} FROM data")
        data = self.cursor.fetchall()

        # Extract 'speed' values into a list
        i = 0
        data_list = []
        while(i < len(data)):
            data_list.append(data[i][0])
            i += 1

        return data_list

    def create_dictionary(self):
        x_dict = {} # createing the dict

        # add the data to the dict
        x_dict["angle"] = self.fetchData("angle")
        x_dict["speed"] = self.fetchData("speed")
        x_dict["acceleration"] = self.fetchData("acceleration")
        x_dict["amount of cars"] = self.fetchData("amount of cars")
        x_dict["Average speed of cars"] = self.fetchData("Average speed of cars")
        x_dict["stop sign"] = self.fetchData("stop sign")
        x_dict["road angle"] = self.fetchData("road angle")
        x_dict["slow sign"] = self.fetchData("slow sign")
        x_dict["answer"] = self.fetchData("answer")

        y_dict = {} # createing the dict

        # add the data to the dict
        y_dict["angle"] = self.fetchData("angle")
        y_dict["speed"] = self.fetchData("speed")
        y_dict["acceleration"] = self.fetchData("acceleration")
        y_dict["amount of cars"] = self.fetchData("amount of cars")
        y_dict["Average speed of cars"] = self.fetchData("Average speed of cars")
        y_dict["stop sign"] = self.fetchData("stop sign")
        y_dict["road angle"] = self.fetchData("road angle")
        y_dict["slow sign"] = self.fetchData("slow sign")
        y_dict["answer"] = self.fetchData("answer")

        return (x_dict, y_dict)

    def close_connection(self):
        # Closing the connection
        self.conn.close()

    def insertData(self):
        #to-do
        cat = "cool"