import bpy
import math
import bmesh




## L3D.py (module 'L3D') Version 1.05
## Copyright (c) 2006 Bruce Vaughan, BV Detailing & Design, Inc.
## All rights reserved.
## NOT FOR SALE. The software is provided "as is" without any warranty.
################################################################################
from math import pi, sqrt, acos, cos, sin
#from point import Point
################################################################################
## Point ########################################
class Point(object):
    '''
    p1 = Point(1,2,3)
    Point(1.000000, 2.000000, 3.000000)
    attributes: x, y, z, data
    methods: dot(), cross(), mag(), uv(), dist(), format(), fformat(), equiv(), eq()
    '''
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.data = (self.x, self.y, self.z)
        # cannot pickle bool objects in Python 2.3 (True, False)
        self.__init = 1
       
    def __str__(self):
        return '(%0.4f, %0.4f, %0.4f)' % self.data
 
    def __repr__(self):
        return 'Point(%f, %f, %f)' % self.data
 
    def format(self):
        return 'Point(%s, %s, %s)' % tuple(map(fifDim, self))
 
    def fformat(self):
        return '%0.4f, %0.4f, %0.4f' % tuple(self)   
 
    '''
    Operator overloading
    'other' can be a Point object, tuple or list.
    'f' can be an integer or float except as noted.
    '''   
   
    def __add__(self, other):
        # return Point(*[a+b for a,b in zip(self,other)])
        # following code is more efficient
        return Point(self.x+other[0], self.y+other[1], self.z+other[2])
 
    def __iadd__(self, other):
        return Point(self.x+other[0], self.y+other[1], self.z+other[2])
 
    def __radd__(self, other):
        return Point(other[0]+self.x, other[1]+self.y, other[2]+self.z)   
   
    def __sub__(self, other):
        return Point(self.x-other[0], self.y-other[1], self.z-other[2])
 
    def __isub__(self, other):
        return Point(self.x-other[0], self.y-other[1], self.z-other[2])
 
    def __rsub__(self, other):
        return Point(other[0]-self.x, other[1]-self.y, other[2]-self.z)      
   
    def __mul__(self, f):
        return Point(self.x*f, self.y*f, self.z*f)
 
    def __imul__(self, f):
        return Point(self.x*f, self.y*f, self.z*f)
 
    def __div__(self, f):
        return Point(self.x/f, self.y/f, self.z/f)
 
    def __imul__(self, f):
        return Point(self.x/f, self.y/f, self.z/f)
 
    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)
 
    def __pow__(pt, pwr):
        return Point(pt.x**pwr, pt.y**pwr, pt.z**pwr)
 
    def __iter__(self):
        '''
        Point iteration:
            for a in pt:
                print a,
        Prints:
            pt.x pt.y pt.z
        '''
        for i in self.data:
            yield i
 
    def __getitem__(self, i):
        return self.data[i]
 
    def __setitem__(self, i, value):
        try:
            object.__setattr__(self, {0:'x',1:'y',2:'z'}[i], float(value))
            object.__setattr__(self, 'data', (float(self.x), float(self.y), float(self.z)))
        except KeyError:
            #raise IndexError, "Index argument out of range in '%s' __setitem__" % (type(self).__name__)
            print('raise IndexError, "Index argument out of range in %s __setitem__" % (type(self).__name__)')
        except ValueError:
            #raise ValueError, "Invalid literal in '%s' __setitem__" % (type(self).__name__)    
            print('raise ValueError, "Invalid literal in %s __setitem__" % (type(self).__name__)')

# TODO: switch to 'keyname' in dictionary
#    def __setattr__(self, name, value):
#        if not self.__dict__.has_key('_Point__init'):
#            return object.__setattr__(self, name, value)
#        elif self.__dict__.has_key(name):
#            object.__setattr__(self, name, value)
#            object.__setattr__(self, 'data', (float(self.x), float(self.y), float(self.z)))
#        else:
            #raise AttributeError, "'%s' object has no attribute '%s'" % (type(self).__name__, name)
#            print('raise AttributeError, "%s object has no attribute %s" % (type(self).__name__, name)')
 
    def __cmp__(self, other, epsilon=0.000001):
        x = abs(self.x-other.x)
        if x < epsilon:
            y = abs(self.y-other.y)
            if y < epsilon:
                return cmp(self.z, other.z)
            return cmp(self.y, other.y)
        return cmp(self.x, other.x)
       
    def dot(self, other):
        '''
        Return the dot product of two Points (self, other)
        'other' must be a Point object
        '''
        # return sum([a*b for a,b in zip(self,other)])
        return (self.x*other.x + self.y*other.y + self.z*other.z)
   
    def uv(self):
        '''
        Return the unit vector of a Point object.
        If vector has no magnitude, returns Point(0,0,0).
        '''
        m = self.mag()
        try: return Point(self.x/m, self.y/m, self.z/m)
        except: return Point()
   
    def cross(self, other):
        '''
        Return the cross product of two Points (self, other)
        'other' must be a Point object
        '''
        return Point(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
   
    def mag(self):
        '''
        Return the scalar length of a Point instance vector
        '''
        return (self.x**2 + self.y**2 + self.z**2)**0.5   
 
    def dist(self, other):
        '''
        Return the scalar distance between two Points (self, other)
        'other' can be a Point object, list or tuple
        '''
        # return sum((self-other)**2)**0.5
        p = self-other
        return (p.x**2 + p.y**2 + p.z**2)**0.5
 
    def equiv(self, other, epsilon=0.000001):
        '''
        Compare two vectors, return a tuple of 1, 0, or -1 values
        Interactive example:
        >>> Point(1,1,5).equiv(Point(2,0,5))
        (-1, 1, 0)
        >>>
        '''
        def comp(x,y):
            if abs(x-y) < epsilon: return 0
            elif x > y: return 1
            else: return -1
        return tuple(map(comp, self, other))
 
    def eq(self, other):
        '''
        Wrapper for equiv() method
        If the points/vectors are equal or equivalent, return True
        Otherwise, return False
        >>> p11 = Point(10,10,10)
        >>> p12 = Point(1,1,1)
        >>> p11.uv().eq(p12.uv())
        True
        >>> p11.eq(p12)
        False
        >>>
        '''
        a = self.equiv(other)
        if 1 in a or -1 in a:
            return False
        return True
"""
    LineLineIntersect3D (class) - Determine information about the intersection of two line segments in 3D space
    DistancePointLine3D (class) - Determine information about the relationship between a line segment and a point in 3D space
    ret_WP (class) - Return the WP on member 1 and which end of member 2 coincides

    Revision History:
        Version 1.02 - Add attributes obj.Pa and obj.Pb to a DistancePointLine3D instance
        Version 1.03 (10/30/06) - Rework calculation of self.position
                                  Consolidate comments
                                  add function ret_WP
        Version 1.04 (11/16/06) - Rework LineLineIntersect3D - solve using like triangles
        Version 1.05 (11/17/06) - Rework LineLineIntersect3D - solve for unknowns by substitution

    Reference 'The Shortest Line Between Two Lines in 3D' - Paul Bourke   
"""
# end class definition
###############################################################################
class LineLineIntersect3D:        
    def __init__(self, p1, p2, p3, p4):
        #from param import Warning
        """                                                                                                                       <-->     <-->
            Calculate the points in 3D space Pa and Pb that define the line segment which is the shortest route between two lines p1p2 and p3p4.
            Each point occurs at the apparent intersection of the 3D lines.
            The apparent intersection is defined here as the location where the two lines 'appear' to intersect when viewed along the line segment PaPb.
            Equation for each line:
            Pa = p1 + ma(p2-p1)
            Pb = p3 + mb(p4-p3)
            
            Pa lies on the line connecting p1p2.
            Pb lies on the line connecting p3p4.

            The shortest line segment is perpendicular to both lines. Therefore:
            (Pa-Pb).(p2-p1) = 0
            (Pa-Pb).(p4-p3) = 0

            Where:            
            '.' indicates the dot product            

            A = p1-p3
            B = p2-p1
            C = p4-p3

            Substituting:
            (A + ma(B) - mb(C)).B = 0       &       (A + ma(B) - mb(C)).C = 0
            -----------------------------------------------------------------
            A.B + ma(B.B) - mb(C.B) = 0
            A.B + ma(B.B) - (ma(C.B)-A.C)/C.C)(C.B) = 0
            ma(B.B)(C.C) - ma(C.B)(C.B) = (A.C)(C.B)-(A.B)(C.C)
            ma = ((A.C)(C.B)-(A.B)(C.C))/((B.B)(C.C) - (C.B)(C.B))
            mb = (A.B + ma(B.B))/(C.B)

            If the cross product magnitude of the two lines is equal to 0.0, the lines are parallel.          
                                                                                                                                                 <-->
            A line extends forever in both directions. The name of a line passing through two different points p1 and p2 would be "line p1p2" or p1p2.                                           
            The two-headed arrow over p1p2 signifies a line passing through points p1 and p2.

            Two lines which have no actual intersection but are not parallel are called 'skew' or 'agonic' lines. Skew lines can only exist in
            three or more dimensions.

            Determine whether the apparent intersection point lies between the line segment end points or beyond one of the line segment end points.
            This information is to be used to evaluate the framing condition of mem1 (p1p2).
            Convention for members:
                p1p2 - mem1.left.location, mem1.right.location
                p3p4 - mem2.left.location, mem2.right.location
                
            Set a keyword indicating the apparent intersection point position with respect to the line segment end points p1 and p2 as follows:
                'LE' indicates the apparent intersection point occurs at p1 (within fudge_factor distance)
                'RE' indicates the apparent intersection point occurs at p2 (within fudge_factor distance)
                'Beyond LE' indicates the apparent intersection point occurs beyond p1
                'Beyond RE' indicates the apparent intersection point occurs beyond p2
                'Not Beyond LE' indicates the apparent intersection point occurs in between p1 and p2 and is closer to p1
                'Not Beyond RE' indicates the apparent intersection point occurs in between p1 and p2 and is closer to p2
            Calculate the magnitude and direction (beam member 'X' distance) the apparent intersection point occurs from line segment p1p2 end points.
        """
        def cross_product(p1, p2):
            return Point(p1.y*p2.z - p1.z*p2.y, p1.z*p2.x - p1.x*p2.z, p1.x*p2.y - p1.y*p2.x)

        def dot_product(p1, p2):
            return (p1.x*p2.x + p1.y*p2.y + p1.z*p2.z)

        def mag(p):
            return sqrt(p.x**2 + p.y**2 + p.z**2)        

        def normalise(p1, p2):
            p = p2 - p1
            m = mag(p)
            if m == 0:
                return Point(0.0, 0.0, 0.0)
            else:
                return Point(p.x/m, p.y/m, p.z/m)

        def ptFactor(p, f):
            return Point(p.x*f, p.y*f, p.z*f)

        A = p1-p3
        B = p2-p1
        C = p4-p3

        # Line p1p2 and p3p4 unit vectors
        self.uv1 = normalise(p1, p2)
        self.uv2 = normalise(p3, p4)        

        # Check for parallel lines
        self.cp12 = cross_product(self.uv1, self.uv2)
        self._cp12_ = mag(self.cp12)

        if round(self._cp12_, 6) != 0.0:         
            ma = ((dot_product(A, C)*dot_product(C, B)) - (dot_product(A, B)*dot_product(C, C)))/ \
                 ((dot_product(B, B)*dot_product(C, C)) - (dot_product(C, B)*dot_product(C, B)))
            mb = (ma*dot_product(C, B) + dot_product(A, C))/ dot_product(C, C)
            
            # Calculate the point on line 1 that is the closest point to line 2
            Pa = p1 + ptFactor(B, ma)
            self.Pmem1 = Pa
            
            # Calculate the point on line 2 that is the closest point to line 1
            Pb = p3 + ptFactor(C, mb)
            self.Pmem2 = Pb
            
            # Distance between lines            
            self.inters_dist = Pa.dist(Pb)
            
            if round(ma, 3) >= 0.0 and round(ma, 3) <= 1.0:
                self.on_segment1 = 1
                xl_dir = 1
                xr_dir = -1
                if round(ma, 2) == 0.0:
                    self.position = "LE" # apparent intersection is at p1
                elif round(ma, 2) == 1.0:
                    self.position = "RE" # apparent intersection is at p2
                    xr_dir = 1
                    xl_dir = 1
                elif ma <= 0.5:
                    self.position = "Not Beyond LE" # apparent intersection is closer to p1
                elif ma > 0.5:
                    self.position = "Not Beyond RE" # apparent intersection is closer to p2
                else:
                    #Warning('self.position calculation error, self.on_segment = 1')
                    print("Warning('self.position calculation error, self.on_segment = 1'")
                    raise ValueError
            else:
                self.on_segment1 = 0
                if ma < 0.0:
                    self.position = "Beyond LE" # apparent intersection is beyond p1
                    xl_dir = -1
                    xr_dir = -1
                elif ma > 0.0:
                    self.position = "Beyond RE" # apparent intersection is beyond p2
                    xl_dir = 1
                    xr_dir = 1
                else:
                    #Warning('self.position calculation error, self.on_segment = 0')
                    print("Warning('self.position calculation error, self.on_segment = 0'")
                    raise ValueError

            # Set the member 'X' direction with respect to p1 and p2 - either '+' or '-'
            self.left_dist = round(Pa.dist(p1)*xl_dir, 8)
            self.right_dist = round(Pa.dist(p2)*xr_dir, 8)                

            if round(mb, 3) >= 0.0 and round(mb, 3) <= 1.0:
                self.on_segment2 = 1
            else:
                self.on_segment2 = 0
            
            # Calculate the unit vector of PaPb
            if round(self.inters_dist, 4) > 0.0:
                self.uv = normalise(Pb, Pa)
            else:
                self.uv = Point(0.0, 0.0, 0.0)
                
        # Lines are parallel
        else:
            self.Pmem1 = None
            self.Pmem2 = None
            self.inters_dist = None
            self.left_dist = None
            self.right_dist = None
            self.uv = None

    # Return False if lines are parallel, and return True if lines are not parallel        
    def not_parallel(self):
        if round(self._cp12_, 5) != 0.0:
            return True
        else:
            return False 
# end class definition
###############################################################################
class Plane3D:
    
    def cross_product(self, p1, p2):
        return Point(p1.y*p2.z - p1.z*p2.y, p1.z*p2.x - p1.x*p2.z, p1.x*p2.y - p1.y*p2.x)

    def dot_product(self, p1, p2):
        return (p1.x*p2.x + p1.y*p2.y + p1.z*p2.z)    
    
    def plane_def(self, p1, p2, p3):
        N = self.cross_product(p2-p1, p3-p1)
        A = N.x
        B = N.y
        C = N.z
        D = self.dot_product(-N, p1)
        return N, A, B, C, D
        
    def __init__(self, p1, p2, p3, theta1 = 0):
        
        def chk_type(p_list):
            ret_list = []
            for p in p_list:
                if type(p) == type(Point(0,0,0)):
                    ret_list.append(True)
                else:
                    ret_list.append(None)
            return ret_list
        
        if None not in chk_type([p1, p2, p3]):
            """
            /// Define a plane from 3 non-collinear points
            /// Ax + By + Cz + D = 0
            /// The normal 'N' to the plane is the vector (A, B, C)
            """
            self.N, A, B, C, self.D = self.plane_def(p1, p2, p3)
            self.N_len = round(sqrt(A*A + B*B + C*C), 6)
            if self.N_len > 0.0:
                self.N_uv = Point(self.N.x/self.N_len, self.N.y/self.N_len, self.N.z/self.N_len)
            else:
                self.N_uv = Point(0.0, 0.0, 0.0)
            # make p1 global to class namespace
            self.p1 = p1
            """
            /// If vector N is the normal to the plane then all points 'p' on the plane satisfy the following:
            /// N dot p = k where 'dot' is the dot product
            /// N dot p = N.x*p.x + N.y*p.y + N.z*p.z
            """
            self.k = round(self.dot_product(self.N, p1), 6)             # calculation of plane constant 'k'
            self.k0 = round(self.dot_product(self.N_uv, p1), 6)         # displacement of the plane from the origin
            """
            /// Determine vector e and unit vector e0 (p1 to p3)
            /// Determine vector d and unit vector d0 (p1 to p2)
            /// Determine location of point F, midpoint on vector d
            /// Determine location of point G, midpoint on vector e
            """
            e = p3 - p1
            e_len = (sqrt(e.x**2 + e.y**2 + e.z**2))
            if e_len > 0.0:
                self.e0 = Point(e.x/e_len, e.y/e_len, e.z/e_len)
            else:
                self.e0 = Point(0.0, 0.0, 0.0)
            d = p2 - p1
            d_len = (sqrt(d.x**2 + d.y**2 + d.z**2))
            if d_len > 0.0:
                self.d0 = Point(d.x/d_len, d.y/d_len, d.z/d_len)
            else:
                self.d0 = Point(0.0, 0.0, 0.0) 
            self.F = Point(p1.x + (d.x/2), p1.y + (d.y/2), p1.z + (d.z/2))
            self.G = Point(p1.x + (e.x/2), p1.y + (e.y/2), p1.z + (e.z/2))
            # Make variables 'e' and 'd' available as attributes
            self.e = e
            self.d = d
            
            # Calculate distance between points p1 and p2
            self.Ra = p2.dist(p1)

            """
            /// Calculate net angle between vectors d0 and e0 (Q)
            /// Radius = self.Ra
            /// Calculate point to point distance (pp)
            """
            if abs(theta1) == pi:
                self.Q = theta1
            else:
                self.Q = acos(self.dot_product(self.d0, self.e0))   # radians
            self.pp = abs(self.Q * self.Ra)            

        else:
            #raise TypeError, 'The arguments passed to Plane3D must be a POINT'
            print ("raise TypeError, 'The arguments passed to Plane3D must be a POINT'")
        
    # Calculate points to define plane #2 and calculate N2 and d2
    def plane_2(self):
        p1 = self.G
        p2 = self.G + self.N_uv
        p3 = self.G + self.cross_product(self.e0, self.N_uv)
        N, A, B, C, D = self.plane_def(p1, p2, p3)
        d = round(sqrt(A*A + B*B + C*C), 6) 
        self.N2 = Point(A/d, B/d, C/d)
        self.d2 = round(self.N2.x*p1.x + self.N2.y*p1.y + self.N2.z*p1.z, 6)
        
    def plane_2(self, p1b, p2b, p3b, theta1b = 0):
        Nb, Ab, Bb, Cb, Db = self.plane_def(p1b, p2b, p3b)
        db = round(sqrt(Ab*Ab + Bb*Bb + Cb*Cb), 6) 
        self.N2 = Point(Ab/db, Bb/db, Cb/db)
        self.d2 = round(self.N2.x*p1b.x + self.N2.y*p1b.y + self.N2.z*p1b.z, 6)
                    
    # Calculate points to define plane #3 and calculate N3 and d3
    def plane_3(self):
        p1 = self.F
        p2 = self.F + self.N_uv
        p3 = self.F + self.cross_product(self.d0, self.N_uv)
        N, A, B, C, D = self.plane_def(p1, p2, p3)
        d = round(sqrt(A*A + B*B + C*C), 6)
        self.N3 = Point(A/d, B/d, C/d)
        self.d3 = round(self.N3.x*p1.x + self.N3.y*p1.y + self.N3.z*p1.z, 6)

    def plane_3(self, p1c, p2c, p3c, theta1c = 0):
        Nc, Ac, Bc, Cc, Dc = self.plane_def(p1c, p2c, p3c)
        dc = round(sqrt(Ac*Ac + Bc*Bc + Cc*Cc), 6) 
        self.N3 = Point(Ac/dc, Bc/dc, Cc/dc)
        self.d3 = round(self.N2.x*p1c.x + self.N2.y*p1c.y + self.N2.z*p1c.z, 6)
        
    def three_pt_circle (self):     
        """
        /// The intersection of three planes is either a point, a line, or there is no intersection.
        /// Three planes can be written as:
        /// N1 dot p = d1
        /// N2 dot p = d2
        /// N3 dot p = d3
        /// 'Nx' is the normal vector
        /// 'p' is a point on the plane
        /// 'dot' signifies the dot product of 'Nx' and 'p'
        /// 'dx' = plane constant (displacement of the plane from the origin if Nx is a unit vector)
        /// The intersection point of the three planes "M" is given by:
        /// M = (d1*(N2 cross N3) + d2(N3 cross N1) + d3*(N1 cross N2)) / (N1 dot (N2 cross N3))
        /// 'cross' indicates the cross product and 'dot' indicates the dot product
        /// Calculate the center point of the circle (intersection point of three planes) and the radius.
        /// Plane 1 is defined in __init__ method.
        """
        # Define Plane 2
        self.plane_2()
        # Define Plane 3
        self.plane_3()
        
        N23 = self.cross_product(self.N2, self.N3)
        N31 = self.cross_product(self.N3, self.N)
        N12 = self.cross_product(self.N, self.N2)
        NdN23 = round(self.dot_product(self.N, N23), 6)

        numer = Point(self.k*N23.x, self.k*N23.y, self.k*N23.z) + (self.d2*N31.x, self.d2*N31.y, self.d2*N31.z) + \
                     (self.d3*N12.x, self.d3*N12.y, self.d3*N12.z)
        if NdN23 != 0.0:
            self.M = Point(numer.x/NdN23, numer.y/NdN23, numer.z/NdN23)
            self.R = self.M.dist(self.p1)
        else:
            self.M = Point(0.0, 0.0, 0.0)
            self.R = 0.0

    """
    /// Rotate point p about a line passing through self.p1 and normal to the current plane by the angle 'theta' in radians
    /// Return the new point
    """    
    def PointRotate3D(self, p, theta):
        # Initialize point q
        q = Point(0.0,0.0,0.0)
        # Rotation axis unit vector
        n = self.N_uv
        # Translate so axis is at origin
        p = p - self.p1

        # Matrix common factors     
        c = cos(theta)
        t = (1 - cos(theta))
        s = sin(theta)
        X = n.x
        Y = n.y
        Z = n.z

        # Matrix 'M'
        d11 = t*X**2 + c
        d12 = t*X*Y - s*Z
        d13 = t*X*Z + s*Y
        d21 = t*X*Y + s*Z
        d22 = t*Y**2 + c
        d23 = t*Y*Z - s*X
        d31 = t*X*Z - s*Y
        d32 = t*Y*Z + s*X
        d33 = t*Z**2 + c

        #            |p.x|
        # Matrix 'M'*|p.y|
        #            |p.z|
        q.x = d11*p.x + d12*p.y + d13*p.z
        q.y = d21*p.x + d22*p.y + d23*p.z
        q.z = d31*p.x + d32*p.y + d33*p.z
        
        # Translate axis and rotated point back to original location
        return q + self.p1

    def lie_check(self, p):
        """
        /// Given any point 'a' on a plane: N dot (a-p) = 0
        """
        return round(self.dot_product(self.N, (p - self.p1)))

# end function definition
###############################################################################
def support_column_fast(x1, y1, z1, x2, y2, z2, strut_radius, faces):

    # Add a cylinder from centre of the face to the baseplate

    cone_radius = 1
    cone_height = 1

    coords = (mw @ f.calc_center_median() for f in bm.faces if f.select)
    bm = bmesh.new()
    for co in coords:
        print(co)
        bm.clear()
        cone_mesh = bpy.data.meshes.new("Base")    
        bmesh.ops.create_cone(
                bm,
                segments=16,
                diameter1=cone_radius,
                depth=cone_height,
                cap_ends=True,
                cap_tris=True, # tri fan fill.
                matrix=Matrix.Translation((0, 0, cone_height/2))
                )
        bm.to_mesh(cone_mesh)        
        cone = bpy.data.objects.new("Base", cone_mesh)
        cone.location = (co.x, co.y, 0)
        coll.objects.link(cone)
            
        bm.clear()
        strut_mesh = bpy.data.meshes.new("Strut")
        
        bmesh.ops.create_cone(
                bm,
                segments=3,
                diameter1=strut_radius,
                diameter2=strut_radius,
                depth=co[2],
                cap_ends=True,
                matrix=Matrix.Translation((0, 0, co[2] / 2)),
                )
        bm.to_mesh(strut_mesh)        
        strut = bpy.data.objects.new("Strut", strut_mesh)
        strut.location = (co.x, co.y, 0)
        coll.objects.link(strut)



def support_column(x1, y1, z1, x2, y2, z2, r, faces):

    # Add a cylinder from centre of the face to the baseplate
    #This is more complex than needed currently but will support variable orientations in the future
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=faces,
        radius = r, 
        depth = dist,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 

    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi
    
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections['AutoSupports'].objects.link(obj)

    # Now add the cone at the base    
    bpy.ops.mesh.primitive_cone_add(
        depth=dist/10, 
        location=(x2, y2, z2),
        scale=(1, 1, 1),
        )
    obj = bpy.context.active_object
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections['AutoSupports'].objects.link(obj)


def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene (not currently required as linked to autosupports elsewhere)
    #bpy.context.scene.collection.objects.link( ob )
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
    return ob
 

def support_interface(worldCoords, face, maxAngle, supportLoc):
    #print()
    #print("NEW FACE")
    (wX,wY,wZ) = worldCoords
    
#        face[0] is the centroid calculated by blender
#        face[1] is the list of vertices for the face

    # will create with faces feeding under the centroid
    # This isn't the ideal point as angle from some vertices will be much shallower than required
    centroid = Point(face[0][0], face[0][1], face[0][2])

    # two random points on the z-axis (to get distance from each vertex to z-axis)
    pZ1 = Point(0,0,-1000)
    pZ2 = Point(0,0,1000)   

    print("")
    print("Starting New Face Calculation")
    if len(face[1]) != 3:
        print("ERROR: this function will not work unless faces have exactly 3 edges")
        print("Function will ignore this face until script is updated to handle this")
        return

    print("Using vertices:-")
    # convert the vertices to Points for looping
    vertices = []
    for vert in face[1]:
        # Converting to world coordinates isn't required, but makes it easier to bug check
        #newV = Point (vert.co[0]+wX, vert.co[1]+wY, vert.co[2]+wZ)
        newV = Point (vert.co[0], vert.co[1], vert.co[2])
        vertices.append(newV)
        print(newV.x,newV.y,newV.z)
        if (newV.x == 0 and newV.y == 0):
            print("ERROR: this function can not currently identify the plane if an edge hits the z-axis (eg if a vertex is on zero)")
            print("Function will ignore this face until script is updated to support this")
            return


    # now loop through each edge and identify the z-intercept in order to generate the 3 points to define the plane
    # add the plane generated to the list of planes
    planes = []
    maxV = len(vertices)
    for v in range(maxV):
        p1 = vertices[v]
        if v < maxV-1:
            p2 = vertices[v+1]
        else:
            p2 = vertices[0]
            
        # identify the intersection of the lines
        #The dot product of the line defined by the two points with the z-axis allow us to calculate that
        # Blender can do this step
        # mathutils.geometry.intersect_line_line(v1, v2, v3, v4)
        lli = LineLineIntersect3D(p1,p2,pZ1,pZ2)


        if (lli.uv.x == 0.0 and lli.uv.x == 0.0 and lli.uv.x == 0.0):
            print("ERROR: unit vector has length zero. This means all three points are in a line.")
            print("Thus the x-axis intercept cannot be used to provide the 3rd point of the plane")
            print("Using (1,1,0)->(1,1,1) line instead)")
            lli = LineLineIntersect3D(p1,p2,Point(1,1,0),Point(1,1,1))
            
        print("Calculating plane from p1p2 edge with coordinates of:")
        print(p1)
        print(p2)
        print("UV (unit vector):", lli.uv)
                    
        # the point on p1p2 will be exactly maxAngle from the point the plane intersects the z-axis
        print("Nearest point on p1p2 to z-axis:",lli.Pmem1)
        # the hypotenuse of a horizontal xy triangle becomes the adjacent side for the triangle down to the intercept
        # thus the opposite side (the difference in z-axis height from the current point is Opp = Adj*tan(maxAngle)
        xyHyp = sqrt(lli.Pmem1.x*lli.Pmem1.x + lli.Pmem1.y*lli.Pmem1.y) 
               
        print("xy hypotenuse = xyz adjacent side:",xyHyp)
        opp = xyHyp * math.tan(maxAngle)
        if opp==0.0:
            print("ERROR: this function will not work for horizontal planes")
            print("Function will ignore this face until script is updated to handle this")
            return            
        print("z intercept should be +/-",opp)
        # now we have two potential intercepts (one above and one below the level of the intersection)
        p3a = Point(0,0,lli.Pmem1.z+opp)
        p3b = Point(0,0,lli.Pmem1.z-opp)
        
        print("zIntercept candidates are:-")     
        print(p3a)
        print(p3b)
   
        
        
        # Now there are four potential normals for the plane. 
        # We need to test which of the two points produces a plane in the coorrect orientation
        # Selecting the normal which is on the same side as one of the other face points and which has uv.z >0 (or it's negative) 
        #   will identify the correct one. 
        # Use the face centron to identify whether the normal is on the same or opposide side of the plane as the face
        #   and whether the normal points up or down (it should point up towards the face or down away)
        print ("Testing plane candidate generated using point p3a")
        planeC = Plane3D(p1, p2, p3a)
        correctPlane = False
        lieCheckA = planeC.lie_check(centroid)

        if lieCheckA == 0.0:
            print("Warning: The face centroid lies on current plane.")
            print("  The face  may be at exactly maxAngle (but if this is the case it shouldn't have been selected for support)")
        elif lieCheckA < 0.0:
            print ("The centroid lies on OPPOSITE side of current plane as normal N.")
            if planeC.N.z < 0:
                print ("The normal N.z points DOWN so this is the correct plane")
                correctPlane = True
                planeC.N = -planeC.N
        else:
            print ("The centroid lies on SAME side of current plane as normal N.")
            if planeC.N.z > 0:
                print ("The normal N.z points UP so this is the correct plane")
                correctPlane = True
                planeC.N = -planeC.N
                
        if not correctPlane:        
            print ("p3a plane didn't meet selection criteria")
            print ("Testing plane candidate generated using  point p3b")
            planeC = Plane3D(p1, p2, p3b)
            correctPlane = False
            lieCheckA = planeC.lie_check(centroid)
            if lieCheckA == 0.0:
                print ("ERROR: The face centroid lies on current plane - THIS SHOULDN'T HAPPEN IF THE PLANE IS CORRECT")
            elif lieCheckA < 0.0:
                print ("The centroid lies on OPPOSITE side of current plane as normal N.")
                if planeC.N.z < 0:
                    print ("The normal N.z points DOWN so this is the correct plane")
                    correctPlane = True
                    planeC.N = -planeC.N
            else:
                print ("The centroid lies on SAME side of current plane as normal N.")
                if planeC.N.z > 0:
                    print ("The normal N.z points UP so this is the correct plane")
                    correctPlane = True
                    planeC.N = -planeC.N
                        
        if not correctPlane:
            print ("ERROR: Neither plane matches - THIS SHOULDN'T HAPPEN IF THE PLANE IS CORRECT")
            return
        else: 
            planes.append(planeC)

        
    # Now we should have three planes we just need to establish the intersect point
    if len(planes) == 3:
        print("3 PLANES IDENTIFIED")
    else:
        print("NEVER EVENT OCCURRED:")
        print("  Number of planes != 3")
        print("  Function will ignore this face until script is updated to handle this")
        return

    # The intersection point of the three planes "M" is given by:
    # M = (d1*(N1 cross N2) + d2*(N2 cross N0) + d3*(N0 cross N1)) / (N0 dot (N1 cross N2))
    # 'cross' indicates the cross product and 'dot' indicates the dot product
    # blender could do this step with:
    # blender could do this with
    # mathutils.geometry.intersect_plane_plane(plane_a_co, plane_a_no, plane_b_co, plane_b_no)
    print("Normals and D coefficients for the three planes are:-")   
    N0 = planes[0].N
    N1 = planes[1].N
    N2 = planes[2].N
    D0 = planes[0].D
    D1 = planes[1].D
    D2 = planes[2].D
    #k0 = round(N0.dot(planes[0].p1), 6)
    #k1 = round(N1.dot(planes[1].p1), 6)
    #k2 = round(N2.dot(planes[2].p1), 6)
    print(N0.x, N0.y, N0.z, "   ", D0)#, "   ", k0)
    print(N1.x, N1.y, N1.z, "   ", D1)#, "   ", k1)
    print(N2.x, N2.y, N2.z, "   ", D2)#, "   ", k2)

    N12 = N1.cross(N2)
    N20 = N2.cross(N0)
    N01 = N0.cross(N1)
    N0dN12 = round(N0.dot(N12), 6)


    print("Original Face Vertices and Centroid are:-")
    for vert in vertices:
        print(vert.x, vert.y, vert.z)
    print(face[0].x, face[0].y, face[0].z, "(=centroid)")


    print("Intersection Point Is:-")    
    # TODO: figure out why Point overloads aren't working
    # M = (D0*N12 + D1*N20 + D2*N01) / N0dN12
    # point overloads not working, so calculate individually first
    D0N12 = Point(N12.x*D0, N12.y*D0, N12.z*D0)    
    D1N20 = Point(N20.x*D1, N20.y*D1, N20.z*D1)    
    D2N01 = Point(N01.x*D2, N01.y*D2, N01.z*D2)    

    CPs = D0N12 + D1N20 + D2N01

            
    M = Point(CPs.x / N0dN12, CPs.y / N0dN12, CPs.z / N0dN12) 
    print(M.x, M.y, M.z)



    x = M.x + wX
    y = M.y + wY
    z = M.z + wZ

    # update the mutables so they're accessible outside the function
#    distanceBelow = 5
    supportLoc[0] = z
#    z = z-distanceBelow
    supportLoc[1] = (x,y,z)
    

    # now create a list with the vertices from the original face + the new vertex
    verts1 = []
    for vert in face[1]:
        verts1.append((vert.co[0] + wX, vert.co[1] + wY, vert.co[2] + wZ))
    faceVertCnt = len(verts1)
    verts1.append((x,y,z))   
    
    #print("faceVertCnt=",faceVertCnt)
    
    faces1 = []
    faces1.append((range(faceVertCnt)))
    faces1.append((0,faceVertCnt-1,faceVertCnt))
    for i in range(0,faceVertCnt-1):
        faces1.append((i+1,i,faceVertCnt))
        
    #print("Verts=",verts1)
    #print("Faces=",faces1)
    obj = createMesh('interface', (0,0,0), verts1, [], faces1)
#    bpy.ops.collection.objects_remove_all()
    bpy.data.collections['AutoSupports'].objects.link(obj)
    return obj



def createSupports():
    supportFaceGap = 0.0
    supportInterfaceOverhangAngle = 45

    supportsMerge = False
    supportType = "SUPPORT_COLUMN"
    supportType = "SUPPORT_IBEAM"
    supportType = "SUPPORT_MOLD"
    supportType = "SUPPORT_WALL"
    supportType = "SUPPORT_AUTO"

    supportColumnDiameter = 0.1
    supportColumnFaces = 3


    ob = bpy.context.object
    if ob is None:
        #print("Please select an object with faces selected to support")
        return()

    #The relevant faces should already have been selected in edit mode
    #The context can be edit or object mode
        
    # Get current context to set back at end
    initialMode = bpy.context.active_object.mode
    initialSelection = bpy.context.selected_objects


    # get current mesh
    current_mesh = bpy.context.object.data

    # create empty bmesh, add current mesh into empty bmesh
    current_bm = bmesh.new()
    current_bm.from_mesh(current_mesh)

    #bpy.ops.object.mode_set(mode = 'EDIT')
    wX =  bpy.context.object.matrix_world[0][3]
    wY =  bpy.context.object.matrix_world[1][3]
    wZ =  bpy.context.object.matrix_world[2][3]




    ##print(wX,wY,wZ)


    selected_faces = []
    for face in current_bm.faces:
        if face.select:
            selected_face_verts = []
            for loop in face.loops:
                #uv = loop[uv_lay].uv
                ##print("Loop UV: %f, %f" % uv[:])
                vert = loop.vert
                ##print("Loop Vert: (%f,%f,%f)" % vert.co[:])
                selected_face_verts.append(vert)
            selected_faces.append([face.calc_center_median(),selected_face_verts])
            #print("\n")

    #Creates a new collection if not testing for existance first
#    if bpy.data.collections["AutoSupports"] == None:
    bpy.context.scene.collection.children.link(bpy.data.collections.new("AutoSupports"))


    #curMode = bpy.ops.object.mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for face in selected_faces:
        # add the direct face support, column and base
#        face[0] is the centroid calculated by blender
#        face[1] is the list of vertices for the face

        supportLoc = [999999, (0,0,0)]         #faceMinZ = 999999
        objSI = support_interface((wX,wY,wZ), face, 45, supportLoc)

        # creates a support column at the centroid
        x = face[0][0] + wX
        y = face[0][1] + wY
        z = face[0][2] + wZ

        # creates a support column centred on the lowest point of the support interface
        x = supportLoc[1][0]
        y = supportLoc[1][1]
        z = supportLoc[1][2]
        
        support_column(x,y,supportLoc[0],x,y,0,supportColumnDiameter/2, supportColumnFaces)        

    # return back to original
    #userSelection.select    
    # bpy.ops.object.mode_set(mode = curMode)  # sadly this doesn't work :-(
    #print (initialMode)
    initialSelection[0].select
    #bpy.ops.object.mode_set(mode = initialMode)


print("")
print("*****************   STARTING NEW RUN    *********************")
createSupports()