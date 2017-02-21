#clients=[]
#joinID=0



class Chatroom:

    clients=[]
    joinID=0
    def echo(self, message,conn,roomref):
        for x in self.clients:
            if x[3] == roomref:
                x[2].sendall(message)

    joinID=joinID
    clients=clients
    def __init__(self,name,refNum):
        self.refNum=refNum
        self.name=name

    def addClient(self,clientName,conn,roomref):


        self.joinID=self.joinID+1
        self.clients.append((clientName,self.joinID,conn,roomref))

    def removeClient(self,clientName,joinID,ref):
        for x in self.clients:
            if(x[0] == clientName):
                print "CLIENTNAME MATCH"
                if ( x[1]==joinID):
                    print "JOINID MATCH"
                    if(x[3]==ref):
                        print"REF MATCH"

                        self.clients.remove(x)
            else:
                print "COULD NOT REMOVE CLIENT"

        #self.clients.remove(clientName,joinID)
    def printClients(self):
        print self.clients
    def sendMessage(self,message,conn):
        echo(message,conn)



    #clients=[]     
    #client_ID=0    
