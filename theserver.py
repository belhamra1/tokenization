import socketserver
from mainthing import *
from datetime import datetime 


######################################################################

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







PORT = 8000
response = b"Token generated successfully"

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_address = self.client_address[0]
        print(f"Connection established with {client_address}")
        buffer = self.request.recv(1024).decode()
        pan_number = buffer #.split("||")
        pan_number=str(pan_number)  #deja split return the buffer into string  donc str is useless
        taille=len(pan_number)

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
           #print(f"tokenli fchek: {token_fchek}")


           #transaction_time=resultats[0][1]
           #il faut convertir la chaîne de caractères en objet datetime
           #transaction_time = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S")
           #current_time=datetime.now()
           #time_difference=current_time - transaction_time
           #time_difference=time_difference.total_seconds()

           #if time_difference < 2*24*60*60:
           #    token=token_fchek
           #else :
           #   token=generate_token(taille,j)    
           
        else:
           token = generate_token(taille,j)
           create_table()
           insert_client_data(token,encrypted_pann,hashh)  
    
        
        
        print("Token:", token)
 
        # stocker la base de données 
        #create_table()
        #insert_client_data(token,encrypted_pann,hashh)   
         

        # Send response to the client
        self.request.sendall(response)
        print("Response sent:", response.decode())

create_table()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    server = ThreadedTCPServer(server_address, MyTCPHandler)
    print("Server started. Waiting for connections...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.shutdown()







'''
if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    server = socketserver.ThreadingTCPServer(server_address, MyTCPHandler)
    print("Server started. Waiting for connections...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.shutdown()

'''