import itk
from timps.algorithms import segmentation
from timps.util import mask2contour

class Region_Growing(segmentation.Segmentation):
    def __init__(self):
        pass
        
    def read_volume(self, vol):
        segmentation.Segmentation.read_volume(self, vol)
        
    def get_segmented_volume(self):
        return segmentation.Segmentation.get_segmented_volume(self)
    
    def get_contour(self):
        return segmentation.Segmentation.get_contour(self)
        
        
    
class Region_Growing_Connected_Threshold(Region_Growing):
    def __init__(self):
        Region_Growing.__init__(self)
        self.__lower_threshold = -32768 # -2**15
        self.__upper_threshold = 32767 # 2**15-1
        
    def read_volume(self, vol):
        Region_Growing.read_volume(self, vol)
        
    def set_threshold(self,threshold):
        self.__lower_threshold = threshold[0]
        self.__upper_threshold = threshold[1]
        
    def set_seed(self,seed):
        self.__seed = seed
        
    def execute(self):
        # cast SS3 to F3
        caster_SS3_to_F3 = itk.CastImageFilter[itk.Image.SS3,itk.Image.F3].New()
        caster_SS3_to_F3.SetInput(self._vol.GetOutput())
        caster_SS3_to_F3.Update()
        
        # smoothing
        smoothing = itk.CurvatureFlowImageFilter[itk.Image.F3,itk.Image.F3].New()
        smoothing.SetInput(caster_SS3_to_F3.GetOutput())
        smoothing.SetNumberOfIterations(5)
        smoothing.SetTimeStep(0.125)
        smoothing.Update()
        
        # region growing connected threshold
        connected_threshold = itk.ConnectedThresholdImageFilter[itk.Image.F3,itk.Image.F3].New()
        connected_threshold.SetInput(smoothing.GetOutput())
        connected_threshold.SetLower(self.__lower_threshold)
        connected_threshold.SetUpper(self.__upper_threshold)
        connected_threshold.SetSeed(self.__seed)
        connected_threshold.SetReplaceValue(1)
        connected_threshold.Update()
        
        # cast F3 to UC3
        caster_F3_to_UC3 = itk.CastImageFilter[itk.Image.F3,itk.Image.UC3].New()
        caster_F3_to_UC3.SetInput(connected_threshold.GetOutput())
        caster_F3_to_UC3.Update()
        
        # hole filling
        hole_filling = itk.VotingBinaryIterativeHoleFillingImageFilter[itk.Image.UC3].New()
        hole_filling.SetInput(caster_F3_to_UC3.GetOutput())
        hole_filling.SetRadius((1,1,1)) # 3*3*3
        hole_filling.SetBackgroundValue(0)
        hole_filling.SetForegroundValue(1)
        hole_filling.SetMajorityThreshold(2) 
        hole_filling.SetMaximumNumberOfIterations(10)
        hole_filling.Update()
        
        self._vol_segmented = hole_filling.GetOutput()
        
        # convert mask to contour
        mask_to_contour = mask2contour.Mask2Contour()
        mask_to_contour.read_segmented_volume(self._vol_segmented)
        mask_to_contour.execute()
        
        self._vol_contoured = mask_to_contour.get_contoured_volume()
        
    def get_segmented_volume(self):
        return Region_Growing.get_segmented_volume(self)
    
    def get_contour(self):
        return Region_Growing.get_contour(self)