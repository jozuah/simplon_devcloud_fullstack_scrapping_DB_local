#j'importe les fonction du fichier script.py
from script_game import request_JV_website

import logging

import mysql.connector

from mysql.connector import Error

from flask import Flask, request, render_template

from flask import jsonify

#https://flask-cors.readthedocs.io/en/latest/
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='my_log.txtmy_log.txt', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def reset_logfile(logfile_path):
    ### Reset du fichier log
    my_txt_file= open(logfile_path, "r+")    
    # to erase all data  
    my_txt_file.truncate() 
    # to close file
    my_txt_file.close() 

class SQL_for_Gaming():

    def __init__(self):
        self.url_ps5_jv = 'https://www.jeuxvideo.com/meilleurs/machine-22/'
        self.url_PC_jv = 'https://www.jeuxvideo.com/meilleurs/machine-10/'
        self.url_XBOX_jv = 'https://www.jeuxvideo.com/meilleurs/machine-30/'
        self.ranking_dict_PS5 = request_JV_website(self.url_ps5_jv)
        self.ranking_dict_XBOX = request_JV_website(self.url_XBOX_jv)
        self.ranking_dict_PC = request_JV_website(self.url_PC_jv)
        self.conn = mysql.connector.connect(host='mysql_flask',
                                database='Top_Gaming',
                                user='root',
                                password='pw',
                                )

    def creationTable(self,support_name,connection_db_name) :
        try:
            sql_query = connection_db_name.cursor()

            #Création de la table en argument
            sql_query.execute(f"DROP TABLE IF EXISTS {support_name}")    
            sql_query.execute(f"CREATE TABLE IF NOT EXISTS {support_name} (number_rank INT PRIMARY KEY NOT NULL AUTO_INCREMENT,game_title VARCHAR(100) NOT NULL)")
            logging.info("[MYSQL] table  %s has been successfully created ", (support_name) )
        except Error as e :
            logging.warning("[MYSQL] message error:  %s", (e))

    def insertIntoTable(self,my_table,connection_db_name,dict_values) :
        
        try:
            sql_query = connection_db_name.cursor()
            #INSERT dans la table ps5

            #faire une range pour toutes les valeurs à recueillir
            for i in range (1,11):
                sql = f"""INSERT INTO {my_table} (game_title) VALUES ('{dict_values[i]}')"""
                #val = (my_table)
                sql_query.execute(sql)  
                connection_db_name.commit()
            logging.info("[MYSQL] Data from dict has been put into %s table ", (my_table) )
        except Error as e :
            logging.warning("[MYSQL] Fail to put data into %s table, Error : %s " % (my_table,e) )    
        except TypeError as e :
            logging.exception("[MYSQL Type] Fail to put data into %s table, message error : %s " % (my_table,e) )
            #logging.exception("message : %s ",e)

    def setAllDataIntoMysql (self):
        try:           
            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchall()

                logging.info("[MYSQL] Connection to %s Database - done ", (record) )

                self.creationTable("XBOX",self.conn)
                self.creationTable("PS5",self.conn)
                self.creationTable("PC",self.conn)

                self.insertIntoTable("PC",self.conn,self.ranking_dict_PC)
                self.insertIntoTable("XBOX",self.conn,self.ranking_dict_XBOX)
                self.insertIntoTable("PS5",self.conn,self.ranking_dict_PS5)
                
                print("Scrapping and setting data into MySQL have been done")
                logging.info("[MYSQL] All data has been put into %s", (record))

        except Error as e :
            logging.warning("[MYSQL] message error:  %s", (e))
    
        finally:
        #closing database connection.
            if(self.conn.is_connected()):
                logging.info("[MYSQL] End of connecion from %s", (record))
                cursor.close()
        
    def getValuesFromMysql(self):
        try:
            user_request = "n"
            while(user_request != 'y'):            
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
                user_request = input ("\n Do you want to leave MySql ? (y/n)")

        except Error as e :
            print ("Print your error msg", e)
        finally:
        #closing database connection.
            if(self.conn.is_connected()):
                print("End of connection")
                cursor.close()


@app.route('/')
def index():
    app.logger.info('Test du logger')
    return 'Hello, world!'

#pour récuperer des données
@app.route('/age/<int:my_age>', methods = ['GET'])
def getAge(my_age):
    return f'your age is {my_age}'

#pour récuperer des données, entre les 2 données je peux mettre n'importe quel séparateur : "espace","virgule","point-virgule"
@app.route('/user/<user_name> <int:user_age>')
def getUser(user_name,user_age):
    return f'{user_name} age is {user_age}'

#Test de la page internet
@app.route('/ma_page')
def my_page():
    return render_template("index.html")

### GET INFO FROM DATABASE ###
#Get all table from database
@app.route('/show_tables')
def showAllTables():
    try:
        conn = mysql.connector.connect(host='mysql_flask',
                                    database='Top_Gaming',
                                    user='root',
                                    password='pw',
                                    )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        myresult = cursor.fetchall()
        #fermeture de la base de donnée
        conn.close()
        logging.info("[MYSQL.route] All tables have been shown") 
        return jsonify(myresult)
    except Error as e :
            logging.warning("[MYSQL.route] Cant show tables, message error:  %s", (e))    

#Test de la page avec arguments:"http://localhost:4500/TOP?name=PS5&ranking=3"
#OU: "http://localhost:4500/TOP?name=PS5&ranking=""
@app.route('/TOP')
def showTables():
    try:
        console_name = request.args.get("name")
        ranking_number = request.args.get("ranking")
        #Ouverture de la base de donnée
        conn = mysql.connector.connect(host='mysql_flask',
                                    database='Top_Gaming',
                                    user='root',
                                    password='pw',
                                    )
        cursor = conn.cursor()
        if ranking_number == "":
            cursor.execute(f"SELECT * FROM {console_name}")
        else:
            cursor.execute(f"SELECT * FROM {console_name} LIMIT {ranking_number}")
        myresult = cursor.fetchall()
        conn.close()
        logging.info("[MYSQL.route] User asked to get data from '%s' table from 1 to %s - done" % (console_name,ranking_number)) 
        return jsonify(myresult)
    except Error as e :
            logging.warning("[MYSQL.route] Fail to show data from '%s' table, message error:  %s" % (console_name,e))

### MODIFIYING DATABASE ###
#http://localhost:4500/create_table?name=PS5
@app.route('/create_table')
def createTable():
    try:
        console_name = request.args.get("name")
        #Ouverture de la connection avec la DB
        conn = mysql.connector.connect(host='mysql_flask',
                                    database='Top_Gaming',
                                    user='root',
                                    password='pw',
                                    )
        sql_query = conn.cursor()
        #Création de la table en argument   
        sql_query.execute(f"CREATE TABLE IF NOT EXISTS {console_name} (number_rank INT PRIMARY KEY NOT NULL AUTO_INCREMENT,game_title VARCHAR(100) NOT NULL)")
        #fermeture de la base de donne
        conn.close()
        logging.info("[MYSQL.route] Table '%s' has been successefully created" % (console_name)) 
        return f'Table {console_name} has been created'
    except Error as e :
            logging.warning("[MYSQL.route] Fail to create '%s' table, message error:  %s" % (console_name,e))

#http://localhost:4500/drop_table?name=PS5
@app.route('/drop_table')
def dropTable():
    try:
        console_name = request.args.get("name")
        #ouverture de la base de donnée
        conn = mysql.connector.connect(host='mysql_flask',
                                    database='Top_Gaming',
                                    user='root',
                                    password='pw',
                                    )
        sql_query = conn.cursor()
        #Création de la table en argument   
        sql_query.execute(f"DROP TABLE IF EXISTS {console_name}")
        #fermeture de la base de donnée
        conn.close()
        logging.info("[MYSQL.route] Table '%s' has been successefully droped" % (console_name)) 
        return f'Table {console_name} has been dropped'
    except Error as e :
        logging.warning("[MYSQL.route] Fail to delete '%s' table, message error:  %s" % (console_name,e))


if __name__ == "__main__":
  
    reset_logfile("my_log.txt")
    
    Data_Gaming = SQL_for_Gaming()
   
    #Open database connection to do all stuff
    Data_Gaming.conn

    Data_Gaming.setAllDataIntoMysql()

    #If you want to print info from your SQL database
    #Data_Gaming.getValuesFromMysql()

    #Close Database afeter everything is done
    Data_Gaming.conn.close()
    
    app.run(host="0.0.0.0", port=3500, debug=True)
