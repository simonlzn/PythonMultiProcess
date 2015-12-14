import itk

class Segmentation():
    def __init__(self):
        pass
    
    def read_volume(self,vol):
        self._vol = vol
        
    def get_segmented_volume(self):
        return self._vol_segmented
    
    def get_contour(self):
        return self._vol_contoured