import itk

class Region_Growing:
    def __init__(self):
        pass
    
    def read_image(self,itk_image):
        self._image = itk_image
        
    def get_segmented_image(self):
        return self._image_segmented
    
    def get_contour(self):
        # binary contour
        binary_contour = itk.BinaryContourImageFilter[itk.Image.SS3,itk.Image.SS3].New()
        binary_contour.SetInput(self._image_segmented)
        binary_contour.SetBackgroundValue(0)
        binary_contour.SetForegroundValue(2**15-1) # i.e. 32767
        binary_contour.Update()
        
        self._contour = binary_contour.GetOutput()
        
        return self._contour
        

class Region_Growing_Connected_Threshold(Region_Growing):
    def __init__(self):
        Region_Growing.__init__(self)
        self.__lower_threshold = -2**15 # i.e. -32768
        self.__upper_threshold = 2**15-1 # i.e. 32767
        self.__seed = (0,0,0)
     
    def read_image(self, itk_image):
        Region_Growing.read_image(self, itk_image)
        
    def set_lower_threshold(self,threshold):
        self.__lower_threshold = threshold
        
    def set_upper_threshold(self,threshold):
        self.__upper_threshold = threshold
        
    def set_seed(self,seed):
        self.__seed = seed
        
    def update(self):
        # cast SS3 to F3
        caster_SS3_to_F3 = itk.CastImageFilter[itk.Image.SS3,itk.Image.F3].New()
        caster_SS3_to_F3.SetInput(self._image.GetOutput())
        caster_SS3_to_F3.Update()
        
        # smoothing
        smoothing = itk.CurvatureFlowImageFilter[itk.Image.F3,itk.Image.F3].New()
        smoothing.SetInput(caster_SS3_to_F3.GetOutput())
        smoothing.SetNumberOfIterations(5)
        smoothing.SetTimeStep(0.125)
        smoothing.Update()
        
        # region growing (connected threshold)
        connected_threshold = itk.ConnectedThresholdImageFilter[itk.Image.F3,itk.Image.F3].New()
        connected_threshold.SetInput(smoothing.GetOutput())
        connected_threshold.SetLower(self.__lower_threshold)
        connected_threshold.SetUpper(self.__upper_threshold)
        connected_threshold.SetSeed(self.__seed)
        connected_threshold.SetReplaceValue(2**15-1) # i.e. 32767
        connected_threshold.Update()
        
        # cast F3 to SS3
        caster_F3_to_SS3 = itk.CastImageFilter[itk.Image.F3, itk.Image.SS3].New()
        caster_F3_to_SS3.SetInput(connected_threshold.GetOutput())
        caster_F3_to_SS3.Update()
        
        # hole filling
        hole_filling = itk.VotingBinaryIterativeHoleFillingImageFilter[itk.Image.SS3].New()
        hole_filling.SetInput(caster_F3_to_SS3.GetOutput())
        hole_filling.SetRadius((2,2,2))
        hole_filling.SetBackgroundValue(0)
        hole_filling.SetForegroundValue(2**15-1) # i.e. 32767
        hole_filling.SetMajorityThreshold(2)
        hole_filling.SetMaximumNumberOfIterations(1)
        hole_filling.Update()
        
        #print(hole_filling.GetCurrentNumberOfIterations())
        #print(hole_filling.GetNumberOfPixelsChanged())
        
        self._image_segmented = hole_filling.GetOutput()
        
    def get_segmented_image(self):
        return Region_Growing.get_segmented_image(self)
    
    def get_contour(self):
        return Region_Growing.get_contour(self)
    
        
        
        
