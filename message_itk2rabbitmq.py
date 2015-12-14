

class Message_ITK2RabbitMQ():
    def __init__(self):
        self.__key = ""
        self.__status = ""
        self.__info = ""
        
    def add_key(self,key_str):
        self.__key = key_str
        
    def occur_errors(self,sign):
        if sign == True:
            self.__status = "Failure"
        else:
            self.__status = "Success"
        
    def add_info(self,info_str):
        self.__info = info_str
        
    def create_message(self):
        #message_str = "{\"key\":\""+self.__key+"\",\"status\":\""+self.__status+"\",\"info\":\"{"+self.__info+"}\"}"  
        message_str = "{\"key\":\""+self.__key+"\",\"status\":\""+self.__status+"\",\"info\":\"["+self.__info+"]\"}"        
            
        print(message_str)
        return message_str