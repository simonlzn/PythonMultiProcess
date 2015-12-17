import itk
import math


class Contour2Mask():
    def __init__(self):
        pass
    
    def read_volume(self,vol):
        self.__vol = vol
        
    def load_contour(self,contour):
        self.__contour = contour
        
    def get_segmented_volume(self):
        return self.__vol_segmented
    
    def __create_segmented_volume(self,vol):
        vol_segmented = itk.Image[itk.UC,3].New()
        
        vol_segmented_region = itk.ImageRegion[3]()
        vol_segmented_region.SetSize(vol.GetOutput().GetLargestPossibleRegion().GetSize())
        vol_segmented_region.SetIndex((0,0,0))
        
        vol_segmented.SetRegions(vol_segmented_region)
        vol_segmented.SetSpacing(vol.GetOutput().GetSpacing())
        vol_segmented.SetOrigin(vol.GetOutput().GetOrigin())
        vol_segmented.SetDirection(vol.GetOutput().GetDirection())
        vol_segmented.Allocate()
        
        return vol_segmented
    
    def __create_slice_contour_table(self,contour):
        slice_contour_table = {}
        
        for idx in xrange(len(contour)):
            coord_3D = contour[idx]
            coord_x = coord_3D[0]
            coord_y = coord_3D[1]
            coord_z = coord_3D[2]
            
            if slice_contour_table.has_key(coord_z):
                val = slice_contour_table[coord_z]
                val.append((coord_x,coord_y))
                slice_contour_table[coord_z] = val
            else:
                slice_contour_table[coord_z] = [(coord_x,coord_y)]
            
        return slice_contour_table  
     
    def __extract_slice_contour(self,slice_contour_table,slice_id):
        slice_contour = []
        
        if slice_contour_table.has_key(slice_id):
            slice_contour = slice_contour_table[slice_id]
        
        return slice_contour
    
    def __is_counter_clockwise(self,polygon):
        number = len(polygon)
        k = 0
        
        for i in xrange(1,number):
            if (polygon[i][0] <= polygon[k][0]) and (polygon[i][0] < polygon[k][0]) or (polygon[i][1] < polygon[k][1]):
                k = i
                
        prev_idx = k-1
        next_idx = k+1
        
        if prev_idx == -1:
            prev_idx = number-1
            
        if next_idx == number:
            next_idx = 0
            
        # form two vectors
        vector_Ax = polygon[k][0] - polygon[prev_idx][0]
        vector_Ay = polygon[k][1] - polygon[prev_idx][1]
        vector_Bx = polygon[next_idx][0] - polygon[prev_idx][0]
        vector_By = polygon[next_idx][1] - polygon[prev_idx][1]
        
        # calculate cross product 2*area if contour_clockwise or -2*area if clockwise
        cross_prod = (vector_Ax*vector_By) - (vector_Ay*vector_Bx)
        
        if cross_prod > 0:
            return False
        
        return True
        
    
    def __make_clockwise(self,polygon):
        if self.__is_counter_clockwise(polygon) == False:
            return polygon
        
        for i in xrange(len(polygon)):
            point = polygon[i]
            polygon.insert(0,point)
            del polygon[i+1]
            
        return polygon
    
    def __det(self,x1,x2,x3,y1,y2,y3):
        return (x1-x3)*(y2-y3)-(x2-x3)*(y1-y3)
    
    def __point_in_polygon(self,point_x,point_y,polygon):
        eps = 1e-12
        isnear = False
        j = 0
             
        polygon_clockwise = self.__make_clockwise(polygon)
        
        number = len(polygon_clockwise)
        
        x = []
        y = []
        
        for i in xrange(number):
            x.append(polygon_clockwise[i][0])
            y.append(polygon_clockwise[i][1])
            
        x.append(x[0])
        x.append(x[1])
        y.append(y[0])
        y.append(y[1])
        
        minimum_distance_squared = 2**16-1
        
        # loop over each side defining the polygon_clockwise
        for i in xrange(number):
            x1 = x[i]
            y1 = y[i]
            x21 = x[i+1]-x1
            y21 = y[i+1]-y1
            x1p = x1-point_x
            y1p = y1-point_y
            
            t = -(x1p*x21 + y1p*y21)/float(x21*x21 + y21*y21)
            
            if t < 0.0:
                d = x1p*x1p + y1p*y1p
                if d < minimum_distance_squared:
                    isnear = False
                    minimum_distance_squared = d
                    j = i
                    
            elif t < 1.0 or t == 1.0:
                dx = x1p + t*x21
                dy = y1p + t*y21
                d = dx*dx + dy*dy
                if d < minimum_distance_squared:
                    isnear = True
                    minimum_distance_squared = d
                    j = i
                        
        minimum_distance = math.sqrt(minimum_distance_squared)
        
        if minimum_distance < eps:
            minimum_distance = 0.0
        elif isnear:
            area = self.__det(x[j],x[j+1],point_x,y[j],y[j+1],point_y)
            if area > 0.0 or area == 0.0:
                minimum_distance = abs(minimum_distance)
            else:
                minimum_distance = -abs(minimum_distance)
        else:
            if j == 0:
                j = number
                
            area = self.__det(x[j+1],x[j],x[j-1],y[j+1],y[j],y[j-1])
            if area > 0.0:
                minimum_distance = abs(minimum_distance)
            else:
                minimum_distance = -abs(minimum_distance)
                
        return minimum_distance
                
    def __fill_slice_contour(self,slice_contour,slice_id):
        for i in xrange(self.__vol_size[0]):
            for j in xrange(self.__vol_size[1]):
                if len(slice_contour) == 0:
                    self.__vol_segmented.SetPixel((i,j,slice_id),0)
                else:
                    min_dist = self.__point_in_polygon(i, j, slice_contour)
                    
                    if min_dist >= 0:
                        self.__vol_segmented.SetPixel((i,j,slice_id),1)
                    else:
                        self.__vol_segmented.SetPixel((i,j,slice_id),0)


    def execute(self):
        self.__vol_size = self.__vol.GetOutput().GetLargestPossibleRegion().GetSize()
        
        self.__vol_segmented = self.__create_segmented_volume(self.__vol)
        
        self.__slice_contour_table = self.__create_slice_contour_table(self.__contour)
        
        print(self.__slice_contour_table)
        
        for k in xrange(self.__vol_size[2]):
            # extract contour in this slice
            slice_contour = self.__extract_slice_contour(self.__slice_contour_table, k)
            # fill slice contour
            self.__fill_slice_contour(slice_contour, k)
    
    