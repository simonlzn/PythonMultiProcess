import vtk
import itk

class Slice_View:
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
        self.__image = flip
        
    def update(self):
        # originvtk
        (origin_x,origin_y,origin_z) = self.__image.GetOutput().GetOrigin()
        # spacing
        (spacing_x,spacing_y,spacing_z) = self.__image.GetOutput().GetSpacing()
        # size
        (size_x_min,size_x_max,size_y_min,size_y_max,size_z_min,size_z_max) = self.__image.GetExecutive().GetWholeExtent(self.__image.GetOutputInformation(0))
        
        # center
        center = (origin_x + spacing_x * 0.5 * (size_x_min + size_x_max),
                  origin_y + spacing_y * 0.5 * (size_y_min + size_y_max),
                  origin_z + spacing_z * 0.5 * (size_z_min + size_z_max))
        
        '''
        print("origin:"+"("+str(origin_x)+","+str(origin_y)+","+str(origin_z)+")")
        print("spacing:"+"("+str(spacing_x)+","+str(spacing_y)+","+str(spacing_z)+")")
        print("size:"+"("+str(size_x_max-size_x_min+1)+","+str(size_y_max-size_y_min+1)+","+str(size_z_max-size_z_min+1)+")")
        print("center:"+"("+str(center[0])+","+str(center[1])+","+str(center[2])+")")
        '''
        
        # axial
        axial = vtk.vtkMatrix4x4()
        axial.DeepCopy((1, 0, 0, center[0],
                        0, 1, 0, center[1],
                        0, 0, 1, center[2],
                        0, 0, 0, 1))
        
        # coronal
        coronal = vtk.vtkMatrix4x4()
        coronal.DeepCopy((1, 0, 0, center[0],
                          0, 0, 1, center[1],
                          0,-1, 0, center[2],
                          0, 0, 0, 1))
        
        # sagittal
        sagittal = vtk.vtkMatrix4x4()
        sagittal.DeepCopy((0, 0,-1, center[0],
                           1, 0, 0, center[1],
                           0,-1, 0, center[2],
                           0, 0, 0, 1))
        
        # extract a slice in the designed Orientation
        # axial
        reslice_axial = vtk.vtkImageReslice()
        reslice_axial.SetInputConnection(self.__image.GetOutputPort())
        reslice_axial.SetOutputDimensionality(2)
        reslice_axial.SetResliceAxes(axial)
        reslice_axial.SetInterpolationModeToLinear()
        
        # coronal
        reslice_coronal = vtk.vtkImageReslice()
        reslice_sagittal = vtk.vtkImageReslice()
        reslice_sagittal.SetInputConnection(self.__image.GetOutputPort())
        reslice_sagittal.SetOutputDimensionality(2)
        reslice_sagittal.SetResliceAxes(sagittal)
        reslice_sagittal.SetInterpolationModeToLinear()
        reslice_coronal.SetInputConnection(self.__image.GetOutputPort())
        reslice_coronal.SetOutputDimensionality(2)
        reslice_coronal.SetResliceAxes(coronal)
        reslice_coronal.SetInterpolationModeToLinear()
        
        # sagittal
        reslice_sagittal = vtk.vtkImageReslice()
        reslice_sagittal.SetInputConnection(self.__image.GetOutputPort())
        reslice_sagittal.SetOutputDimensionality(2)
        reslice_sagittal.SetResliceAxes(sagittal)
        reslice_sagittal.SetInterpolationModeToLinear()
        
        # actor
        # axial
        actor_axial = vtk.vtkImageActor()
        actor_axial.GetMapper().SetInputConnection(reslice_axial.GetOutputPort())
        
        # coronal
        actor_coronal = vtk.vtkImageActor()
        actor_coronal.GetMapper().SetInputConnection(reslice_coronal.GetOutputPort())
        
        # sagittal
        actor_sagittal = vtk.vtkImageActor()
        actor_sagittal.GetMapper().SetInputConnection(reslice_sagittal.GetOutputPort())
        
        # render
        # axial
        renderer_axial = vtk.vtkRenderer()
        renderer_axial.AddActor(actor_axial)
        renderer_axial.SetBackground(0,0,0)
        renderer_axial.SetViewport(0,0,1,1)
        
        # coronal
        renderer_coronal = vtk.vtkRenderer()
        renderer_coronal.AddActor(actor_coronal)
        renderer_coronal.SetBackground(0,0,0)
        renderer_coronal.SetViewport(0,0,1,1)
        
        # sagittal
        renderer_sagittal = vtk.vtkRenderer()
        renderer_sagittal.AddActor(actor_sagittal)
        renderer_sagittal.SetBackground(0,0,0)
        renderer_sagittal.SetViewport(0,0,1,1)
        
        # render window
        # axial
        render_window_axial = vtk.vtkRenderWindow()
        render_window_axial.AddRenderer(renderer_axial)
        
        # coronal
        render_window_coronal = vtk.vtkRenderWindow()
        render_window_coronal.AddRenderer(renderer_coronal)
        
        # sagittal
        render_window_sagittal = vtk.vtkRenderWindow()
        render_window_sagittal.AddRenderer(renderer_sagittal)
        
        # render window interactor
        # axial
        render_window_interactor_axial = vtk.vtkRenderWindowInteractor()
        render_window_interactor_axial.SetRenderWindow(render_window_axial)
        render_window_axial.SetInteractor(render_window_interactor_axial)
        
        # coronal
        render_window_interactor_coronal = vtk.vtkRenderWindowInteractor()
        render_window_interactor_coronal.SetRenderWindow(render_window_coronal)
        render_window_coronal.SetInteractor(render_window_interactor_coronal)
        
        # sagittal
        render_window_interactor_sagittal = vtk.vtkRenderWindowInteractor()
        render_window_interactor_sagittal.SetRenderWindow(render_window_sagittal)
        render_window_sagittal.SetInteractor(render_window_interactor_sagittal)
        
        # interactor style
        # axial
        interactor_style_axial = vtk.vtkInteractorStyleImage()
        render_window_interactor_axial.SetInteractorStyle(interactor_style_axial)
        render_window_axial.Render()
        
        # coronal
        interactor_style_coronal = vtk.vtkInteractorStyleImage()
        render_window_interactor_coronal.SetInteractorStyle(interactor_style_coronal)
        render_window_coronal.Render()
        
        # sagittal 
        interactor_style_sagittal = vtk.vtkInteractorStyleImage()
        render_window_interactor_sagittal.SetInteractorStyle(interactor_style_sagittal)
        render_window_sagittal.Render()
        
        render_window_interactor_axial.Initialize()
        render_window_interactor_coronal.Initialize()
        render_window_interactor_sagittal.Initialize()
        
        render_window_interactor_axial.Start()
        render_window_interactor_coronal.Start()
        render_window_interactor_sagittal.Start()
        
        '''
        # render window interactor
        # axial
        render_window_interactor_axial = vtk.vtkRenderWindowInteractor()
        render_window_interactor_axial.SetRenderWindow(render_window_axial)
        render_window_axial.SetInteractor(render_window_interactor_axial)
        
        # coronal
        render_window_interactor_coronal = vtk.vtkRenderWindowInteractor()
        render_window_interactor_coronal.SetRenderWindow(render_window_coronal)
        render_window_coronal.SetInteractor(render_window_interactor_coronal)
        
        # sagittal
        render_window_interactor_sagittal = vtk.vtkRenderWindowInteractor()
        render_window_interactor_sagittal.SetRenderWindow(render_window_sagittal)
        render_window_sagittal.SetInteractor(render_window_interactor_sagittal)
        
        # interactor style
        # axial
        interactor_style_axial = vtk.vtkInteractorStyleImage()
        render_window_interactor_axial.SetInteractorStyle(interactor_style_axial)
        render_window_axial.Render()
        
        
        # coronal
        interactor_style_coronal = vtk.vtkInteractorStyleImage()
        render_window_interactor_coronal.SetInteractorStyle(interactor_style_coronal)
        render_window_coronal.Render()
        
        # sagittal 
        interactor_style_sagittal = vtk.vtkInteractorStyleImage()
        render_window_interactor_sagittal.SetInteractorStyle(interactor_style_sagittal)
        render_window_sagittal.Render()
        
        # Create callbacks for slicing the image
        actions = {}
        actions["Slicing"] = 0
        
        def ButtonCallback(obj,event):
            # axial
        #    (current_mouse_x_axial, current_mouse_y_axial) = render_window_interactor_axial.GetEventPosition()
        #    render_window_interactor_axial.
        #    GetRenderer().SetDisplayPoint(render_window_interactor_axial.GetEventPosition())
            #render_window_axial.DisplayToView()
            #render_window_axial.ViewToWorld()
            #render_window_axial.GetRenderer.GetWorldPoint()
            #print(render_window_axial.GetRenderer.GetWorldPoint())
            
            
            # axial
            (current_mouse_x_axial, current_mouse_y_axial) = render_window_interactor_axial.GetEventPosition()
            (window_x_axial,window_y_axial) = render_window_axial.GetSize() # window size
            (window_center_x_axial,window_center_y_axial) = (window_x_axial/2,window_y_axial/2) # window center
            
            
            print("("+str(current_mouse_x_axial)+","+str(current_mouse_y_axial)+")")
            print("window size: "+str(window_x_axial)+","+str(window_y_axial))
            print("window center: ("+str(window_center_x_axial)+","+str(window_center_y_axial)+")")
            print("volume center: ("+str(center[0])+","+str(center[1])+","+str(center[2])+")")
            
            
        
        def MouseMoveCallback(obj,event):
            pass
        
        
        # axial
        interactor_style_axial.AddObserver("RightButtonPressEvent", ButtonCallback)
        interactor_style_axial.AddObserver("RightButtonReleaseEvent", ButtonCallback)
        interactor_style_axial.AddObserver("MouseMoveEvent", MouseMoveCallback)
        
        
        # coronal
        interactor_style_coronal.AddObserver("RightButtonPressEvent", ButtonCallback)
        interactor_style_coronal.AddObserver("RightButtonReleaseEvent", ButtonCallback)
        interactor_style_coronal.AddObserver("MouseMoveEvent", MouseMoveCallback)
        
        
        # sagittal
        interactor_style_sagittal.AddObserver("RightButtonPressEvent", ButtonCallback)
        interactor_style_sagittal.AddObserver("RightButtonReleaseEvent", ButtonCallback)
        interactor_style_sagittal.AddObserver("MouseMoveEvent", MouseMoveCallback)
        
        render_window_interactor_axial.Initialize()
        #render_window_interactor_coronal.Initialize()
        #render_window_interactor_sagittal.Initialize()
        
        render_window_interactor_axial.Start()
        #render_window_interactor_coronal.Start()
        #render_window_interactor_sagittal.Start()
        '''
