# Server Program

# # # # # MODULES # # # # #

from socket import *
import pickle
import random
import time

# # # # # # # # # #

# # # # # LOADING QUESTIONS # # # # #


questions = []
file = open("questions.txt", "r")
for x in file:
    question_set = x.split("::")
    questions.append(question_set)
print(questions)


# # # # # CONNECTION # # # # #


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(2)

# # # # # # # # # #

# # # # # GLOBALS # # # # #


players_connections = []  # connection object, address
players_details = []  # name, score


# # # # # # # # # #


# # # # # FUNCTIONS # # # # #


# ---> decode
def dc(string):  # DECODE
    return string.decode("utf-8")


# ---> encode
def ec(string):  # ENCODE
    return bytes(string, "utf-8")


# ---> send string to every client
def send_all_text(text):
    msg = ec(text)
    for i in players_connections:
        i[0].send(msg)


# ---> send object to every client
def send_all_objects(obj):
    msg = pickle.dumps(obj)
    # print("OBJECT SEND")
    for i in players_connections:
        i[0].send(msg)


# ---> send question to all clients
def send_question():
    # print("SEND QUESTION")
    question = random.choice(questions)
    send_all_objects(question)
    correct_option = question[2]
    questions.remove(question)
    # print("QUESTION SENT")
    print(question)
    return correct_option


# # # # # # # # # #

# # # # # INITIAL MESSAGE # # # # #


while len(players_connections) < 1:
    conn, addr = serverSocket.accept()
    name = dc(conn.recv(2048))
    players_connections.append([conn, addr])
    players_details.append([name, 0])

send_all_text("ALL PLAYERS ARE READY\n")
send_all_objects(players_details)


# # # # # # # # # #

while True:
    # ---> Check condition
    scores = [d[1] for d in players_details]
    if max(scores) < 5:
        time.sleep(5)

        # ---> send question
        answer = []
        j = send_question()

        # ---> receive clients response
        a = 0
        while len(answer) < len(players_connections):
            ans = pickle.loads(players_connections[a][0].recv(1024))
            answer.append(ans)
            a += 1

        # ---> print details
        timez = [t[0] for t in answer]
        print(answer)
        print(j)
        # ---> Update scores
        i = timez.index(min(timez))
        if str(answer[i][1]) == str(int(j)):
            players_details[i][1] += 1
        elif int(answer[i][1] == 0):
            players_details[i][1] += 0
        else:
            players_details[i][1] -= 0.5
        print(players_details)
        print(i, str(j), str(answer[i][1]))
        # ---> send scores
        send_all_objects(players_details)

    # ---> End condition
    else:
        for i in players_connections:
            i[0].close()
        break

# ---> Server closes
serverSocket.close()
# END OF SCRIPT #

# Use option/alt + shift + f for fomating the text script

