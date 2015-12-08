import itk
import sys

class Volume_Slicing_3D():
    def __init__(self):
        self.__slice_info = []
    
    def set_volume_coord(self,coord):
        self.__volume_coord = coord
        
    def set_volume(self,volume):
        self.__volume = volume
        
    def get_info(self):
        return self.__slice_info
    
    def update(self):
        volume_coord_transverse = self.__volume_coord[0]
        volume_coord_coronal = self.__volume_coord[1]
        volume_coord_sagittal = self.__volume_coord[2]
        
        volume_size = self.__volume.GetOutput().GetLargestPossibleRegion().GetSize()
        volume_spacing = self.__volume.GetOutput().GetSpacing()
        
        print(volume_size)
        print(volume_spacing)
        sys.stdout.flush()

        transverse_slice_info = "{}"
        coronal_slice_info = "{}"
        sagittal_slice_info = "{}"

        # transverse
        if not volume_coord_transverse < 0:
            transverse_slice_info = self.__do_slicing("transverse", volume_size[0], volume_size[1], volume_spacing[0], volume_spacing[1], self.__volume, volume_coord_transverse)
            
        # coronal
        if not volume_coord_coronal < 0:
            coronal_slice_info = self.__do_slicing("coronal", volume_size[0], volume_size[2], volume_spacing[0], volume_spacing[2], self.__volume, volume_coord_coronal)
        
        # sagittal
        if not volume_coord_sagittal < 0:
            sagittal_slice_info = self.__do_slicing("sagittal", volume_size[1], volume_size[2], volume_spacing[1], volume_spacing[2], self.__volume, volume_coord_sagittal)
         
        self.__slice_info = str(transverse_slice_info) + "," + \
                            str(coronal_slice_info) + "," + \
                            str(sagittal_slice_info)
                
    
    def __create_slice_info(self,view,row_size,column_size,row_spacing,column_spacing,pixel_data):
        info =  "{" + \
                "\"view\":\"" + str(view) + "\"," + \
                "\"row\":" + str(row_size) + "," + \
                "\"column\":" + str(column_size) + "," + \
                "\"rowspacing\":" + str(row_spacing) + "," + \
                "\"columnspacing\":" + str(column_spacing) + "," + \
                "\"data\":\"" + str(pixel_data) + "\"" + \
                "}"
                
        return info
    
    def __do_slicing(self,view,row_size,column_size,row_spacing,column_spacing,vol,slice_id):
        voxel_values = ""
        
        for row in range(0,row_size):
            for col in range(0,column_size):
                if view == "transverse":
                    val = vol.GetOutput().GetPixel((row,col,slice_id))
                elif view == "coronal":
                    val = vol.GetOutput().GetPixel((row,slice_id,col))
                elif view == "sagittal":
                    val = vol.GetOutput().GetPixel((slice_id,row,col))
                
                voxel_values += str(val)
                voxel_values += ","
                
        voxel_values = voxel_values[:-1] 
        
        slice_info = self.__create_slice_info(str(view), row_size, column_size, row_spacing, column_spacing, voxel_values)
        
        return slice_info
    