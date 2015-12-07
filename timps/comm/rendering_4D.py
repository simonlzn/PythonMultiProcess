import vtk
import itk


class Rendering_4D:
    def __init__(self):
        pass
    
    def read_image(self,itk_image):
        # convert ITK image to VTK image, set image type to signed short (16-bits/pixel)
        vtk_image = itk.ImageToVTKImageFilter[itk.Image.SS3].New()
        vtk_image.SetInput(itk_image.GetOutput())
        vtk_image.Update()
            
        # the coordinate of ITK and VTK are inconsistent, so flip the y-axis of the image
        flip = vtk.vtkImageFlip()
        flip.SetInputData(vtk_image.GetOutput())
        flip.SetFilteredAxes(1)
        flip.Update()
        
        self._image = flip
        
    def set_file_directory(self,dir):
        self._file_dir = dir
        
    def set_temporary_file_directory(self,dir):
        self._temporary_file_dir = dir
            
            
            
            
        
        
        
class Surface_Rendering_4D(Rendering_4D):
    def __init__(self):
        Rendering_4D.__init__(self)
        
    def read_image(self, itk_image):
        Rendering_4D.read_image(self, itk_image)
        
    def set_surface_value(self,value):
        self.__surface_value = value
        
    def set_file_directory(self, dir):
        Rendering_4D.set_file_directory(self, dir)
        
    def set_temporary_file_directory(self, dir):
        Rendering_4D.set_temporary_file_directory(self, dir)
        
    def update(self):
        dicom_io = itk.GDCMImageIO.New()
        
        name_generator = itk.GDCMSeriesFileNames.New()
        name_generator.SetUseSeriesDetails(True)
        name_generator.SetDirectory(self._file_dir)
        
        series_uid = name_generator.GetSeriesUIDs()
    
        cycle_number = len(series_uid)
        
        for cycle_id in range(0,cycle_number):
            print("*** load cycle: "+str(cycle_id)+" ***")
            
            series_identifier = series_uid[cycle_id]
            
            file_names = name_generator.GetFileNames(series_identifier)
            
            # sort file names
            file_names = list(file_names)
            file_names.sort()
            
            file_names = tuple(file_names)
        
            # set image type to signed short (16-bits/pixel)
            itk_reader = itk.ImageSeriesReader[itk.Image.SS3].New()
            itk_reader.SetImageIO(dicom_io)
            itk_reader.SetFileNames(file_names)
            itk_reader.Update()
            
            self.read_image(itk_reader)

            surface_extractor = vtk.vtkMarchingCubes()
            surface_extractor.SetInputConnection(self._image.GetOutputPort())
            surface_extractor.SetValue(0,self.__surface_value)
            surface_extractor.ComputeNormalsOn()
            surface_extractor.ComputeScalarsOn()
            surface_extractor.Update()
            
            writer = vtk.vtkXMLPolyDataWriter()
            writer.SetInputData(surface_extractor.GetOutput())
            writer.SetFileName(self._temporary_file_dir+"/cycle"+str(cycle_id)+".vtp")
            writer.Update()
            
        render_window = vtk.vtkRenderWindow()    
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        
        camera = vtk.vtkCamera()
        camera.SetViewUp(0.0, 0.0, -1.0)
        camera.SetPosition(0.0, 1.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.ComputeViewPlaneNormal()
        camera.Dolly(1.5)
        
        for cycle_id in range(0,cycle_number):
            print("*** display cycle "+str(cycle_id)+" ***")
            
            reader = vtk.vtkXMLPolyDataReader()
            reader.SetFileName(self._temporary_file_dir+"/cycle"+str(cycle_id)+".vtp")
            reader.Update()
            
            surface_mapper = vtk.vtkPolyDataMapper()
            surface_mapper.SetInputConnection(reader.GetOutputPort())
            surface_mapper.ScalarVisibilityOff()
            
            surface_actor = vtk.vtkActor()
            surface_actor.SetMapper(surface_mapper)
            
            renderer = vtk.vtkRenderer()
            render_window.AddRenderer(renderer)
            render_window_interactor.SetRenderWindow(render_window)
            
            renderer.AddActor(surface_actor)
            renderer.ResetCameraClippingRange()
            renderer.SetActiveCamera(camera)
            renderer.ResetCamera()
            renderer.SetBackground(0.0,0.0,0.0)
            
            render_window.Render()
            render_window_interactor.Initialize()
            render_window_interactor.CreateRepeatingTimer(20)

class Volume_Rendering_4D(Rendering_4D):
    def __init__(self):
        Rendering_4D.__init__(self)
        
    def read_image(self, itk_image):
        Rendering_4D.read_image(self, itk_image)
        
    def set_file_directory(self, dir):
        Rendering_4D.set_file_directory(self, dir)
        
    def update(self):
        dicom_io = itk.GDCMImageIO.New()
        
        name_generator = itk.GDCMSeriesFileNames.New()
        name_generator.SetUseSeriesDetails(True)
        name_generator.SetDirectory(self._file_dir)
        
        series_uid = name_generator.GetSeriesUIDs()
    
        #cycle_number = len(series_uid)
        cycle_number = 1
        
        render_window = vtk.vtkRenderWindow()    
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        
        camera = vtk.vtkCamera()
        camera.SetViewUp(0, 1, 0)
        camera.SetPosition(1.0, 0.0, 0.0)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        #camera.ComputeViewPlaneNormal()
        camera.Dolly(1.5)
        
        for cycle_id in range(0,cycle_number):
            print("*** load cycle: "+str(cycle_id)+" ***")
            
            series_identifier = series_uid[cycle_id]
            
            file_names = name_generator.GetFileNames(series_identifier)
            
            # sort file names
            file_names = list(file_names)
            file_names.sort()
            
            file_names = tuple(file_names)
        
            # set image type to signed short (16-bits/pixel)
            itk_reader = itk.ImageSeriesReader[itk.Image.SS3].New()
            itk_reader.SetImageIO(dicom_io)
            itk_reader.SetFileNames(file_names)
            itk_reader.Update()
            
            # ===================================
            spacing = itk_reader.GetOutput().GetSpacing()
            spacing[2] = 3
            itk_reader.GetOutput().SetSpacing(spacing)
            # ===================================
                       
            print(itk_reader().GetOutput().GetSpacing())
                       
            self.read_image(itk_reader)
            
            # only unsigned char or unsigned short can be accepted by vtkVolumeRayCastMapper, so convert signed short to unsigned short
            val_range = self._image.GetOutput().GetScalarRange()
            min_val = val_range[0]
            max_val = val_range[1]
            diff = max_val - min_val
            slope = 65536/diff # 16-bits/pixel
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
            volume_property.SetInterpolationTypeToNearest()
            
            volume = vtk.vtkVolume()
            volume.SetMapper(volume_mapper)
            volume.SetProperty(volume_property)
            
            volume_color.AddRGBSegment(0.0,0.0,0.0,0.0,1000,1.0,1.0,1.0)
            volume_scalar_opacity.AddSegment(0, 0, 65536, 1) # 16 bits/pixel
            volume_mapper.SetBlendModeToMaximumIntensity()
            
            renderer = vtk.vtkRenderer()
            render_window.AddRenderer(renderer)
            render_window_interactor.SetRenderWindow(render_window)
            
            renderer.AddViewProp(volume)
            #renderer.ResetCameraClippingRange()
            renderer.SetActiveCamera(camera)
            renderer.ResetCamera()
            renderer.SetBackground(0.0,0.0,0.0)
            
            render_window.Render()
            render_window_interactor.Initialize()
            #render_window_interactor.CreateRepeatingTimer(20)
            render_window_interactor.Start()
           
