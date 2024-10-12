from double_functions import Piecewise_dérivabilité, get_piecewise_function_info,continuité,get_boundary_point
from sympy import oo

expr,fulldomain,subdomain1,subdomain2=get_piecewise_function_info(
    function1="x",         
    function1_a=-oo,         
    function1_b=-2,         
    function2="x",     
    function2_a=-2,         
    function2_b=oo          
    )
print(f"debug:{type(expr)}")