import os
import hashlib
import msvcrt
import sys
import re
from datetime import datetime
from dateutil import tz
import threading
import time
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import sqlalchemy as sql

# Connects to database
eng= sql.create_engine('<YOUR POSTGRESQL CONNECTION LINK>', isolation_level="AUTOCOMMIT")
db = eng.connect()


# Secret keys
referralkey = "<YOUR REFERRAL KEY>"
encryptkey = b'<YOUR ENCRYPTION KEY>'
iv = b'<YOUR IV KEY>'


# Global variables
printing = False
END = False


# Setting Variables
LASTMESSAGES = 0


# Calls login or create_user
def main(msg=None):
    clear()
    banner()
    if msg != None:
        print(msg)
    while True:
        choice = input("""
Hit 1 to Login
Hit 2 to Register an account with The GroundFloor™ 
""").strip()
        if choice == "1":
            clear()
            banner()
            login()
        elif choice == "2":
            clear()
            banner()
            create_user()
        else:
            continue


# Clears terminal
def clear():
    os.system("cls||clear")


# Converts UTC to local time
def convert_time(time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime('%Y-%m-%d %H:%M:%S')


# Prints banner
def banner():
    return print("""             
                                                                                                                 
   █|█|█|  █|█|█|      █|█|    █|    █|  █|      █|  █|█|█|    █|█|█|█|  █|          █|█|      █|█|    █|█|█|    
 █|        █|    █|  █|    █|  █|    █|  █|█|    █|  █|    █|  █|        █|        █|    █|  █|    █|  █|    █|  
 █|  █|█|  █|█|█|    █|    █|  █|    █|  █|  █|  █|  █|    █|  █|█|█|    █|        █|    █|  █|    █|  █|█|█|    
 █|    █|  █|    █|  █|    █|  █|    █|  █|    █|█|  █|    █|  █|        █|        █|    █|  █|    █|  █|    █|  
   █|█|█|  █|    █|    █|█|      █|█|    █|      █|  █|█|█|    █|        █|█|█|█|    █|█|      █|█|    █|    █|  
                                                                                                                 

--------------------------------------------WELCOME TO GroundFloor™--------------------------------------------
           We are a highly secure messaging service, say goodbye to Zuckerberg stealing your data!
""", end="")


# Login
def login(msg=None):
    if msg != None:
        print(msg)
    print("""
----------------------------------------------------LOGIN------------------------------------------------------
""")
    while True:
        username = input("Username: ")
        password = input("Password: ")

        # Retrieves the user's information from the database
        user = db.execute('SELECT * FROM users WHERE username = %s', (username,)).all()[0]._asdict()

        # Checks if the user exists
        if user:
            salt = user["salt"]
            password = verify(salt, password)
            if password == user["password"]:
                clear()
                banner()
                menu(username)
            else:
                print("Invalid credentials")
                continue
        else:
            print("User does not exist")
            continue


# Register
def create_user():
    print("""
---------------------------------------------------REGISTER----------------------------------------------------
""")
    # Asks user for a referral code
    while True:
        referral = input("Referral code: ")
        if not referral == referralkey:
            print("Invalid referral code. Please try again.")
            continue
        else:
            break

    # Asks user for full name
    while True:
        fullname = input("Full name: ")
        choice = input("Is this correct? (Y/N): ").strip().upper()
        if choice == "Y":
            break
        elif choice == "N":
            continue
        else:
            msg = "Invalid input: " + choice
            clear()
            banner()
            main(msg)
    
    # Asks user for email
    while True:
        email = input("Email: ")
        if not re.match(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", email):
            print("Invalid email address. Please try again.")
            continue
        choice = input("Is this correct? (Y/N): ").strip().upper()
        if choice == "Y":
            break
        elif choice == "N":
            continue
        else:
            msg = "Invalid input: " + choice
            clear()
            banner()
            main(msg)    

    # Prompts user for new username
    while True:
        username = input("Username: ")

        # Validates username
        if not re.match("^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$", username):
            print("""
Invalid Username!
Username must follow the following criteria:
1. Username consists of alphanumeric characters (a-zA-Z0-9), lowercase, or uppercase.
2. Username allowed of the dot (.), underscore (_), and hyphen (-).
3. The dot (.), underscore (_), or hyphen (-) must not be the first or last character.
4. The dot (.), underscore (_), or hyphen (-) does not appear consecutively, e.g., java..regex
5. The number of characters must be between 5 to 20.
            """)
            continue

        # Checks if username already exists
        elif len((db.execute(f"SELECT * FROM users WHERE Username = %s", (username,))).fetchall()) == 1:
            print("Username already exists")
            continue

        break

    # Prompts user for new password
    while True:
        password = input("Password: ")
    
        # Validates password
        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,32})", password):
            print("""
Invalid Password!
Password must follow the following criteria:
1. At least one digit [0-9]
2. At least one lowercase character [a-z]
3. At least one uppercase character [A-Z]
4. At least one special character [!@#\$%\^&\*]
5. At least 8 characters in length, but no more than 32.)
            """)
            continue

        break
    
    # Prompts user for confirmation of new password
    while True:
        repassword = input("Confirm Password: ")
        if repassword == password:
            break
        else:
            print("Passwords do not match!")
            continue  
    salt, password = hashpass(password)
    updateCredentials(fullname, email, username, password, salt)
    msg = """
Thank you for registering with GroundFloor™.
Please login to continue using the application.
"""
    clear()
    banner()
    login(msg)


# Create new user in database 
def updateCredentials(fullname, email, username, password, salt):

    db.execute("INSERT INTO users (Fullname, Email, Username, Password, Salt) VALUES (%s, %s, %s, %s, %s)", fullname, email, username, password, salt)


# Creates hex of a password
def hashpass(password):

    # Generates a random salt
    salt = os.urandom(32).hex().encode()

    # Convert password to byte 
    plaintext = password.encode()

    # Hash the password
    hash = hashlib.pbkdf2_hmac('sha512', plaintext, salt, 500000)

    # Return the salt and the hashed password
    return salt.decode(), hash.hex()


# Returns hex of the inputted password
def verify(salt, password):

    # Convert password and salt to byte
    plaintext = password.encode()
    salt = salt.encode()

    # Hash the password
    hash = hashlib.pbkdf2_hmac('sha512', plaintext, salt, 500000)

    # Return the hashed password
    return hash.hex()


# Encrypts message
def encrypt(message):
    cipher = AES.new(encryptkey, AES.MODE_CTR, initial_value = iv, nonce = b'')
    bytemsg = cipher.encrypt(message.encode())
    encodedmsg = b64encode(bytemsg).decode('utf-8')
    return encodedmsg


# Decrypts message
def decrypt(message):
    cipher = AES.new(encryptkey, AES.MODE_CTR, initial_value = iv, nonce = b'')
    stored = b64decode(message)
    decodedmsg = cipher.decrypt(stored).decode('utf-8')
    return decodedmsg


# Main Menu
def menu(username, msg=None):
    if msg != None:
        print(msg)
    unreadmsg = db.execute("SELECT Sender FROM messages WHERE Receiver = %s AND Read = 0", username).fetchall()
    friendreqs = db.execute('SELECT Requests FROM users WHERE username = %s', username).fetchall()
    updatesettings(username)
    print("""
----------------------------------------------MAIN MENU--------------------------------------------------------
Hit 1 to initiate a chat
Hit 2 to manage your friends
Hit 3 to check your friend requests
Hit 4 to check unread messages
Hit 5 to open settings
Hit 6 to quit
""", end="")
    print("""
--------------------------------------------Notifications------------------------------------------------------
""", end="")
    if friendreqs[0]._asdict()["requests"] and unreadmsg:
        friendrequests = friendreqs[0]._asdict()["requests"].split(",")
        unreadmessages = set()
        for i in unreadmsg:
            unreadmessages.add(i._asdict()["sender"])
        print(f"You have {len(friendrequests)} new friend request(s) and unread messages from {len(unreadmessages)} user(s)!")
    elif friendreqs[0]._asdict()["requests"]:
        friendrequests = friendreqs[0]._asdict()["requests"].split(",")
        print(f"You have {len(friendrequests)} new friend request(s)!")
    elif unreadmsg:
        unreadmessages = set()
        for i in unreadmsg:
            unreadmessages.add(i._asdict()["sender"])
        print(f"You have new unread messages from {len(unreadmessages)} user(s)!")
    else:
        print("You have no notifications")
    while True:
        choice = input().strip()

        # Error handling for invalid input
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            clear()
            banner()
            menu(username)
            break

        # Executes the appropriate function
        else:
            choice = int(choice)
            if choice == 1:
                clear()
                banner()
                print()
                while True:

                    # Prompts user for friend's username
                    friend = input("Enter the username of the friend you want to chat with: ").strip()

                    # Non Database Error handling
                    if friend == username:
                        print("You can't chat with yourself!")
                        continue
                    elif friend == "":
                        print("Input cannot be blank!")
                        continue

                    # Database query to get the friend's data
                    verify_friend = db.execute('SELECT * FROM users WHERE Username = %s', friend).fetchall()
                    if verify_friend:
                        check = verify_friend[0]._asdict()["friends"]

                        # Cleaning up the friend's friend list
                        if check == None or check == "":
                            check = []
                        else:
                            check = check.split(",")
                            check = [i.strip() for i in check]

                        # Error handling for when the user is not in the friend's friend list
                        if username in check:
                            clear()
                            banner()
                            chat(username, friend)
                        else:
                            print("That user is not your friend.")
                            newchoice = input("Do you want to try again? (Y/N): ").strip().lower()
                            if newchoice == "y":
                                continue
                            elif newchoice == "n":
                                clear()
                                banner()
                                menu(username)
                            else:
                                msg = "Invalid choice: " + newchoice
                                clear()
                                banner()
                                menu(username, msg)
                    
                    # Error handling for when the friend is not in the database
                    else:
                        print("User does not exist")
                        newchoice = input("Do you want to try again? (Y/N) ").strip().lower()
                        if newchoice == "y":
                            continue
                        elif newchoice == "n":
                            clear()
                            banner()
                            menu(username)
                            break
                        else:
                            msg = "Invalid input: " + newchoice
                            clear()
                            banner()
                            menu(username, msg)
            elif choice == 2:
                clear()
                banner()
                manage_friends(username)
            elif choice == 3:
                clear()
                banner()
                friendreq(username)
            elif choice == 4:
                clear()
                banner()
                unread(username)
            elif choice == 5:
                clear()
                banner()
                settings(username)
            elif choice == 6:
                clear()
                banner()
                sys.exit("""
                                      Thank you for using GroundFloor™!
""")


# Gets messages for the chatroom
def getmessages(username, friend):
    global printing

    # Database query to get messages between user and friend
    while END == False:

        # Database query to get messages between user and friend
        messages = db.execute("SELECT * FROM messages WHERE (Sender = %s AND Receiver = %s AND Print = 0) OR (Sender = %s AND Receiver = %s AND Read = 0) ORDER BY Time", username, friend, friend, username).fetchall()
        

        # Print messages
        if messages:
            
            # Update print and read flag columns
            db.execute("UPDATE messages SET Read = 1 WHERE Sender = %s AND Receiver = %s", friend, username)
            db.execute("UPDATE messages SET Print = 1 WHERE Sender = %s AND Receiver = %s", username, friend)

            # Plays a sound when new messages are received
            print(end='\a')
            
            # Set printing variable to true to prevent user input and friend message from being printed on same line
            printing = True

            # Clears user's line while messages are being printed
            print('\033[2K\033[1G', flush = True, end = '')
            for message in messages:

                # Converts time to local time and prints the messages
                localtime = convert_time(message._asdict()["time"].strftime('%Y-%m-%d %H:%M:%S'))

                # Decrypts the message
                decryptmessage = decrypt(message._asdict()["message"])
                print(f"{localtime} {message._asdict()['sender']}: {decryptmessage}", flush = True)

                # To not overload the program
                time.sleep(0.01)
            
            # Set printing variable to false after messages are printed
            time.sleep(0.1)
            printing = False
        
        # Wait for 0.5 second before checking for new messages
        time.sleep(0.5)


# Main chat function
def chat(username, friend):
    global END, printing
    print("""
Hit 1 followed by your message to send a message (no spaces)
Hit 9 to return to the menu
""")
    print(f"""
--------------------------------------------Connected with {friend}--------------------------------------------
""")

    # Gets user's settings for number of messages to display initially
    num = LASTMESSAGES

    # Database queries to get messages between the two users and updating print and read flag columns
    initialmessage = db.execute(f"SELECT * FROM messages WHERE (Sender = %s AND Receiver = %s) OR (Sender = %s AND Receiver = %s) ORDER BY Time DESC LIMIT {num}", username, friend, friend, username).fetchall()
    db.execute(f"UPDATE messages SET Read = 1 WHERE Sender = %s AND Receiver = %s", friend, username)
    db.execute("UPDATE messages SET Print = 1 WHERE Sender = %s AND Receiver = %s", username, friend)
    
    # Prints messages
    if initialmessage:
        for message in initialmessage[::-1]:

            # Converts time to local time and prints the messages
            localtime = convert_time(message._asdict()["time"].strftime('%Y-%m-%d %H:%M:%S'))

            # Decrypts the message
            decryptmessage = decrypt(message._asdict()["message"])
            print(f"{localtime} {message._asdict()['sender']}: {decryptmessage}")
    
    # Set global variable for executing thread
    END = False

    # Define the thread    
    messageupdate = threading.Thread(target=getmessages, args=(username, friend), daemon=True)

    # Start thread to auto update messages
    messageupdate.start()

    # Gets user input and sends the message to the database
    while True:
        message = custominput()
        if message != "":
            if message[0] == "1":
                message = message[1:]
                if message == "":
                    print("Message can't be blank", flush = True)
                    continue

                # Encrypts the message
                message = encrypt(message)

                # Database query to insert the message
                db.execute("INSERT INTO messages (Sender, Receiver, Message) VALUES (%s, %s, %s)", username, friend, message)
            elif message == "9":

                # Set global variable for ending thread
                END = True

                # Ends the thread
                messageupdate.join()
                clear()
                banner()
                menu(username)
            else:
                msg = "Invalid input: " + message
                clear()
                banner()
                menu(username, msg)


# Shows friends of a user and allows them to add or remove friends
def manage_friends(username):
    print("""
----------------------------------------------------FRIENDS----------------------------------------------------
""")

    # Gets the user's friends from the database
    friends = db.execute('SELECT * FROM users WHERE username = %s', username).fetchall()

    # Error handling for when the user doesn't have any friends
    if friends[0]._asdict()["friends"] == None or friends[0]._asdict()["friends"] == "":
        print("You have no friends")
    
    # Printing the user's friends
    else:
        friend = friends[0]._asdict()["friends"].split(",")
        j = 1
        for i in friend:
            print(str(j) + ". " + i.strip())
            j += 1
    print("""
Hit 1 to add a friend
Hit 2 to remove a friend
Hit 9 to return to the menu
""")
    choice = input("")
    if choice == "1":
        add_friend(username)
    elif choice == "2":
        remove_friend(username)
    elif choice == "9":
        clear()
        banner()
        menu(username)
    else:
        msg = "Invalid input: " + choice
        clear()
        banner()
        menu(username, msg)


# Friend request
def add_friend(username):
    print("ADD FRIEND:")
    while True:

        # Get the friend's username
        friend = input("Enter the username of the friend you want to add: ").strip()

        # Non-database error handling
        if friend == username:
            print("You cant add yourself as a friend")
            continue
        if friend == "":
            print("You must enter a username")
            continue

        # Database requests
        frienduser = db.execute('SELECT * FROM users WHERE Username = %s', friend).fetchall()
        user = db.execute('SELECT * FROM users WHERE Username = %s', username).fetchall()

        # Making arrays from friend's data for error checks
        if frienduser:
            friendsreq = [frienduser[0]._asdict()["requests"]]
            friendscurrentfriends = [frienduser[0]._asdict()["friends"]]

            # Cleaning up the friend's requests array
            if friendsreq == [None]:
                friendsreq = []
            else:
                friendsreq = frienduser[0]._asdict()["requests"].split(",")
                friendsreq = [i.strip() for i in friendsreq]

            # Cleaning up the friend's friends array
            if friendscurrentfriends == [None]:
                friendscurrentfriends = []
            else:
                friendscurrentfriends = [i.strip() for i in friendscurrentfriends]
        
        # CMaking arrays from friend's data for error checks
        if user:
            userreq = [user[0]._asdict()['requests']]
            currentfriends = [user[0]._asdict()['friends']]

            # Cleaning up the user's requests array
            if userreq == [None]:
                userreq = []
            else:
                userreq = [i.strip() for i in userreq[0].split(",")]
            
            # Cleaning up the user's friends array
            if currentfriends == [None]:
                currentfriends = []
            else:
                currentfriends = [i.strip() for i in currentfriends[0].split(",")]
        
        # Database error handling
        if frienduser:
            
            # Error handling for sending a request to someone again
            if username in friendsreq:
                print("You have already sent a friend request to this user")
                newchoice = input("Do you want to try again? (Y/N) ").strip().lower()
                if newchoice == "y":
                    continue
                elif newchoice == "n":
                    clear()
                    manage_friends(username)
                    break
                else:
                    msg = "Invalid input: " + newchoice
                    clear()
                    banner()
                    menu(username, msg)
            
            # Error handling for sending a request to someone already friends with user
            elif username in friendscurrentfriends or friend in currentfriends:
                print("You already have this user as a friend")
                newchoice = input("Do you want to try again? (Y/N) ").strip().lower()
                if newchoice == "y":
                    continue
                elif newchoice == "n":
                    clear()
                    manage_friends(username)
                else:
                    msg = "Invalid input: " + newchoice
                    clear()
                    banner()
                    menu(username, msg)
            
            # Error handling for sending a request to someone who sent you a request
            elif friend in userreq:
                print("You have received a friend request from this user, please accept or decline the request")
                newchoice = input("Do you want to try again? (Y/N) ").strip().lower()
                if newchoice == "y":
                    continue
                elif newchoice == "n":
                    clear()
                    manage_friends(username)
                    break
                else:
                    msg = "Invalid input: " + newchoice
                    clear()
                    banner()
                    menu(username, msg)
            
            # Sending the friend request
            else:

                # Adding the user to the friend's requests array
                friendsreq.append(username)

                # Making the friend's requests array into a string
                friendlist = ""
                i = 0
                while i < len(friendsreq):
                    if i == 0:
                        friendlist += friendsreq[i]
                    else:
                        friendlist += ", " + friendsreq[i]
                    i += 1
                
                # Updating the friend's requests array in the database
                db.execute('UPDATE users SET Requests = %s WHERE Username = %s', friendlist, friend)
                print(f"You have successfully sent {friend} a friend request")

                # Prompting the user to continue
                while True:
                    newchoice = input("Do you want to add another friend? (Y/N) ").strip().lower()
                    if newchoice == "y":
                        break
                    elif newchoice == "n":
                        clear()
                        manage_friends(username)
                        break
                    else:
                        msg = "Invalid input: " + newchoice
                        clear()
                        banner()
                        menu(username, msg)
                continue
        
        # Error handling for when the friend doesn't exist
        else:
            print(f"{friend} does not exist in the database")
            choice = input("Do you want to return to the previous screen? (Y/N) ").strip().lower()
            if choice == "y":
                clear()
                manage_friends(username)
            elif choice == "n":
                continue
            else:
                msg = "Invalid input: " + choice
                clear()
                banner()
                menu(username, msg)


# Removal of a friend
def remove_friend(username):
    print("REMOVE FRIEND:")
    while True:
        friend = input("Enter the username of the friend you want to remove: ").strip()

        # Non-database error handling
        if friend == username:
            print("You cant remove yourself as a friend")
            continue
        elif friend == "":
            print("You must enter a username")
            continue

        # Database queries
        frienduser = db.execute('SELECT * FROM users WHERE Username = %s', friend).fetchall()
        user = db.execute('SELECT * FROM users WHERE Username = %s', username).fetchall()
        currentfriends = user[0]._asdict()['friends']

        # Clean up the current friends
        if currentfriends == None or currentfriends == "":
            currentfriends = []
        else:
            currentfriends = [i.strip() for i in currentfriends.split(",")]
        
        # If friend exists in database
        if frienduser:
            friendscurrentfriends = frienduser[0]._asdict()["friends"]

            # Cleaning up the friend's friends array
            if friendscurrentfriends == None or friendscurrentfriends == "":
                friendscurrentfriends = []
            else:
                friendscurrentfriends = [i.strip() for i in friendscurrentfriends.split(",")]

            # Removes the friend from the database of the user
            if username in friendscurrentfriends:
                friendscurrentfriends.remove(username)
                currentfriends.remove(friend)

                # Create a new string from the friend's and user's friends arrays
                friendsfriendlist = ""
                friendlist = ""
                i = 0
                j = 0
                if friendscurrentfriends == []:
                    friendsfriendlist = None
                else:
                    while i < len(friendscurrentfriends):
                        if i == 0:
                            friendsfriendlist += friendscurrentfriends[i]
                        else:
                            friendsfriendlist += ", " + friendscurrentfriends[i]
                        i += 1
                if currentfriends == []:
                    friendlist = None
                else:
                    while j < len(currentfriends):
                        if j == 0:
                            friendlist += currentfriends[j]
                        else:
                            friendlist += ", " + currentfriends[j]
                        j += 1

                # Update the database with new friend lists
                db.execute('UPDATE users SET Friends = %s WHERE Username = %s', friendsfriendlist, friend)
                db.execute('UPDATE users SET Friends = %s WHERE Username = %s', friendlist, username)

                # Print confirmation message
                print(f"{friend} has been removed from your friends")

                # Asks the user if they want to return to the menu
                choice = input("Do you want to return to the previous screen? (Y/N) ").strip().lower()
                if choice == "y":
                    clear()
                    manage_friends(username)
                elif choice == "n":
                    clear()
                    remove_friend(username)
                else:
                    msg = "Invalid input: " + choice
                    clear()
                    banner()
                    menu(username, msg)
        
        # Error handling for when the friend doesn't exist
        else:
            print(f"{friend} does not exist in the database")
            choice = input("Do you want to try again? (Y/N) ").strip().lower()
            if choice == "y":
                continue
            elif choice == "n":
                clear()
                manage_friends(username)
            else:
                msg = "Invalid input: " + choice
                clear()
                banner()
                menu(username, msg)       


# Handling friend requests
def friendreq(username):
    print("""
------------------------------------------------FRIEND REQUESTS------------------------------------------------
""")

    # Database query to get data on user
    requests = db.execute('SELECT * FROM users WHERE Username = %s', username).fetchall()
    friendrequests = requests[0]._asdict()["requests"]
    currentfriends = requests[0]._asdict()["friends"]

    # Cleaning up current friends
    if currentfriends == "" or currentfriends == None:
        currentfriends = []
    else:
        currentfriends = [i.strip() for i in currentfriends.split(",")]
    
    # If no requests, print message
    if friendrequests == None or friendrequests == "":
        print("No friend requests")
        while True:
            choice = input("Hit any key to return to menu\n")
            clear()
            banner()
            menu(username)
    
    # If requests, print them
    else:
        friendrequests = requests[0]._asdict()["requests"].split(",")
        friendrequests = [i.strip() for i in friendrequests]
        i = 1
        for friendrequest in friendrequests:
            print(str(i) + ". " + friendrequest, sep="")
            i += 1
    print("""
Hit 1 followed by the name of the user whose request you want to accept (no spaces)
Hit 2 followed by the name of the user whose request you want to reject (no spaces)
Hit 9 to return to the menu
    """)

    # Function to accept or reject friend requests
    while True:
        choice = input("").strip().lower()
        if choice != "":

            # Return to menu
            if choice == "9":
                clear()
                banner()
                menu(username)

            # Accepting friend request
            elif choice[0] == "1":

                # Gets the username of the friend who the user wants to accept
                choice = choice.lstrip("1")

                # Checks if the user has a friend request from the choice
                if choice in friendrequests:

                    # Adds the request into the user's friend list
                    currentfriends.append(choice)
                    
                    # Creates a string of the current friends with new friend
                    friendlist = ""
                    i = 0
                    while i < len(currentfriends):
                        if i == 0:
                            friendlist += currentfriends[i]
                        else:
                            friendlist += ", " + currentfriends[i]
                        i += 1

                    # Updates the user's friend list
                    db.execute('UPDATE users SET Friends = %s WHERE Username = %s', friendlist, username)
                    
                    # Database query to get data on friend
                    friendrequest = db.execute('SELECT * FROM users WHERE Username = %s', choice).fetchall()
                    friendscurrentfriends = friendrequest[0]._asdict()["friends"]
                    
                    # Cleans up current friends of friend
                    if friendscurrentfriends == None or friendscurrentfriends == "":
                        friendscurrentfriends = []
                    else:
                        friendscurrentfriends = [i.strip() for i in friendscurrentfriends.split(",")]

                    # Adds the user to the friend's friend list
                    friendscurrentfriends.append(username)
                    
                    # Creates a string of the current friends
                    friendlist = ""
                    i = 0
                    while i < len(friendscurrentfriends):
                        if i == 0:
                            friendlist += friendscurrentfriends[i]
                        else:
                            friendlist += ", " + friendscurrentfriends[i]
                        i += 1

                    # Updates the friend's friend list
                    db.execute('UPDATE users SET Friends = %s WHERE Username = %s', friendlist, choice)

                    # Deletes the request from the user's friend requests list
                    friendrequests.remove(choice)
                    requestlist = ""
                    i = 0
                    if friendrequests == []:
                        requestlist = None
                    else:
                        while i < len(friendrequests):
                            if i == 0:
                                requestlist += friendrequests[i]
                            else:
                                requestlist += ", " + friendrequests[i]
                            i += 1

                    # Updates the user's friend requests list
                    db.execute('UPDATE users SET Requests = %s WHERE Username = %s', requestlist, username)
                    
                    # Prints confirmation message
                    print(f"{choice} has been added to your friends!")
                    
                    # Asks if the user wants to return to the menu
                    choice = input("Do you want to return to the menu? (Y/N) ").strip().lower()
                    if choice == 'y':
                        clear()
                        banner()
                        menu(username)
                        break
                    elif choice == 'n':
                        clear()
                        friendreq(username)
                        break
                    else:
                        msg = "Invalid input: " + choice
                        clear()
                        banner()
                        menu(username, msg)
                
                # Error message if the user's choice has not sent them a request
                else:
                    print("This user has not sent you a friend request")
                    continue 

            # Rejecting friend request               
            elif choice[0] == "2":

                # Gets the username of the friend who the user wants to reject
                choice = choice.lstrip("2")

                # Checks if the user has a friend request from the choice
                if choice in friendrequests:

                    # Deletes the request from the user's friend requests list
                    friendrequests.remove(choice)

                    # Creates a string of the current friend requests
                    if friendrequests == []:
                        requestlist = None
                    else:
                        requestlist = ""
                        i = 0
                        while i < len(friendrequests):
                            if i == 0:
                                requestlist += friendrequests[i]
                            else:
                                requestlist += ", " + friendrequests[i]
                            i += 1

                    # Updates the user's friend requests list
                    db.execute('UPDATE users SET Requests = %s WHERE Username = %s', requestlist, username)
                    
                    # Prints confirmation message
                    print(f"{choice} removed from friend requests.")

                    # Asks if the user wants to return to the menu
                    choice = input("Do you want to return to the menu? (Y/N) ").strip().lower()
                    if choice == 'y':
                        clear()
                        banner()
                        menu(username)
                        break
                    elif choice == 'n':
                        clear()
                        friendreq(username)
                        break
                    else:
                        msg = "Invalid input: " + choice
                        clear()
                        banner()
                        menu(username, msg)
                
                # Error handling if the user's choice has not sent them a request
                else:
                    print("This user has not sent you a friend request")
                    continue
            
            # Error handling if the user's choice is invalid
            else:
                msg = "Invalid input: " + choice
                clear()
                banner()
                menu(username, msg)
        else:
            msg = "Invalid input: " + choice
            clear()
            banner()
            menu(username, msg)


# Get usernames of the users who sent current user a message, and allows user to intiate a chat with them
def unread(username):
    print("""
---------------------------------------------UNREAD MESSAGES FROM----------------------------------------------
""")

    # Gets the user's data from message database
    users = db.execute('SELECT * FROM messages WHERE Receiver = %s AND Read = 0', username).fetchall()

    # Error handling for when the user has not received a message
    if users:
        unreadmessages = set()
        cleanunreadmessages = []
        for i in users:
            unreadmessages.add(i._asdict()["sender"])
        j = 1
        for i in unreadmessages:
            print(str(j) + ". " + i)
            cleanunreadmessages.append(i)
            j += 1

        # Asks the user if they want to start a chat
        while True:
            choice = input("""
Hit the number of the user who sent you a message to initiate a chat with them
Hit 9 to return to the menu
""").strip().lower()
            if choice != "":
                if choice == "9":
                    clear()
                    banner()
                    menu(username)
                elif choice.isdigit():
                    if int(choice) <= len(unreadmessages):
                        clear()
                        banner()
                        chat(username, cleanunreadmessages[int(choice)-1])
                    else:
                        print("Invalid input: " + choice)
                        continue
                else:
                    print("Invalid input: " + choice)
                    continue
    else:
        print("No one sent you a message")
        input("Hit any key to return to the menu")
        clear()
        menu(username)


# Change settings
def settings(username):
    print("""
---------------------------------------------------SETTINGS----------------------------------------------------
Hit 1 to change the number of messages you see per page
Hit 9 to return to the menu
""")
    choice = input("")
    if choice == '1':

        # Prompt the user to enter 
        while True:
            try:
                num = int(input("Enter the number of messages you want to see per page: "))
                if num > 0:
                    break
                else:
                    print("Number must be greater than 0")
                    continue
            except ValueError:
                msg = "Please enter a number"
        
        # Update the user's settings
        db.execute('UPDATE users SET NumMessages = %s WHERE Username = %s', num, username)
        updatesettings(username)
        print(f"Number of messages changed to {num}")

        # Asks if the user wants to return to the menu
        choice = input("Do you want to return to the menu? (Y/N) ").strip().lower()
        if choice == 'y':
            clear()
            banner()
            menu(username)
        if choice == 'n':
            clear()
            settings(username)
        else:
            msg = "Invalid input: " + choice
            clear()
            banner()
            menu(username, msg)
    elif choice == '9':
        clear()
        banner()
        menu(username)
    else:
        msg = "Invalid input: " + choice
        clear()
        banner()
        menu(username, msg)


# Updates global variables for user settings
def updatesettings(username):
    global LASTMESSAGES
    LASTMESSAGES = db.execute('SELECT NumMessages FROM users WHERE Username = %s', username).fetchall()[0]._asdict()["nummessages"]


# SETTINGS FUNCTION - Num of messages
def nummsg(username):

    # Gets the user's settings for the number of messages they want to see per page
    num = db.execute('SELECT NumMessages FROM users WHERE Username = %s', username).fetchall()
    num = num[0]._asdict()["nummessages"]
    return int(num)


# Custom input for chat function that does not block execution (standard input function blocks execution of block)
def custominput():

    # Empty string to be returned
    string = ""

    # Temprary string made for checking if the user has inputted anything new
    old_string = ""

    # Default value of check is false
    check = False

    # While thread is running
    while END == False:

        # If the user is not receiving any message
        if printing == False:

            # Making this check since input is no longer blocking, if check was ignored then the string will be cleared and reprinted every 0.000001 seconds
            # Checking if user inputted something new or check variable is flagged
            if string != old_string or check == True:
                
                # Brings check to default value
                check = False

                # Clears line the input otherwise it would clear the message the user is receiving
                print('\033[2K\033[1G', flush = True, end = '')

                # Prints user input on the new line
                print(string, flush = True, end = '')

                # Updates the string to be returned
                old_string = string
        
        # If the user is receiving a message from friend, flag the check variable
        else:
            check = True

        # Non blocking input
        if msvcrt.kbhit():
            key = msvcrt.getch()
        
        # To not overload the while loop
        else:
            time.sleep(0.0000001)
            continue

        # Checks if key pressed is enter
        if key == b'\r':

            # Only clears line if the user is not receiving message, otherwise the received message is also cleared
            if printing == False:

                # Clears line if printing is false, because when it is true, the user input is cleared by getmessage function
                print('\033[2K\033[1G', flush = True, end = '')

            # Returns the string
            return string

        # Checks if key pressed is backspace
        elif key == b'\x08':

            # Last character of string is cleared
            string = string[:len(string)-1]
            continue

        elif key == b'\xe0' or key == b'\x00':
            msvcrt.getch()
            continue

        # Error handling ctrl + char inputs
        elif not (ord(key) > 0x1f and ord(key) != 0x7f and not (0x80 <= ord(key) <= 0x9f)):
            continue

        # Error handling for special characters
        try:
            key.decode()
        except:
            continue
        string += key.decode()
        

if __name__ == "__main__":
    main()
