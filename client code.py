#client code

#importing needed library
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

#Handles receiving of messages
def receive():
        while True:
                try:
                                                   
                        msg = client_socket.recv(BUFSIZ).decode("utf8")
                        msg_list.insert(tkinter.END, msg)   #add msg to the end of msg_list
                except OSError:  # Possibly client has left the chat
                        break

#Handles sending of messages
def send(event=None):  # event is passed by binders.
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        if msg == "shutdown":
                client_socket.close()
                top.destroy()

#this function is to be called when the window is closed
def on_closing(event=None):
        top.destroy()

top = tkinter.Tk() #define new tkinter object
top.title("Chatter") #give title to the window
top.geometry('600x400') # define shape of window

messages_frame = tkinter.Frame(top) # define message frame object
my_msg = tkinter.StringVar()  # For the messages to be sent
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
#define messages listbox object
msg_list = tkinter.Listbox(messages_frame, height=15, width=60, yscrollcommand=scrollbar.set) 
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # add scrollbar to object
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH) # add place of messages to object 
msg_list.pack()  # add msg_list to the window
messages_frame.pack()  # add message frame to window

#define entry field object link to window and set variable
entry_field = tkinter.Entry(top, textvariable=my_msg) 
entry_field.bind("<Return>", send)  # define that the entry field change call send() function
entry_field.pack()    # add entry field to window
#define button with name send and command send()
send_button = tkinter.Button(top, text="Send", command=send) 
send_button.pack()   #add button to window
#define what happen when user close window it is call on_closing() function
top.protocol("WM_DELETE_WINDOW", on_closing) 

#sockets part
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
        PORT = 33000
else:
        PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)  #define Thread object and set target
receive_thread.start() # start thread excution
tkinter.mainloop()  # Starts GUI execution as infinite loop
