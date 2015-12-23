import itk
from timps.util import coordinate_system
import sys

class Structure_Volume_Reconstruction_3D():
    def __init__(self):
        self.__info = ""
        self.__structure_voxel_number = 0
        self.__structure_coords = [] # image coordinates
        self.__error_sign = False
    
    def set_structure_volume(self,structure_volume):
        self.__structure_vol = structure_volume
        
    def set_structure_index(self,structure_index):
        self.__structure_index = structure_index
        
    def set_structure_coordinates(self,structure_coordinates):
        # physical coordinates in DICOM space
        structure_coordinates_list = structure_coordinates.split(",")
        structure_coordinates_list.pop() # e.g. "-1.34,128.69,-409,"
        structure_coordinates_list_number = len(structure_coordinates_list)
        
        print(structure_coordinates_list_number)
        sys.stdout.flush()
        
        if structure_coordinates_list_number == 0:
            self.__info = "Error: No structure coordinates find!"
            self.__error_sign = True
        elif not structure_coordinates_list_number % 3 == 0:
            self.__info = "Error: Structure coordinates loss!"
            self.__error_sign = True
        else:
            structure_coordinates_x = structure_coordinates_list[0::3]
            structure_coordinates_y = structure_coordinates_list[1::3]
            structure_coordinates_z = structure_coordinates_list[2::3]
            
            self.__structure_voxel_number = structure_coordinates_list_number/3
            
            self.__info = str(self.__structure_voxel_number)
            
            coord_sys = coordinate_system.Coordinate_System()
            
            for i in xrange(self.__structure_voxel_number):
                coord = (float(structure_coordinates_x[i]),float(structure_coordinates_y[i]),float(structure_coordinates_z[i]))
                
                # convert physical coordinates to image coordinates, and keep image coordinates in self.__structure_coords
                self.__structure_coords.append(coord_sys.physical_coord2image_coord(coord, self.__structure_vol))
                
            # self.__structure_coords should not be modified yet
            self.__structure_coords = tuple(self.__structure_coords)

    def get_structure_volume(self):
        return self.__structure_vol
    
    def get_info(self):
        return self.__info
    
    def get_error_sign(self):
        return self.__error_sign
    
    def execute(self):
        if self.__error_sign == False:
            for i in xrange(self.__structure_voxel_number):
                self.__structure_vol.SetPixel(self.__structure_coords[i],self.__structure_index)
                
            self.__info = str(self.__structure_voxel_number)
        
    