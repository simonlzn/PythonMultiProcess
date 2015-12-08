import message_itk2rabbitmq
import sender
import volume_reconstruction_3D
import volume_slicing_3D
import sys

class Pipeline():
    def __init__(self):
        self.__errors_sign = False
    
    
    def set_data_key(self,data_key):
        self.__data_key = data_key
        
    def set_process_id(self,process_id):
        self.__process_id = process_id
        
    def set_data(self,data):
        self.__data = data
        
    def __send_message(self):
        message = message_itk2rabbitmq.Message_ITK2RabbitMQ()
        message.add_key(str(self.__data_key))
        message.occur_errors(self.__errors_sign)
        message.add_info(self.__info)
        
        message_sender = sender.Sender()
        message_sender.send(message.create_message())
        
    def execute(self):
        print("start execute")
        sys.stdout.flush()
        
        if self.__data["func"] == "reconstruct":
            print("reconstruct")
            
            volume_reconstruction_3D_filter = volume_reconstruction_3D.Volume_Reconstruction_3D()
            volume_reconstruction_3D_filter.set_folder_path(str(self.__data["folderPath"]))
            volume_reconstruction_3D_filter.update()
            
            self.__volume = volume_reconstruction_3D_filter.get_volume()
            self.__info = volume_reconstruction_3D_filter.get_info()
            
            self.__send_message()
            
            self.__info = ""
            
            
        elif self.__data["func"] == "slicing":
            print("slicing")
            sys.stdout.flush()
            
            volume_coord = str(self.__data["views"])
            volume_coord_transverse, volume_coord_coronal, volume_coord_sagittal = volume_coord.split(',')
            volume_coord = (int(volume_coord_transverse),int(volume_coord_coronal),int(volume_coord_sagittal))
            
            print(volume_coord)
            sys.stdout.flush()
            
            volume_slicing_3D_filter = volume_slicing_3D.Volume_Slicing_3D()
            volume_slicing_3D_filter.set_volume_coord(volume_coord)
            volume_slicing_3D_filter.set_volume(self.__volume)
            volume_slicing_3D_filter.update()
            
            slicing_info = volume_slicing_3D_filter.get_info()
            
            self.__info = slicing_info
            self.__send_message()
            
            print("slicing done")
            sys.stdout.flush()
    