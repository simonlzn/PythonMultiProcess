import itk

class Slicing_2D:
    def __init__(self):
        pass
    
    def set_view(self,view):
        self.__view = view
        
    def set_size(self,size):
        self.__row_size = size[0]
        self.__column_size = size[1]
        
    def set_spacing(self,spacing):
        self.__row_spacing = spacing[0]
        self.__column_spacing = spacing[1]
        
    def set_volumn(self,vol):
        self.__vol = vol
        
    def set_slice_id(self, slice_id):
        self.__slice_id = slice_id
        
    def get_slice_info(self):
        return self.__slice_info
    
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

    def execute(self):
        voxel_values = ""

        for col in xrange(self.__column_size):
            for row in xrange(self.__row_size):
                if self.__view == "transverse":
                    val = self.__vol.GetPixel((row,col,self.__slice_id)) 
                elif self.__view == "coronal":
                    val = self.__vol.GetPixel((row,self.__slice_id,int(self.__column_size-col))) 
                elif self.__view == "sagittal":
                    val = self.__vol.GetPixel((self.__slice_id,row,int(self.__column_size-col))) 
                
                voxel_values += str(val)
                voxel_values += ","
        
                
        voxel_values = voxel_values[:-1] 
        
        self.__slice_info = self.__create_slice_info(str(self.__view), self.__row_size, self.__column_size, self.__row_spacing, self.__column_spacing, voxel_values)
        
    