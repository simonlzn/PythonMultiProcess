import message_itk2rabbitmq
import sender

from timps.func import volume_reconstruction_3D
from timps.func import volume_slicing_3D
from timps.func import structure_volume_reconstruction_3D
#from timps.func import region_growing_segmentation_3D

import sys
import itk

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
        
        # reconstruct 3D volume
        if self.__data["func"] == "reconstruct":
            print("reconstruct")
            
            volume_reconstruction_3D_filter = volume_reconstruction_3D.Volume_Reconstruction_3D()
            volume_reconstruction_3D_filter.set_folder_path(str(self.__data["folderPath"]))
            volume_reconstruction_3D_filter.execute()
            
            # write DICOM (3D volume)
            writer = itk.ImageFileWriter[itk.Image.SS3].New()
            writer.SetFileName("./volume.dcm")
            writer.SetInput(volume_reconstruction_3D_filter.get_volume())
            writer.Update()
            
            # write DICOM (structure volume)
            writer = itk.ImageFileWriter[itk.Image.UC3].New()
            writer.SetFileName("./structure.dcm")
            writer.SetInput(volume_reconstruction_3D_filter.get_structure_volume())
            writer.Update()
            
            # send message
            self.__info = volume_reconstruction_3D_filter.get_info()
            self.__send_message()
            
            print("reconstruct done")
            sys.stdout.flush()
            
        # slicing 3D volume
        elif self.__data["func"] == "slicing":
            print("slicing")
            sys.stdout.flush()
            
            volume_coord = str(self.__data["views"])
            volume_coord_transverse, volume_coord_coronal, volume_coord_sagittal = volume_coord.split(',')
            volume_coord = (int(volume_coord_transverse),int(volume_coord_coronal),int(volume_coord_sagittal))
            
            # read DICOM (3D volume)
            reader = itk.ImageFileReader[itk.Image.SS3].New()
            reader.SetFileName("./volume.dcm")
            reader.Update()
            
            volume_slicing_3D_filter = volume_slicing_3D.Volume_Slicing_3D()
            volume_slicing_3D_filter.set_volume_coord(volume_coord)
            volume_slicing_3D_filter.set_volume(reader.GetOutput())
            volume_slicing_3D_filter.execute()
            
            self.__info = volume_slicing_3D_filter.get_info()
            self.__send_message()
            
            print("slicing done")
            sys.stdout.flush()
            
        # reconstruct 3D structure volume
        elif self.__data["func"] == "reconstruct_structure":
            print("reconstruct structure")
            sys.stdout.flush()
            
            structure_id = int(self.__data["structure_id"])
            structure_coords = self.__data["data"]
            
            # read DICOM (3D structure volume)
            reader = itk.ImageFileReader[itk.Image.SS3].New()
            reader.SetFileName("./structure.dcm")
            reader.Update()
            
            structure_volume_reconstruction_3D_filter = structure_volume_reconstruction_3D.Structure_Volume_Reconstruction_3D()
            structure_volume_reconstruction_3D_filter.set_structure_volume(reader.GetOutput())
            structure_volume_reconstruction_3D_filter.set_structure_index(structure_id)
            structure_volume_reconstruction_3D_filter.set_structure_coordinates(structure_coords)
            structure_volume_reconstruction_3D_filter.execute()
            
            # write DICOM (3D structure volume)
            writer = itk.ImageFileWriter[itk.Image.UC3].New()
            writer.SetFileName("./structure.dcm")
            writer.SetInput(structure_volume_reconstruction_3D_filter.get_structure_volume())
            writer.Update()
            
            # send message
            self.__info = structure_volume_reconstruction_3D_filter.get_info()
            self.__send_message()
        
            print("reconstruct structure done")
            sys.stdout.flush()
        
        '''
        # region growing segmentation
        elif self.__data["func"] == "region_growing":
            print("region growing segmentation")
            sys.stdout.flush()
            
            seed_coord = str(self.__data["seed"])
            seed_coord_transverse, seed_coord_coronal, seed_coord_sagittal = seed_coord.split(',')
            
            region_growing_segmentation_3D_filter = region_growing_segmentation_3D.Region_Growing_Segmentation_3D()
            region_growing_segmentation_3D_filter.set_volume(self.__volume)
            region_growing_segmentation_3D_filter.set_seed((int(seed_coord_transverse),int(seed_coord_coronal),int(seed_coord_sagittal)))
            region_growing_segmentation_3D_filter.set_threshold((-1000,-200))
            region_growing_segmentation_3D_filter.execute()
            
            # writer
            writer = itk.ImageFileWriter[itk.Image.UC3].New()
            writer.SetFileName('/home/zshen/workspace/contour.dcm')
            writer.SetInput(region_growing_segmentation_3D_filter.get_contoured_volume())
            writer.Update()
            
            print("region growing segmentation done")
            sys.stdout.flush()
        '''