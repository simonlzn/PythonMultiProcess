import itk
import os

class Slicing_2D:
    def __init__(self):
        pass
    
    def set_image(self,image):
        self.__image = image
        self.__size = image.GetOutput().GetLargestPossibleRegion().GetSize()
        
    def set_output_dir(self,dir):
        self.__output_dir = dir
    
    def __slicing_axial(self,dir):
        axial_plane = itk.Image[itk.SS,2].New()
        
        axial_region = itk.ImageRegion[2]()
        axial_region.SetSize((int(self.__size[0]),int(self.__size[1])))
        axial_region.SetIndex((0,0))
        
        axial_plane.SetRegions(axial_region)
        axial_plane.Allocate()
        
        for k in range(0,self.__size[2]):
            for i in range(0,self.__size[0]):
                for j in range(0,self.__size[1]):
                    id = (i,j)
                    val = self.__image.GetOutput().GetPixel((i,j,k))
                    axial_plane.SetPixel(id,val)
                    
            axial_rescale = itk.RescaleIntensityImageFilter[itk.Image.SS2,itk.Image.UC2].New()
            axial_rescale.SetInput(axial_plane)
            axial_rescale.SetOutputMinimum(0)
            axial_rescale.SetOutputMaximum(255)
            axial_rescale.Update()
            
            axial_writer = itk.ImageFileWriter[itk.Image.UC2].New()
            axial_writer.SetInput(axial_rescale.GetOutput())
            axial_writer.SetFileName(dir+"/axial_"+str(k)+".png")
            axial_writer.Update()
        
    
    def __slicing_coronal(self,dir):
        coronal_plane = itk.Image[itk.SS,2].New()
        
        coronal_region = itk.ImageRegion[2]()
        coronal_region.SetSize((int(self.__size[0]),int(self.__size[2])))
        coronal_region.SetIndex((0,0))
        
        coronal_plane.SetRegions(coronal_region)
        coronal_plane.Allocate()
        
        for j in range(0,self.__size[1]):
            for i in range(0,self.__size[0]):
                for k in range(0,self.__size[2]):
                    id = (i,k)
                    val = self.__image.GetOutput().GetPixel((i,j,k))
                    coronal_plane.SetPixel(id,val)
                
            coronal_rescale = itk.RescaleIntensityImageFilter[itk.Image.SS2,itk.Image.UC2].New()
            coronal_rescale.SetInput(coronal_plane)
            coronal_rescale.SetOutputMinimum(0)
            coronal_rescale.SetOutputMaximum(255)
            coronal_rescale.Update()
            
            coronal_writer = itk.ImageFileWriter[itk.Image.UC2].New()
            coronal_writer.SetInput(coronal_rescale.GetOutput())
            coronal_writer.SetFileName(dir+"/coronal_"+str(j)+".png")
            coronal_writer.Update()
            
        
    def __slicing_sagittal(self,dir):
        sagittal_plane = itk.Image[itk.SS,2].New()
        
        sagittal_region = itk.ImageRegion[2]()
        sagittal_region.SetSize((int(self.__size[1]),int(self.__size[2])))
        sagittal_region.SetIndex((0,0))
        
        sagittal_plane.SetRegions(sagittal_region)
        sagittal_plane.Allocate()
        
        for i in range(0,self.__size[0]):
            for j in range(0,self.__size[1]):
                for k in range(0,self.__size[2]):
                    id = (j,k)
                    val = self.__image.GetOutput().GetPixel((i,j,k))
                    sagittal_plane.SetPixel(id,val)
                
            sagittal_rescale = itk.RescaleIntensityImageFilter[itk.Image.SS2,itk.Image.UC2].New()
            sagittal_rescale.SetInput(sagittal_plane)
            sagittal_rescale.SetOutputMinimum(0)
            sagittal_rescale.SetOutputMaximum(255)
            sagittal_rescale.Update()
            
            sagittal_writer = itk.ImageFileWriter[itk.Image.UC2].New()
            sagittal_writer.SetInput(sagittal_rescale.GetOutput())
            sagittal_writer.SetFileName(dir+"/sagittal_"+str(i)+".png")
            sagittal_writer.Update()
        
    def update(self):
        axial_dir = self.__output_dir+"/axial"
        coronal_dir = self.__output_dir+"/coronal"
        sagittal_dir = self.__output_dir+"/sagittal"
        
        if not os.path.exists(axial_dir):
            os.mkdir(axial_dir)
            
        if not os.path.exists(coronal_dir):
            os.mkdir(coronal_dir)
            
        if not os.path.exists(sagittal_dir):
            os.mkdir(sagittal_dir)
        
        self.__slicing_axial(axial_dir)
        self.__slicing_coronal(coronal_dir)
        self.__slicing_sagittal(sagittal_dir)
        