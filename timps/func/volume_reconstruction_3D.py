import itk

from timps.comm import dicom_2D_series

class Volume_Reconstruction_3D():
    def __init__(self):
        self.__error_sign = False
        self.__folder_path = ""
    
    def set_folder_path(self,folder_path):
        self.__folder_path = folder_path
        
    def get_info(self):
        return self.__info
    
    def get_error_sign(self):
        return self.__error_sign
    
    def get_volume(self):
        return self.__volume.GetOutput()
    
    def get_structure_volume(self):
        return self.__structure_volume
    
    def execute(self):
        if self.__folder_path == "":
            self.__info = "Error: No folder path find!"
            self.__error_sign = True
        
        if self.__error_sign == False:
            # read DICOM image files
            try:
                self.__volume = self.__read_dicom_2D_series(self.__folder_path)
            except Exception as err:
                self.__info = str(err)
                self.__error_sign = True
                return
            
            # volume size, spacing, origin, direction
            volume_size = self.__volume.GetOutput().GetLargestPossibleRegion().GetSize()
            
            # return volume size as info
            self.__info = str(volume_size[0])+","+str(volume_size[1])+","+str(volume_size[2])
        
    def __read_dicom_2D_series(self,dicom_dir): 
        reader = dicom_2D_series.Dicom_2D_Series_Read()
        reader.set_dicom_dir(dicom_dir)
        reader.execute()
        
        # print(reader.get_file_names())
        # print(reader.get_image_origin())
        # print(reader.get_image_spacing())
        # print(reader.get_image_size())
        
        return reader.get_image()