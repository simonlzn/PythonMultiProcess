import vtk
import itk

class Rendering_3D:
    def __init__(self):
        pass
    
    def read_image(self,itk_image):
        # convert ITK image to VTK image, set image type to signed short (16-bits/pixel)
        vtk_image = itk.ImageToVTKImageFilter[itk.Image.SS3].New()
        vtk_image.SetInput(itk_image.GetOutput())
        vtk_image.Update()
        
        # the coordinates of ITK and VTK are inconsistent, so flip the y-axis of the image
        flip = vtk.vtkImageFlip()
        flip.SetInputData(vtk_image.GetOutput())
        flip.SetFilteredAxes(1)
        flip.Update()
        self._image = flip
    

class Surface_Rendering_3D(Rendering_3D):
    def __init__(self):
        Rendering_3D.__init__(self)
    
    def read_image(self, itk_image):
        Rendering_3D.read_image(self, itk_image)
        
    def set_surface_value(self,value):
        self.__surface_value = value
    
    def update(self):
        surface_extractor = vtk.vtkContourFilter()
        surface_extractor.SetInputConnection(self._image.GetOutputPort())
        surface_extractor.SetValue(0, self.__surface_value)
        
        surface_normals = vtk.vtkPolyDataNormals()
        surface_normals.SetInputConnection(surface_extractor.GetOutputPort())
        surface_normals.SetFeatureAngle(60.0)
        
        surface_stripper = vtk.vtkStripper()
        surface_stripper.SetInputConnection(surface_normals.GetOutputPort())
        
        surface_mapper = vtk.vtkPolyDataMapper()
        surface_mapper.SetInputConnection(surface_stripper.GetOutputPort())
        surface_mapper.ScalarVisibilityOff()
        
        surface_actor = vtk.vtkActor()
        surface_actor.SetMapper(surface_mapper)
        
        camera = vtk.vtkCamera()
        camera.SetViewUp(0.0, 0.0, -1.0)
        camera.SetPosition(0.0, 1.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.ComputeViewPlaneNormal()
        camera.Dolly(1.5)
        
        renderer = vtk.vtkRenderer()
        renderer.AddActor(surface_actor)
        renderer.SetActiveCamera(camera)
        renderer.ResetCamera()
        renderer.SetBackground(0.0,0.0,0.0)
        renderer.ResetCameraClippingRange()
        
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)
        render_window_interactor.Initialize()
        render_window.Render()
        render_window_interactor.Start()
    
class Volume_Rendering_3D(Rendering_3D):
    # Maximum intensity projections (MIP)
    def __init__(self):
        Rendering_3D.__init__(self)
        
    def read_image(self, itk_image):
        Rendering_3D.read_image(self, itk_image)
        
    def update(self):
        # only unsigned char or unsigned short can be accepted by vtkVolumeRayCastMapper, so convert signed short to unsigned short
        val_range = self._image.GetOutput().GetScalarRange()
        min_val = val_range[0]
        max_val = val_range[1]
        diff = max_val - min_val
        slope = 65536/diff # 16 bits/pixel
        inter = -slope*min_val
        shift = inter/slope
        
        shifter = vtk.vtkImageShiftScale()
        shifter.SetShift(shift)
        shifter.SetScale(slope)
        shifter.SetOutputScalarTypeToUnsignedShort()
        shifter.SetInputConnection(self._image.GetOutputPort())
        shifter.ReleaseDataFlagOff()
        shifter.Update()
        
        volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        volume_mapper.SetInputConnection(shifter.GetOutputPort())
        
        volume_color = vtk.vtkColorTransferFunction()
        
        volume_scalar_opacity = vtk.vtkPiecewiseFunction()
        
        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetIndependentComponents(True)
        volume_property.SetColor(volume_color)
        volume_property.SetScalarOpacity(volume_scalar_opacity)
        volume_property.SetInterpolationTypeToLinear()
        
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        
        volume_color.AddRGBSegment(0.0,0.0,0.0,0.0,1000,1.0,1.0,1.0)
        volume_scalar_opacity.AddSegment(0, 0, 65536, 1) # 16 bits/pixel
        volume_mapper.SetBlendModeToMaximumIntensity()
        
        camera = vtk.vtkCamera()
        camera.SetViewUp(0.0, 0.0, -1.0)
        camera.SetPosition(0.0, 1.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.ComputeViewPlaneNormal()
        camera.Dolly(1.5)
        
        renderer = vtk.vtkRenderer()
        renderer.AddViewProp(volume)
        renderer.SetActiveCamera(camera)
        renderer.ResetCamera()
        renderer.SetBackground(0.0,0.0,0.0)
        renderer.ResetCameraClippingRange()
        
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)
        render_window_interactor.Initialize()
        render_window.Render()
        render_window_interactor.Start()

 