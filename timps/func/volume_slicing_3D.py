import itk

from timps.comm import slicing_2D

class Volume_Slicing_3D():
    def __init__(self):
        self.__slice_info = ""
    
    def set_volume_coord(self,coord):
        self.__volume_coord = coord
        
    def set_volume(self,volume):
        self.__volume = volume
        
    def get_info(self):
        return self.__slice_info
    
    def __do_slicing(self,slice_id,view,row,col,row_spacing,col_spacing):
        if slice_id >= 0:
            slicing = slicing_2D.Slicing_2D()
            slicing.set_view(str(view))
            slicing.set_size((row,col))
            slicing.set_spacing((row_spacing,col_spacing))
            slicing.set_volumn(self.__volume)
            slicing.set_slice_id(slice_id)
            slicing.execute()
            slice_info = slicing.get_slice_info()
        else:
            slice_info = "{}"
            
        return slice_info
            

    def execute(self):
        volume_coord_transverse = self.__volume_coord[0]
        volume_coord_coronal = self.__volume_coord[1]
        volume_coord_sagittal = self.__volume_coord[2]
        
        volume_size = self.__volume.GetOutput().GetLargestPossibleRegion().GetSize()
        volume_spacing = self.__volume.GetOutput().GetSpacing()
        
        transverse_slice_info = self.__do_slicing(volume_coord_transverse,'transverse',volume_size[0],volume_size[1],volume_spacing[0],volume_spacing[1])
        coronal_slice_info = self.__do_slicing(volume_coord_coronal,'coronal',volume_size[0],volume_size[2],volume_spacing[0],volume_spacing[2])
        sagittal_slice_info = self.__do_slicing(volume_coord_sagittal,'sagittal',volume_size[1],volume_size[2],volume_spacing[1],volume_spacing[2])
        
        
        self.__slice_info = str(transverse_slice_info) + "," + \
                            str(coronal_slice_info) + "," + \
                            str(sagittal_slice_info)
        
    