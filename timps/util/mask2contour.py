import itk

class Mask2Contour():
    def __init__(self):
        pass
    
    def read_segmented_volume(self,vol_segmented):
        self.__vol_segmented = vol_segmented
        
    def get_contoured_volume(self):
        return self.__vol_contoured
    
    def __extract_slice(self,slice_id):
        slice_plane = itk.Image[itk.UC,2].New()
            
        slice_region = itk.ImageRegion[2]()
        slice_region.SetSize((int(self.__vol_size[0]),int(self.__vol_size[1])))
        slice_region.SetIndex((0,0))
        
        slice_plane.SetRegions(slice_region)
        slice_plane.Allocate()
        
        for i in xrange(self.__vol_size[0]):
            for j in xrange(self.__vol_size[1]):
                idx = (i,j)
                val = self.__vol_segmented.GetPixel((i,j,slice_id))
                slice_plane.SetPixel(idx,val)
                
        return slice_plane
    
    def __segment2contour(self,segment):
        # binary contour
        contour = itk.BinaryContourImageFilter[itk.Image.UC2,itk.Image.UC2].New()
        contour.SetInput(segment)
        contour.SetBackgroundValue(0)
        contour.SetForegroundValue(1)
        contour.Update()
        
        return contour.GetOutput()
    
    def __merge_slice(self,slice_id,slice_plane):
        for i in xrange(self.__vol_size[0]):
            for j in xrange(self.__vol_size[1]):
                idx = (i,j,slice_id)
                val = slice_plane.GetPixel((i,j))
                self.__vol_contoured.SetPixel(idx,val)
                
    def __create_contoured_volume(self,vol):
        vol_contoured = itk.Image[itk.UC,3].New()
        
        vol_contoured_region = itk.ImageRegion[3]()
        vol_contoured_region.SetSize(vol.GetLargestPossibleRegion().GetSize())
        vol_contoured_region.SetIndex((0,0,0))
        
        vol_contoured.SetRegions(vol_contoured_region)
        vol_contoured.SetSpacing(vol.GetSpacing())
        vol_contoured.SetOrigin(vol.GetOrigin())
        vol_contoured.SetDirection(vol.GetDirection())
        vol_contoured.Allocate()
        
        return vol_contoured
    
    def execute(self):
        self.__vol_size = self.__vol_segmented.GetLargestPossibleRegion().GetSize()
        
        self.__vol_contoured = self.__create_contoured_volume(self.__vol_segmented)
        
        for k in xrange(self.__vol_size[2]):
            # extract a slice from segmented volume
            segment_slice = self.__extract_slice(k)
            
            # convert segment to contour
            contour_slice = self.__segment2contour(segment_slice)
                    
            # merge all slice to generate a contour volume
            self.__merge_slice(k, contour_slice)
            
        