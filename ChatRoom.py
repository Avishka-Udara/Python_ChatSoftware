from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


"""
The below function gets the latest messages from the server and inserts it into the Listbox object.
If the window has somehow been closed abruptly, we remove the user.
"""
def receive():
    stop = False
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE).decode('utf8')
            msgList.insert(tkinter.END,msg)
        except OSError:
            cleanAndClose()
            break

"""
The below function sends the messages of the user to the server to be broadcast, 
if the exit sequence is entered, user's data is purged, and the window is closed.
"""
def send(event=None):
    msg = myMsg.get()
    myMsg.set("")
    clientSocket.send(bytes(msg,'utf8'))
    if msg == "exit":
        clientSocket.close()
        cleanAndClose()
        top.quit()

"""
If the exit sequence is entered, this function is executed.
"""
def cleanAndClose(event=None):
    myMsg.set("'exit'")
    send()
    top.destroy()
    stop = True

if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('ChatRoom')
    top.configure(bg='#ddffe7')
    messageFrame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messageFrame)

    msgList = tkinter.Listbox(messageFrame, width = 60, height= 25,  yscrollcommand = scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msgList.pack(fill = tkinter.X)
    msgList.configure(bg='#ddffe7')
    messageFrame.pack()

    myMsg = tkinter.StringVar()
    #myMsg.set("Click to type")
    entryField = tkinter.Entry(top,textvariable = myMsg)
    entryField.bind("<Return>", send)
    entryField.pack(ipadx=120, ipady=15, padx=10, pady=10)
    entryField.configure(bg='#98d7c2')

    sendButton = tkinter.Button(top, text = 'Send', command = send)
    sendButton.pack(ipadx=100, ipady=5, pady=(0, 20))
    sendButton.configure(bg='#167d7f')

    top.protocol("WM_DELETE_WINDOW", cleanAndClose)

    #HOST = input('Enter HOST IP Address: ')
    #PORT = input('Enter PORT number: ')
    HOST = '127.0.0.1'
    PORT = 5545
    PORT = 5545 if not PORT else int(PORT)

    BUFFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(ADDR)

    receiveThread = Thread(target=receive)
    receiveThread.start()
    tkinter.mainloop()  
    receiveThread.join()
