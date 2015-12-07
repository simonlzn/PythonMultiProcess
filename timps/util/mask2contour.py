# convert mask to contour (3D)
# Subrahmanyam Gorthi, Meritxel Bach Cuadra, Jean-Philippe Thiran, Exporting Contours to DICOM-RT Structure Set, 2009 (http://www.insight-journal.org/browse/publication/316)

import itk

class Mask2Contour_3D:
    def __init__(self):
        pass
    
    def read_mask(self,mask):
        self.__mask = mask
        
    def set_contour_value(self,value):
        self.__contour_value = value
        
    def set_contour_file_directory(self,dir):
        self.__contour_file_dir = dir
    
    def update(self):
        spacing = self.__mask.GetOutput().GetSpacing()
        
        contour_extractor = itk.ContourExtractor2DImageFilter[itk.Image.SS2].New()
        contour_extractor.SetContourValue(self.__contour_value)
        contour_extractor.ReverseContourOrientationOn()
        
        region = self.__mask.GetOutput().GetLargestPossibleRegion()
        
        size = region.GetSize()
        
        number_of_slices = size[2]
        
        # only one axial slice at a time is considered
        size[2] = 0
        
        slice_region = itk.ImageRegion[3]()
        slice_region.SetSize(size)
        start = region.GetIndex()
        
        
        slice_extractor = itk.ExtractImageFilter[itk.Image.SS3,itk.Image.SS2].New()
        
        for current_slice in range(0,number_of_slices):
            start[0] = 0
            start[1] = 0
            start[2] = current_slice
            
            slice_region.SetIndex(start)
            
            slice_extractor.SetExtractionRegion(slice_region)
            slice_extractor.SetInput(self.__mask.GetOutput())
            contour_extractor.SetInput(slice_extractor.GetOutput())
            
            contour_extractor.Update()
            
            self.write_contour_vertices(self.__contour_file_dir,contour_extractor,current_slice,)
            
            
    def write_contour_vertices(self,dir,contour_extractor,current_slice):
        pass
    
    def write_common_data(self):
        pass
    
    def write_vertex_coordinate(self):
        pass
    
    def write_last_vertex_coordinate(self):
        pass
    
    def append_text_file(self):
        pass