DEVELOPMENT OF A TOKENIZATION SYSTEM For ONLINE PAYMENT 

This project involves the development of a tokenization system for online payment using Python Flask. The main components of the project are two files: tok.py and authentification.py. The system allows users to tokenize and detokenize sensitive payment information, enhancing security during online transactions.


GETTING STARTED:

To run the tokenization system on your local machine, follow the instructions below.

Prerequisites
*Python 3.x
*Flask (install using pip install Flask)
*SQLite3 (usually included with Python installations)

Running the Tokenization Server 

1-Open a terminal and navigate to the project directory.

2-Start the tokenization server by running the following command:
   
   $ python tok.py

3-The server should start running on http://localhost:8080.


TOKENIZATION PROCESS
To tokenize payment information, use the following curl command:

$ curl -X POST -H "Content-Type: application/json" -d '{"pan_number": "555213321212161777"}' http://localhost:8080/handle

You will receive a response similar to:

{
  "token": "5553885852144301101"
}

The token, encrypted PAN, and hash are stored in the SQLite3 database.

RUNNING THE AUTHENTICATION SERVER 

1-Open another terminal window and navigate to the project directory.

2-Start the authentication server by running the following command:

 $ python authentification.py

3-The server should start running on http://127.0.0.1:5000.

DETOKENIZATION PROCESS

To detokenize payment information, follow these steps:

1-Obtain an authentication token by sending a POST request with bank coordinates:
$ curl -i -X POST "http://127.0.0.1:5000/login" \
    -H "Content-Type: application/json" \
    -d '{"bank_coordinates":"cih"}'

   you will receive a response containing the session (jwt)

HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.2
Date: Wed, 30 Aug 2023 10:01:45 GMT
Content-Type: application/json
Content-Length: 80
Set-Cookie: session=b1795a18-9f9d-469a-8e76-6cc4251a9360.eRpolqxrkZp5OXDZ4XMYsWOV8bM; HttpOnly; Path=/
Connection: close

{
  "bank_coordinates": "cih",
  "id": "29599e10-dd1c-4c6a-a3b9-eb1fa8acf967"
}

2-use the obtained session to send a GET request for detokenization : 
$ curl -X GET "http://127.0.0.1:5000/@me?token=5553885852144301101" -H "Content-Type: application/json" -b "session=b1795a18-9f9d-469a-8e76-6cc4251a9360.eRpolqxrkZp5OXDZ4XMYsWOV8bM"

you will receive a response similar to : 
{
  "encrypted_pan":    
  "WW91ckZpeGVkU2FsdFZhbHVlfHxl_jEF_WxJGMetaDLxD05KfHwYvZDizVefWux2dixCWXmBdJ8g-Pfi7NBumCrsPQWzPw==",
  "hash": "78a66b70c71e71c383a9cefe170fd666582e2a1f8c56dae4afb7d3a224370f5c",
  "token": "5553885852144301101",
  "transaction_time": "2023-08-21 18:29:13"
}

NOTE : 
This project shwocases a basic implementation of a tokenization system for online payment using Flask. For production environments, consider enhancing security  measures and implementing proper authentication mechanisms . 
