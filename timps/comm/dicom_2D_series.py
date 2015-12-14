import itk

class Dicom_2D_Series_Read():
    '''
    variables
        (1) file_names
        (2) image
        (3) origin
        (4) spacing
        (5) size
    function
        (1) __init__
        (2) set_dicom_dir
        (3) update
        (4) get_file_names
        (5) get_image_origin
        (6) get_image_spacing
        (7) get_image_size
        (8) get_image
    '''
    
    def __init__(self):
        pass
    
    def set_dicom_dir(self,dicom_dir):
        self.__dicom_dir = dicom_dir
    
    def execute(self):
        dicom_io = itk.GDCMImageIO.New()
        
        # set image type to signed short (16-bits/pixel)
        reader = itk.ImageSeriesReader[itk.Image.SS3].New()
        reader.SetImageIO(dicom_io)
        
        name_generator = itk.GDCMSeriesFileNames.New()
        name_generator.SetUseSeriesDetails(True)
        name_generator.SetDirectory(self.__dicom_dir)
        
        series_uid = name_generator.GetSeriesUIDs()
        
        series_identifier = series_uid[0]
        
        file_names = name_generator.GetFileNames(series_identifier)
        
        # sort file names
        file_names = list(file_names)
        file_names.sort()
        file_names = tuple(file_names)
        
        self.__file_names = file_names
        
        reader.SetFileNames(self.__file_names)
        reader.Update()
        
        self.__image = reader        
    
    def get_file_names(self):
        return self.__file_names
    
    def get_image_origin(self):
        self.__origin = self.__image.GetOutput().GetOrigin()
        return self.__origin
    
    def get_image_spacing(self):
        self.__spacing = self.__image.GetOutput().GetSpacing()
        return self.__spacing
    
    def get_image_size(self):
        self.__size = self.__image.GetOutput().GetLargestPossibleRegion().GetSize()
        return self.__size
    
    def get_image_direction(self):
        self.__direction = self.__image.GetOutput().GetDirection()
        return self.__direction
    
    def get_image(self):
        return self.__image
    
