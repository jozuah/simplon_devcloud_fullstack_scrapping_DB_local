import mysql.connector
from mysql.connector import Error
#j'importe les fonction du fichier script.py
from script_game import request_JV_website



class SQL_for_Gaming():

    def __init__(self):
        self.url_ps5_jv = 'https://www.jeuxvideo.com/meilleurs/machine-22/'
        self.url_PC_jv = 'https://www.jeuxvideo.com/meilleurs/machine-10/'
        self.url_XBOX_jv = 'https://www.jeuxvideo.com/meilleurs/machine-30/'
        self.ranking_dict_PS5 = request_JV_website(self.url_ps5_jv)
        self.ranking_dict_XBOX = request_JV_website(self.url_XBOX_jv)
        self.ranking_dict_PC = request_JV_website(self.url_PC_jv)
        self.conn = mysql.connector.connect(host='ms',
                                database='Top_Gaming',
                                user='root',
                                password='pw',
                                )

    def creationTable(self,support_name,connection_db_name) :

        sql_query = connection_db_name.cursor()

        #Création de la table en argument
        sql_query.execute(f"DROP TABLE IF EXISTS {support_name}")       
        sql_query.execute(f"CREATE TABLE IF NOT EXISTS {support_name} (number_rank INT PRIMARY KEY NOT NULL AUTO_INCREMENT,game_title VARCHAR(100) NOT NULL)")

    def insertIntoTable(self,my_table,connection_db_name,dict_values) :

        sql_query = connection_db_name.cursor()
        #INSERT dans la table ps5

        #faire une range pour toutes les valeurs à recueillir
        for i in range (1,11):
            sql = f"""INSERT INTO {my_table} (game_title) VALUES ('{dict_values[i]}')"""
            #val = (my_table)
            sql_query.execute(sql)  
            connection_db_name.commit()


    def setAllDataIntoMysql (self):
        try:           
            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchall()
                print ("You're connected to - ", record)

                
                self.creationTable("XBOX",self.conn)
                self.creationTable("PS5",self.conn)
                self.creationTable("PC",self.conn)

                self.insertIntoTable("PS5",self.conn,self.ranking_dict_PS5)
                self.insertIntoTable("PC",self.conn,self.ranking_dict_PC)
                self.insertIntoTable("XBOX",self.conn,self.ranking_dict_XBOX)

                print("All data has been executed")
        except Error as e :
            print ("Print your error msg", e)
    
        finally:
        #closing database connection.
            if(self.conn.is_connected()):
                print("End of connection")
                cursor.close()

        
    def getValuesFromMysql(self):
        try:            
            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchall()
                print ("You're connected to - ", record)

                cursor.execute("SHOW TABLES")
                table_sql = cursor.fetchall()
                print(table_sql)


                my_sql_request = input ("\nYour request :")
                cursor.execute(f"{my_sql_request}")
                myresult = cursor.fetchall()
                for x in myresult:
                    print(x)

        except Error as e :
            print ("Print your error msg", e)
        finally:
        #closing database connection.
            if(self.conn.is_connected()):
                print("End of connection")
                cursor.close()


Data_Gaming = SQL_for_Gaming()

#Open database connection to do all stuff
Data_Gaming.conn

Data_Gaming.setAllDataIntoMysql()

Data_Gaming.getValuesFromMysql()

#Close Database afeter everything is done
Data_Gaming.conn.close()