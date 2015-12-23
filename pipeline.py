import message_itk2rabbitmq
import sender
import os

from timps.func import volume_reconstruction_3D
from timps.func import volume_slicing_3D
from timps.func import structure_volume_reconstruction_3D
#from timps.func import region_growing_segmentation_3D

from timps.util import volume_base

import sys
import itk

class Pipeline():
    def __init__(self):
        self.__vol = None
      
    def set_data_key(self,data_key):
        self.__data_key = data_key
        
    def set_process_id(self,process_id):
        self.__process_id = process_id
        
    def set_data(self,data):
        self.__data = data
        
    def __send_message(self,error_sign,info):
        message = message_itk2rabbitmq.Message_ITK2RabbitMQ()
        message.add_key(str(self.__data_key))
        message.occur_errors(error_sign)
        message.add_info(info)
        
        message_sender = sender.Sender()
        message_sender.send(message.create_message())
        
    def execute(self):
        print("start execute")
        print(self.__data)
        sys.stdout.flush()
        
        # reconstruct 3D volume
        if self.__data["func"] == "reconstruct":
            print("reconstruct")
            
            folder_path = str(self.__data["folderPath"])
            
            if os.path.exists(folder_path) == False:
                info = "Error: DICOM series folder not find!"
                error_sign = True
                self.__send_message(error_sign,info)
                return
            else:
                volume_reconstruction_3D_filter = volume_reconstruction_3D.Volume_Reconstruction_3D()
                volume_reconstruction_3D_filter.set_folder_path(folder_path)
                volume_reconstruction_3D_filter.execute()
                
                # send message
                info = volume_reconstruction_3D_filter.get_info()
                error_sign = volume_reconstruction_3D_filter.get_error_sign()
                self.__send_message(error_sign,info)
                
                if error_sign == False:
                    self.__vol = volume_reconstruction_3D_filter.get_volume()
                    
                    # write DICOM (3D volume)
                    writer = itk.ImageFileWriter[itk.Image.SS3].New()
                    writer.SetFileName("data/volume.nrrd")
                    writer.SetInput(volume_reconstruction_3D_filter.get_volume())
                    writer.Update()
                
                print("reconstruct done")
                sys.stdout.flush()
            
        # slicing 3D volume
        elif self.__data["func"] == "slicing":
            print("slicing")
            sys.stdout.flush()
            
            volume_coord = str(self.__data["views"])
            volume_coord_transverse, volume_coord_coronal, volume_coord_sagittal = volume_coord.split(',')
            volume_coord = (int(volume_coord_transverse),int(volume_coord_coronal),int(volume_coord_sagittal))
            
            if self.__vol == None:
                # read DICOM (3D volume)
                reader = itk.ImageFileReader[itk.Image.SS3].New()
                reader.SetFileName("data/volume.nrrd")
                try:
                    reader.Update()
                except Exception as err:
                    info = str(err)
                    error_sign = True
                    self.__send_message(error_sign, info)
                    return
                self.__vol = reader.GetOutput()
            
            volume_slicing_3D_filter = volume_slicing_3D.Volume_Slicing_3D()
            volume_slicing_3D_filter.set_volume_coord(volume_coord)
            volume_slicing_3D_filter.set_volume(self.__vol)
            volume_slicing_3D_filter.execute()
            
            info = volume_slicing_3D_filter.get_info()
            error_sign = volume_slicing_3D_filter.get_error_sign()
            self.__send_message(error_sign,info)
            
            print("slicing done")
            sys.stdout.flush()
        
        # reconstruct 3D structure volume
        elif self.__data["func"] == "reconstruct_structure":
            print("reconstruct structure")
            sys.stdout.flush()
            
            structure_id = int(self.__data["structure_id"])
            structure_coords = self.__data["coord"]
            
            if os.path.isfile("data/structure.nrrd"):
                # read DICOM (3D structure volume)
                reader = itk.ImageFileReader[itk.Image.SS3].New()
                reader.SetFileName("data/structure.nrrd")
                try:
                    reader.Update()
                except Exception as err:
                    info = str(err)
                    error_sign = True
                    self.__send_message(error_sign, info)
                    return
                structure_vol = reader.GetOutput()
            else:
                if self.__vol == None:
                    if os.path.exists('data/volume.nrrd'):
                        # read DICOM (3D volume)
                        reader = itk.ImageFileReader[itk.Image.SS3].New()
                        reader.SetFileName("data/volume.nrrd")
                        try:
                            reader.Update()
                        except Exception as err:
                            info = str(err)
                            error_sign = True
                            self.__send_message(error_sign, info)
                            return
                        self.__vol = reader.GetOutput()
                    else:
                        info = "Error: reconstruct volume first!"
                        error_sign = True
                        self.__send_message(error_sign, info)
                        return
                
                vol_base = volume_base.Volume_Base()
                structure_vol = vol_base.copy_volume(self.__vol, itk.UC)
            
            structure_volume_reconstruction_3D_filter = structure_volume_reconstruction_3D.Structure_Volume_Reconstruction_3D()
            structure_volume_reconstruction_3D_filter.set_structure_volume(structure_vol)
            structure_volume_reconstruction_3D_filter.set_structure_index(structure_id)
            structure_volume_reconstruction_3D_filter.set_structure_coordinates(structure_coords)
            structure_volume_reconstruction_3D_filter.execute()
            
            # send message
            info = structure_volume_reconstruction_3D_filter.get_info()
            error_sign = structure_volume_reconstruction_3D_filter.get_error_sign()
            self.__send_message(error_sign, info)        
                
            # write DICOM (3D structure volume)
            if error_sign == False:
                writer = itk.ImageFileWriter[itk.Image.UC3].New()
                writer.SetFileName("data/structure.nrrd")
                writer.SetInput(structure_volume_reconstruction_3D_filter.get_structure_volume())
                writer.Update()
            
            print("reconstruct structure done")
            sys.stdout.flush()
        
        # slicing 3D structure volume
        elif self.__data["func"] == "slicing_strucutre":
            print("slicing structure")
            sys.stdout.flush()
            
            
            
            print("slicing structure done")
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