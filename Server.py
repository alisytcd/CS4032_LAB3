import socket
import sys,os
from threading import Thread
from SocketServer import ThreadingMixIn
from chatroom import Chatroom

data=""
kill=0
leave=0
chat_room1=Chatroom("room1",1)
chat_room2=Chatroom("room2",2)
rooms = []
rooms.append(chat_room1)
rooms.append(chat_room2)

TCP_IP = '0.0.0.0'
TCP_PORT = 8000
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
tcpServer.listen(10)
alive = True
t_lim = 150
num_threads=0
threads=[]

#class ClientThread(Thread):
def communication(conn):

#        def __init__(self,ip,port):
#            Thread.__init__(self)
#            self.ip = ip
#            self.port = port
#            print "[+] New server socket thread started for " + ip + ":" + str(port)

#        def run(self):
     while alive == True:
         print "looping around"

         global data
         global TCP_PORT
         global kill
         global leave
         data=""

         data = conn.recv(2048)

         print data
         if data[:5] == "LEAVE":
             print "leave enabled"
             leave = 1
         if data[:12] == "KILL_SERVICE":
             print "Server received data:", data

             kill=1
             os._exit(1)
             sys.exit
             break
         elif data[:4] == "HELO":
             print "Server received data:", data
             MESSAGE = data+"IP:"+str(socket.gethostbyname(socket.gethostname()))+"\nPort:"+str(TCP_PORT)+"\nStudentID:13323690\n"
             conn.sendall(MESSAGE)

         elif data[:13] == "JOIN_CHATROOM":
             print "Server received data:\n",data
             chatroom_name=""
             column=":"
             data_array=data.splitlines()
             join_part = data_array[0]
             i=join_part.find(column)
            #print "index is "+str(i)
             i=i+2
            #print "new index is "+str(i)

             while i<len(join_part):
                 chatroom_name=chatroom_name+join_part[i]
                 i=i+1
             print "Chatroom name is: "+chatroom_name
             print "Joining chatroom..."

             for x in rooms:
                 if(chatroom_name==x.name):

                     client_name=""
                     c_name=data_array[3]
                     i=c_name.find(column)
                     i=i+2
                     while i < len(c_name):
                         client_name=client_name+c_name[i]
                         i=i+1

                    #Checking if the client handle already exists in the chatroom..if it does,then we don't add the client
                    #for c in x.clients:
                        #   if(c[0]==client_name and c[3] == x.refNum):
                        #       print"ERROR! Client handle already exists." 
                         #      break

                                #else:       
                     x.addClient(client_name,conn,x.refNum)

                     MESSAGE = "JOINED_CHATROOM: "+x.name+"\nSERVER_IP: "+str(socket.gethostbyname(socket.gethostname()))+"\nPORT: "+str(TCP_PORT)+"\nROOM_REF: "+str(x.refNum)+"\nJOIN_ID:"+str(x.joinID)+"\n"
                     conn.sendall(MESSAGE)

                     print "Printing clients"
                    #print x.clients
                     for c in x.clients:
                         print c

                     MESSAGE ="CHAT: "+str(x.refNum)+"\nCLIENT_NAME: "+client_name+"\nMESSAGE: "+client_name +"has joined the room\n"
                     conn.sendall(MESSAGE)
                     x.echo(MESSAGE,conn,x.refNum)
                               #x.addClient(client_name,conn)
                    # conn.send(MESSAGE)
                    # break

                 #else:
                    # print "Error! Chat room doesn't exist"
               # elif data[:14]=="LEAVE_CHATROOM":
         elif leave == 1:
             print "Server received Data :\n",data
             data_array=data.splitlines()
             refPart = data_array[0]
             column=":"
             ref=""
             i = refPart.find(column)
             i=i+2
             while i<len(refPart):
                 ref=ref+refPart[i]
                 i=i+1
             ref=int(ref)
             print "REF TO REMOVE IS "+str(ref)

             id_Part = data_array[1]
             j_ID = ""
             i = id_Part.find(column)
             i=i+2
             while i<len(id_Part):
                 j_ID=j_ID+id_Part[i]
                 i=i+1
             j_ID=int(j_ID)
             print "JOIN ID TO REMOVE IS "+str(j_ID)

             client_name=""
             c_name=data_array[2]
             i=c_name.find(column)
             i=i+2
             while i < len(c_name):
                 client_name=client_name+c_name[i]
                 i=i+1
             print "CLIENT NAME TO REMOVE IS "+client_name
             for x in rooms:
                 MESSAGE ="LEFT_CHATROOM: "+str(x.refNum)+"\nJOIN_ID: "+str(j_ID)+"\n"
                 if(ref==x.refNum):
                     MESSAGE_1="CHAT: "+str(x.refNum)+"\nCLIENT_NAME: "+client_name+"\nMESSAGE: "+client_name+"has left the chat\n"
                     conn.sendall(MESSAGE)
                     x.removeClient(client_name,j_ID,ref)
                     for c in x.clients:
                         print c
                     x.echo(MESSAGE_1,conn,x.refNum)
                     #print x.clients
                     #for c in x.clients:
                         #   if(c[0]==c_name and c[1]==j_ID):
                        #      x.removeClient(c_name,j_ID)
            # MESSAGE ="LEFT_CHATROOM: "+str(x.refNum)+"\nJOIN_ID: "+str(j_ID)+"\n"
                   # conn.send(MESSAGE)
                   # MESSAGE = "CHAT: "+str(x.refNum)+"\nCLIENT_NAME:"+client_name+"\nMESSAGE: "+client_name+"has left the chat\n"
                   # conn.send(MESSAGE)

         elif data[:4]=="CHAT":
             print "inside Chat"
             data_array=data.splitlines()
             refPart = data_array[0]
             column=":"
             ref=""
             i = refPart.find(column)
             i=i+2
             while i<len(refPart):
                 ref=ref+refPart[i]
                 i=i+1
             ref=int(ref)

             id_Part = data_array[1]
             j_ID = ""
             i = id_Part.find(column)
             i=i+2
             while i<len(id_Part):
                 j_ID=j_ID+id_Part[i]
                 i=i+1
             j_ID=int(j_ID)

             client_name=""
             c_name=data_array[2]
             i=c_name.find(column)
             i=i+2
             while i < len(c_name):
                 client_name=client_name+c_name[i]
                 i=i+1

             message=""
             msg_part=data_array[3]
             i=msg_part.find(column)
             i=i+2
             while i < len(msg_part):
                 message = message+msg_part[i]
                 i=i+1
             for x in rooms:
                 if(ref==x.refNum):
                     new_message= "CHAT:"+str(ref)+"\nCLIENT_NAME:"+client_name+"\nMESSAGE:"+message

                    #new_message=client_name+ "sent the message: "+message
                     conn.sendall(new_message)
                     x.echo(new_message,conn,x.refNum)


           # else:
             #   print "THIS IS SPARTA"
            #    print "Server received data:", data

# Initialising server
#TCP_IP = '0.0.0.0'
#TCP_PORT = 8000
#BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 

#tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#tcpServer.bind((TCP_IP, TCP_PORT))
#threads = []

#while data[:12]!="KILL_SERVICE" :
#while kill!=1:
#    tcpServer.listen(10)
#    print "Multithreaded Python server : Waiting for connections from TCP clients..."
#    (conn, (ip,port)) = tcpServer.accept()
#    newthread = ClientThread(ip,port)
#    newthread.start()
#    threads.append(newthread)

#print "out of while loop"
#for t in threads:
#    t.join()
#    tcpServer.close()
while alive:
    if num_threads<t_lim:
        conn,address=tcpServer.accept()
        threads.append(Thread(target=communication,args=(conn,)))
        threads[num_threads].start()
        global num_threads
        num_threads = num_threads+1
    else:
        print "maximum number of threads has been reached"
                                                                                                                                                                                              252,1         Bot

                  
