from flask import Flask, request, jsonify
from mainthing import *
from datetime import datetime

app = Flask(__name__)
messages = []


def read_day_from_file(numb_of_days):
    try:
        with open(numb_of_days, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file does not exist, return 2 and create the file with the value 2.
        write_counter_to_file(increment, 2)
        return 2


import sqlite3
def create_table():
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS clients ( 
         token STRING,
         encrypted_pan TEXT,
         hash TEXT ,
         transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              )
           '''  )
    conn.commit()
    conn.close()

def insert_client_data(token, encrypted_pan, hash):
    conn=sqlite3.connect("my_database.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO clients (token,encrypted_pan,hash) VALUES(?, ?, ?)",
                  (token, encrypted_pan, hash))
    conn.commit()
    conn.close()

@app.route('/handle', methods=['POST'])
def handle_request():
    client_address = request.remote_addr
    print(f"Connection established with {client_address}")
    
    pan_number = request.json.get('pan_number')
    pan_number = str(pan_number)
    taille = len(pan_number)

    print(f"Received PAN card number: {pan_number}")


    ###################################################
        #hna l9aleb dyal token pour que j augmente 
    increment = 'incrementc.txt'
    j = read_counter_from_file(increment)
        #print("Current value of j:", j)
    j += 1
    write_counter_to_file(increment, j)
        ####################################################

        
        
    hashh=generate_hash(pan_number)
        #print(f"Received hash card number: "+hashh)
    encrypted_pann=encrypt(pan_number,pan_number)
        #print(f"Received PAN card number: {encrypted_pann}")
         
    import sqlite3

    import datetime 
    current_time = datetime.datetime.now()
    numb_of_days='numb_of_days.txt'
    d=read_day_from_file(numb_of_days)
    two_days_ago = current_time - datetime.timedelta(days=d)
    formatted_date=two_days_ago.strftime('%Y-%m-%d %H:%M:%S')
    conn=sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT token,transaction_time FROM clients WHERE hash=? AND transaction_time >= ? ORDER BY transaction_time DESC LIMIT 1", (hashh,formatted_date))
    resultats=cursor.fetchall()
    cursor.close()
    conn.close()

        # mycode to generate the token number
    if resultats:
      token=resultats[0][0]
      token_str = token.decode('utf-8')
            
           
    else:
      token = generate_token(taille,j)
      create_table()
      insert_client_data(token,encrypted_pann,hashh) 
      token_str = token.decode('utf-8')
    
        
        
    print("Token:", token)
    token_str=token.decode('utf_8')

    
    # Rest of your code handling the received PAN card number
    
    print ( "Data received successfully")
           
    response_data={'token':token_str}      
    return jsonify(response_data), 200
##########################################
 
@app.route('/get', methods=['GET'])
def get_token_pan_hash():
    given_token = request.args.get('token')  # Get the token from the query parameters
    print("given_token",given_token)
    if given_token is None:
        return jsonify({'error': 'Token not provided'}), 400
    
    #convert the string token to an integer 
    given_token_string=given_token
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_pan, hash FROM clients WHERE token = ?", (given_token_string,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return jsonify({'error': 'Token not found'}), 404

    encrypted_pan, hash_value = result
    return jsonify({'encrypted_pan': encrypted_pan, 'hash': hash_value}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
