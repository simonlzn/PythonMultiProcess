import itk

class Coordinate_System():
    def __init__(self):
        pass
    
    def physical_coord2image_coord(self,phy_coord,vol):
        return vol.TransformPhysicalPointToIndex(phy_coord)
    
    def image_coord2phy_coord(self,img_coord,vol):
        return vol.TransformIndexToPhysicalPoint(img_coord)