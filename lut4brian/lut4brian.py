from brian2 import *
import os

def lutinit():
    """
    It generates lut4brian.c file with all required constants
    for cpp and cython target.
    It requires to have 4 module variables:
        tbl  - 2d table: number_fo_tabulated_curves x number_of_point_along_index_variable
        Xmin - minimal value of index variable which corresponds to 0 column of lookup table
        Xmax - maximal value of index variable which corresponds to -1 column of lookup table
        dX   - change in index variable.
    """
    M,N = tbl.shape
    with open("lut4brian.c","w") as fd:
        fd.write(f"const double lutXmin  = {Xmin};\n")
        fd.write(f"const double lutXmax  = {Xmax};\n")
        fd.write(f"const double lutdX    = {dX};\n")
        fd.write(f"const int    lutTSize = {N-1};\n")
        fd.write(f"const double luttbl[{M}][{N}] = {{"+"\n")
        for cid in range(M):
            fd.write("   {")
            for x in range(N):
                fd.write(f"{tbl[cid,x]}"+("," if x != N-1 else "}") )
            fd.write(",\n" if cid != M-1 else "\n")
        fd.write("};\n")

@implementation('cpp', '''
#include <lut4brian.c>;
double lutinterpol(double x, int cid){
    if (x >= lutXmax) return luttbl[cid][lutTSize];
    if (x <= lutXmin) return luttbl[cid][       0];
    x     -= lutXmin          ;
    int idx0 = (int)(x/lutdX) ;
    int idx1 = idx0 + 1       ;
    return luttbl[cid][idx0] + (luttbl[cid][idx1]-luttbl[cid][idx0])*(x/lutdX - (double)idx0);
}
''',include_dirs=[os.getcwd()])
@implementation('cython',f'''
cdef extern from "{os.getcwd()}/lut4brian.c":
    const double lutXmin, lutXmax, lutdX
    const int    lutTSize
    const double **luttbl
cdef double lutinterpol(double x, int cid):
    if x >= lutXmax    : return luttbl[cid][lutTSize]
    if x <= lutXmin    : return luttbl[cid][       0]
    x    -= lutXmin
    cdef int idx0 = int(x/lutdX)
    cdef int idx1 = idx0 + 1
    return luttbl[cid][idx0] + (luttbl[cid][idx1]-luttbl[cid][idx0])*(x/lutdX - float(idx0))
''',include_dirs=[os.getcwd()])
@check_units(arg=[1,1], result=1)
def lutinterpol(x,cid):
    """
    Interpolate between rows of a table
    It requires to have 4 module variables:
        tbl  - 2d numpy array: number_fo_tabulated_curves x number_of_point_along_index_variable
        Xmin - minimal value of index variable which corresponds to 0 column of lookup table
        Xmax - maximal value of index variable which corresponds to -1 column of lookup table
        dX   - change in index variable.
    Inputs:
        x    - tabulated variable (for example voltage)
        cid  - curve index
    
    """
    def sigle (x,cid):
        if x >= Xmax    : return tbl[cid,-1]
        if x <= Xmin    : return tbl[cid, 0]
        x    = x-Xmin
        idx0 = int(x/dX)
        idx1 = idx0 + 1
        return tbl[cid,idx0] + (tbl[cid,idx1]-tbl[cid,idx0])*(x/dX - float(idx0))
    return array([ sigle(y,cid) for y in x ])
