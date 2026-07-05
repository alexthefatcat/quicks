

def get_line_function_from_two_points(point_a,point_b):
    point_c = ((point_a[0]+point_b[0])/2,(point_a[1]+point_b[1])/2)
    m = (point_a[1] - point_b[1]) / (point_a[0] - point_b[0])
    m_inv = -1/m
    c = point_c[1]- (m*point_c[0])
    c_inv = point_c[1]- (m_inv*point_c[0])
    def func(x=None, y=None, inverse=False):
        m0,c0 = m,c
        if inverse:        m0,c0 = m_inv,c_inv 
        if x is not None:  return m0*x+c0
        if y is not None:  return (y-c0)/m0
        return point_c, (m, c), (m_inv, c_inv)
    return func


def draw_line(img, point_a, point_b, just_between=True):
    func = get_line_function_from_two_points(point_a,point_b) 
    axis = int(func(0)>0)
    locs = (point_a[0], point_b[0]) if just_between else (0, img.shape[0])
    points = [ (iz, func(x=iz)) if axis else (func(y=iz), iz) for iz in range(*sorted(locs))]         
    for ix,iy in points:    
        img[round(ix), round(iy)] = 1    