SOCKET QUIZ-ING

- - - - - - - - - - - 
NAME   :  NIKHIL AGARWAL
ROLL NO:  IMT20919060
- - - - - - - - - - - 

LANGUAGE : PYTHON3

MODULES TO BE INSTALLED:
1) socket
2) pickle
3) time
4) sys
5) Thread
6) random

TRANSPORT PROTOCOL : TCP
PORT NUMBER : 12000

- - - - - - - - - - - 

 
INSTRUCTION :

1. Download the files server.py, client.py and questions.txt
2. Download the above mentioned modules ( using pip install command )
3. run server.py using the command ---> python3 server.py 
4. run client.py using the command ---> python3 client.py ( on all the 3 clients )

- - - - - - - - - - - 

Project Overview:

1. There is a host(server) who conducts the show and participants/players who provide answers.
 
2. There are three participants in the show(clients).

3. The players receive the question.
	a. They can press buzzer to answer(within 10 seconds)

4. whoever press the buzzer is given chance to answer.

5. server collects the responses and whoever pressed the first is evaluated 
	a. +1 for correct answer
	b. -0.5 for wrong answer or answering after 10 seconds of pressing buzzer

6. which ever client doesn't pressed the buzzer, will have option to continue

7. scores are displayed

8. Points : 3 to 7 is repeated until score of one of the client reaches 5 points


- - - - - - - - - - - 

Project Description:

A) SENDIND AND RECIEVING DATA:
---> 
using socket module, we can easily send data
		1) from client to server
		2) from server to client
	
Data is send in bytes, thus every {string} input is decode and encode wherever
necessary.

to send objects, I have used pickle module which converts python objects into 
bytes. ( THIS IS REALLY HELPFUL )

B) BUZZER

buzzer was a tricky part to execute, mainly because 
once a input() function is call, python script doesn't run unless a input is given

to solve this, I have used Thread from threading module, so two process can take place
simultaneously 
	1) INPUT for BUZZER
	2) Sending data accordingly to server

also i have used time module to get buzzer timing, which can be used during evaluation
( minimum buzzer time will only be evaluated )

C) QUIZ-ING

To implement quiz-ing, I have used while loop (on both server and client side )
which will run unless score reaches 5

In this while loop following takes place

	1) SERVER
		a) SEND QUESTION
		b) RECEIVE RESPONSE
		c) EVALUATE RESPONSE and UPDATE SCORE
		d) SEND SCORES


	2) CLIENT
		a) RECEIVE QUESTION and PRINT IT
		b) SEND RESPONSE
		c) RECIEVE SCORES
		d) PRINT SCORES


D) SCORE DISPLAY

After every questions scores are display, in the following manner

Player1   : ######
Player1   : ####
Player1   : #########

each # corresponds to 0.5 points

E) END OF GAME 

when score reaches 5 or greater than 5 ( 5.5 ) , game ends
These closes all the connections and sockets.

- - - - - - - - - - - 
COMPUTER NETWORK PROJECT 
- - - - - - - - - - - S
 


