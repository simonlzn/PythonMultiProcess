import itk
from timps.algorithms import region_growing

class Region_Growing_Segmentation_3D():
    def __init__(self):
        pass
    
    def set_volume(self,volume):
        self.__volume = volume
        
    def set_seed(self,seed):
        self.__seed = seed
        
    def set_threshold(self,threshold):
        self.__threshold = threshold
        
    def execute(self):
        region_growing_segmentation = region_growing.Region_Growing_Connected_Threshold()
        region_growing_segmentation.read_volume(self.__volume)
        region_growing_segmentation.set_seed(self.__seed)
        region_growing_segmentation.set_threshold(self.__threshold)
        region_growing_segmentation.execute()
        
        self.__contoured_volume = region_growing_segmentation.get_contour()
        self.__segmented_volume = region_growing_segmentation.get_segmented_volume()
        
    def get_contoured_volume(self):
        return self.__contoured_volume
    
    def get_segmented_volume(self):
        return self.__segmented_volume