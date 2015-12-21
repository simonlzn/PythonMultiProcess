import itk

from timps.comm import dicom_2D_series

class Volume_Reconstruction_3D():
    def __init__(self):
        pass
    
    def set_folder_path(self,folder_path):
        self.__folder_path = folder_path
        
    def get_info(self):
        return self.__info
    
    def get_volume(self):
        return self.__volume
    
    def get_structure_volume(self):
        return self.__structure_volume
    
    def execute(self):
        # read DICOM image files
        self.__volume = self.__read_dicom_2D_series(self.__folder_path)
        
        # volume size, spacing, origin, direction
        volume_size = self.__volume.GetOutput().GetLargestPossibleRegion().GetSize()
        volume_spacing = self.__volume.GetOutput().GetSpacing()
        volume_origin = self.__volume.GetOutput().GetOrigin()
        volume_direction = self.__volume.GetOutput().GetDirection()
        
        # create Structure Volume
        self.__structure_volume = self.__copy_volume(volume_size, volume_spacing, volume_origin, volume_direction, itk.UC, 3)
        
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
    
    def __copy_volume(self,size,spacing,origin,direction,pixel_type,dim):
        #image_type = itk.Image[pixel_type,dim]
        
        image_type = itk.Image.UC3
        
        new_vol = itk.Image[image_type].New()
        
        new_vol_region = itk.ImageRegion[dim]()
        new_vol_region.SetSize(size)
        new_vol_region.SetIndex((0,0,0))
        
        new_vol.SetRegions(new_vol_region)
        new_vol.SetSpacing(spacing)
        new_vol.SetOrigin(origin)
        new_vol.SetDirection(direction)
        new_vol.Allocate()
        
        for i in xrange(size[0]):
            for j in xrange(size[0]):
                for k in xrange(size[0]):
                    new_vol.SetPixel((i,j,k),0)
                    
        return new_vol
      