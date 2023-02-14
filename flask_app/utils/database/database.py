import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print('I create and populate database tables.')

        data = ["institutions", "positions", "experiences", "skills"]

        for i in range(len(data)-1, -1, -1):
            temp = "DROP TABLE IF EXISTS " + data[i]
            self.query(temp)

        # Execute each sql file
        for j in data:
            filename = data_path + "create_tables/" + j + ".sql"
            fp = open(filename, "r")
            sql_file = fp.read().strip()
            garb = self.query(sql_file)
            fp.close()

        filename = data_path + "create_tables/" + "feedback" + ".sql"
        fp = open(filename, "r")
        sql_file = fp.read().strip()
        garb = self.query(sql_file)
        fp.close()

        filename = data_path + "create_tables/" + "users" + ".sql"
        fp = open(filename, "r")
        sql_file = fp.read().strip()
        garb = self.query(sql_file)
        fp.close()

        # read and open each file of initial data, then pass it to insertRows to add the data to the tables
        for k in data:
            filename = data_path + "initial_data/" + k + ".csv"
            fp = open(filename, "r")
            reader = csv.reader(fp)
            h = False
            cols = []
            params = []
            for line in reader:
                if not h:
                    cols = line
                    h = True
                    continue
                elif h:
                    params.append(line)

            self.insertRows(k, cols, params)

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id

    def getResumeData(self):
        # Master dictionary for data storage
        master_dict = dict()

        # Institution data
        institutions = self.query("SELECT * FROM institutions") 

        for i in institutions:
            inst_id = i['inst_id']
            type_ = i['type']
            name = i['name']
            dept = i['department']
            address = i['address']
            city = i['city']
            state = i['state']
            zip_ = i['zip']
            temp_dict = {'address': address, 'city': city, 'state': state, \
                'type': type_, 'zip': zip_, 'department': dept, 'name': name, 'positions': dict() }
            master_dict[inst_id] = temp_dict

        # Position data
        positions = self.query("SELECT * FROM positions")

        for p in positions:
            pos_id = p['position_id']
            inst_id = p['inst_id']
            title = p['title']
            respons = p['responsibilities']
            start_date = p['start_date']
            end_date = p['end_date']

            value_dict = {'end_date': end_date, 'responsibilities': respons, \
                'start_date': start_date, 'title': title, 'experiences': dict()}

            master_dict[inst_id]['positions'][pos_id] = value_dict

        # Experiences data
        experiences = self.query("SELECT * FROM experiences")

        for e in experiences:
            exp_id = e['experience_id']
            pos_id = e['position_id']
            name = e['name']
            description = e['description']
            hyperlink = e['hyperlink']
            start_date = e['start_date']
            end_date = e['end_date']

            value_dict2 = {'name': name, 'description': description, \
                'hyperlink': hyperlink, 'start_date': start_date, 'end_date': end_date, 'skills': dict()}

            for ins, info in master_dict.items():
                for pos in info['positions'].keys():
                    if pos_id == pos:
                        master_dict[ins]['positions'][pos_id]['experiences'][exp_id] = value_dict2

        # Skills data
        skills = self.query("SELECT * FROM skills")

        for s in skills:
            skill_id=s['skill_id']
            exp_id = s['experience_id']
            name = s['name']
            level = s['skill_level']

            value_dict3 = {'name': name, 'skill_level': level}

            for ins, info in master_dict.items():
                for pos, info2 in info['positions'].items():
                    
                    for exp in info2['experiences'].keys():
                        if exp == exp_id:
                            master_dict[ins]['positions'][pos]['experiences'][exp]['skills'][skill_id] = value_dict3

        return master_dict

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    # Create User
    def createUser(self, email='me@email.com', password='password', role='user'):
        encryptedPass = self.onewayEncrypt(password)
        self.query("""INSERT INTO users (role, email, password) VALUES (%s, %s, %s)""", [role, email, encryptedPass])
        # self.query(f"INSERT INTO users (role, email, password) VALUES ({role}, {email}, {encryptedPass})")

        
        return {'success': 1}

    # Authenticate
    def authenticate(self, email='me@email.com', password='password'):
        checkInserted = self.query(query      = """SELECT COUNT(*) as success FROM users WHERE email=%s AND password=%s""",
                           parameters = [email, self.onewayEncrypt(password)])[0]

        if checkInserted['success'] == 0:
            return {'success': 0}
        return {'success': 1}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


