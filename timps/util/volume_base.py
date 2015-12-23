import itk

class Volume_Base:
    def __init__(self):
        pass
    
    def copy_volume(self,vol,voxel_type):
        size = vol.GetLargestPossibleRegion().GetSize()
        spacing = vol.GetSpacing()
        origin = vol.GetOrigin()
        direction = vol.GetDirection()
        
        new_vol = itk.Image[voxel_type,3].New()
        
        new_vol_region = itk.ImageRegion[3]()
        new_vol_region.SetSize(size)
        new_vol_region.SetIndex((0,0,0))
        
        new_vol.SetRegions(new_vol_region)
        new_vol.SetSpacing(spacing)
        new_vol.SetOrigin(origin)
        new_vol.SetDirection(direction)
        new_vol.Allocate()
        
        for i in xrange(size[0]):
            for j in xrange(size[1]):
                for k in xrange(size[2]):
                    new_vol.SetPixel((i,j,k),0)
                    
        return new_vol
        