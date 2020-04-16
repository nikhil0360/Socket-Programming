# Client Program

# # # # # MODULES # # # # #

from socket import *
import pickle
import time
import sys
from threading import Thread

# # # # # # # # # #


# # # # # CONSTANTS # # # # #

# ---> for function delete_last_lines()
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

# ---> Socket Connection
serverName = 'localhost'
serverPort = 12000

# # # # # # # # # #


# # # # # GLOBALS # # # # #

question_count = [0]
status = [1]
response = []
t = []

# # # # # # # # # #

# # # # # CONNECTION # # # # #

# ---> TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# # # # #


# # # # # FUNCTIONS # # # # #

# ---> decode
def dc(string):
    return string.decode("utf-8")


# ---> encode
def ec(string):
    return bytes(string, "utf-8")


# ---> print scores ( list of [name,score] )
def print_score(data_list):
    for i in data_list:
        string = f'{i[0]:<{10}}'  # left shifts, proper alignment
        print(string + ": " + "#" * int(i[1] * 2))

    s = [d[1] for d in data_list]
    if max(s) >= 5:
        status[0] = 0
        i = s.index(max(s))
        print("\nGAME OVER \n%s WON THE GAME\n" % (data_list[i][0]))
        clientSocket.close()


# ---> Prints a progress bar
def progress_bar(seconds):
    for i in range(seconds):
        print("# " * (i + 1) + "%d" % (i + 1))
        time.sleep(1)
        if i + 1 < seconds:
            delete_last_lines()


# ---> deletes the last line in terminal
def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def buzzer():
    answer = None
    del t[:]

    # ---> buzzer
    def check():
        time.sleep(10)
        if answer is None:
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            print("PRESS ENTER TO CONTINUE")
            msg = [1000, 0]
            response.append(msg)
            return

        elif answer == '':
            buzzer_time = (t[1] - t[0]) / 1000000000
            print("YOU PRESSED BUZZER IN %f" % buzzer_time)
            t.append(time.time_ns())
            opt = input("ENTER CORRECT OPTION: ")
            t.append(time.time_ns())
            time_taken = (t[3] - t[2]) / 1000000000
            if time_taken <= 10:
                msg = [buzzer_time, opt]
                response.append(msg)
                return

            else:
                print("YOU TOOK MORE THAN 10 Seconds")
                msg = [time_taken, '0']
                response.append(msg)
                return

    Thread(target=check).start()
    t.append(time.time_ns())
    print("PRESS BUZZER")
    answer = input()
    t.append(time.time_ns())


# ---> print questions,options which are in format (questions::options::answer)
def print_question(question_set):
    print("\n%d) %s\n" % (question_count[0] + 1, question_set[0]))
    options = question_set[1].split(";")
    for i in range(len(options)):
        print("  %d) %s" % (i + 1, options[i]))
    question_count[0] += 1


# # # # # # # # # #

# # # # # MAIN # # # # #


# # # # # INITIAL MESSAGE # # # # #

print("\nHELLO THERE, I AM QUIZ HOST CORONA")
print("THESE ARE THE RULES OF THE GAME :")
print("  YOU WILL HAVE 10 SECONDS TO PRESS THE BUZZER ---> PRESS ENTER")
print("  YOU WILL HAVE 10 SECONDS TO CHOOSE YOUR OPTION  ---> PRESS ENTER TO SUBMIT")
print("  +1 FOR CORRECT ANSWER || -0.5 FOR WRONG ANSWER")
print("\nHAPPY QUIZ-ING")

name = input("ENTER YOUR NAME: ")
clientSocket.send(ec(name))
print(f"\nHello {name}, please wait while other players are connecting ...")

message = dc(clientSocket.recv(1024))
print(message)

data = pickle.loads(clientSocket.recv(1024))
print_score(data)

print("STARTING GAME IN : ")
progress_bar(5)

# # # # # # # # # #

# # # # # RECEIVE QUESTION, PRINT QUESTIONS, SEND, RECEIVE SCORES, PRINT SCORES # # # # #
while status[0]:

    del response[:]
    # ---> print questions
    print_question(pickle.loads(clientSocket.recv(1024)))
    buzzer()

    # ---> waiting for the buzzer function
    while len(response) < 1:
        pass

    # ---> send response
    msg = pickle.dumps(response[0])
    clientSocket.send(msg)

    # ---> get scores
    data = pickle.loads(clientSocket.recv(1024))

    # ---> print scores
    print_score(data)

# END OF SCRIPT #
