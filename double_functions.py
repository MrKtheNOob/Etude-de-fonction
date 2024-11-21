from array import array
from typing import List
from sympy import AccumBounds, Contains,Intersection, Piecewise,latex, limit,symbols, sympify,S,Union,Interval,oo
from sympy.calculus.util import continuous_domain
import sympy
from algorythm import branche_infinie, branche_infinie_sans_oo,dérivabilité, format_domain, is_numeric_string


def format_expression_for_mathjax(expr):
    # Convert the SymPy expression to LaTeX format
    latex_expr = latex(expr)
    # Replace \log with \ln to ensure natural logarithm representation
    latex_expr = latex_expr.replace(r'\log', r'\ln')
    # Return the LaTeX expression wrapped in MathJax delimiters with specified font-size
    return f"<li style='font-size: 3em;'>\\({latex_expr}\\)</li>"

x=symbols("x")
def defined_interval_edges(interval:Interval,interval_style:str):
    match interval_style:
        case "[a,b]":
            return Interval(interval.start,interval.end,left_open=False,right_open=False)
        case "]a,b[":
            return Interval(interval.start,interval.end,left_open=True,right_open=True)
        case "]a,b]":
            return Interval(interval.start,interval.end,left_open=True,right_open=False)
        case "[a,b[":
            return Interval(interval.start,interval.end,left_open=False,right_open=True)
        case _:
            raise ValueError
            
def get_piecewise_function_info(function1:str,function1_a:int, function1_b:int,function2:str ,function2_a: int, function2_b:int,interval_style1,interval_style2):
    # domain of single functions    
        #defining intervals before intersections with the conditions
    interval1=Interval(function1_a,function1_b)
    defined_interval1=defined_interval_edges(interval1,interval_style1)
    interval2=Interval(function2_a,function2_b)
    defined_interval2=defined_interval_edges(interval2,interval_style2)
        #intersections with conditions    
    intersection1=Intersection(continuous_domain(sympify(function1),x,S.Reals),defined_interval1)
    intersection2=Intersection(continuous_domain(sympify(function2),x,S.Reals),defined_interval2)
    print(f"domain of f1(x):{intersection1}")
    print(f"domain of f2(x):{intersection2}")
    double_function_domain=Union(intersection1,intersection2)
    print(f"full domain:{double_function_domain}")
    
    piecewise_function = Piecewise(
    (sympify(function1), Contains(x,Interval(function1_a,function1_b))), 
    (sympify(function2), Contains(x,Interval(function2_a,function2_b)))  
    )
    print(piecewise_function)

    return [piecewise_function,double_function_domain,intersection1,intersection2]

def calculate_domain_and_border_limits2(expr,domain)->List:
    response = []
    limits = {}
    
    # Check if the domain is an interval or union of intervals
    if isinstance(domain, Interval):
        # Single interval
        if domain.left_open:
            if "oo" not in str(domain.start):
                limits[f'limit_at_{domain.start}'] = sympy.limit(expr, x, domain.start, dir='-')
                response.append(f"limite à gauche en {domain.start} : {limits[f'limit_at_{domain.start}']}")
            elif domain.start == -oo:
                limits['limit_at_-oo'] = sympy.limit(expr, x, domain.start)
                if isinstance(limits['limit_at_-oo'],AccumBounds):
                    a=limits['limit_at_-oo']
                    response.append(f"La fonction oscille entre {a.min} et {a.max} mais la limite n'existe pas")
                else:
                    response.append(f"limite en -oo : {limits['limit_at_-oo']}")
        else:
            limits['limit_at_left_edge'] = expr.subs(x, domain.start)
            response.append(f"limite en {domain.start} : {limits['limit_at_left_edge']}")
        
        if domain.right_open:
            if "oo" not in str(domain.end):
                limits[f'limit_at_{domain.end}'] = sympy.limit(expr, x, domain.end, dir='+')
                response.append(f"limite à droite en {domain.end} : {limits[f'limit_at_{domain.end}']}")
            elif domain.end == oo:
                limits['limit_at_oo'] = sympy.limit(expr, x, domain.end)
                if isinstance(limits['limit_at_oo'],AccumBounds):
                    a=limits['limit_at_oo']
                    response.append(f"La fonction oscille entre {a.min} et {a.max} mais la limite n'existe pas")
                else:
                    response.append(f"limite en oo : {limits['limit_at_oo']}")
        else:
            limits['limit_at_right_edge'] = expr.subs(x, domain.end)
            response.append(f"limite en {domain.end} : {limits['limit_at_right_edge']}")
    
    elif domain.is_Union or domain.is_Intersection:
        # Union of intervals
        intervals = domain.args
        for interval in intervals:
            if interval.left_open:
                if "oo" not in str(interval.start):
                    limits[f'limit_at_{interval.start}'] = sympy.limit(expr, x, interval.start, dir='-')
                    response.append(f"limite à gauche en {interval.start} : {limits[f'limit_at_{interval.start}']}")
                elif interval.start == -oo:
                    limits['limit_at_-oo'] = sympy.limit(expr, x, interval.start)
                    if isinstance(limits['limit_at_-oo'],AccumBounds):
                        a=limits['limit_at_-oo']
                        response.append(f"La fonction oscille entre {a.min} et {a.max} mais la limite n'existe pas")
                else:
                    response.append(f"limite en -oo : {limits['limit_at_-oo']}")
            else:
                limits[f'limit_at_{interval.start}'] = expr.subs(x, interval.start)
                response.append(f"limite en {interval.start} : {limits[f'limit_at_{interval.start}']}")

            if interval.right_open:
                if "oo" not in str(interval.end):
                    limits[f'limit_at_{interval.end}'] = sympy.limit(expr, x, interval.end, dir='+')
                    response.append(f"limite à droite en {interval.end} : {limits[f'limit_at_{interval.end}']}")
                elif interval.end == oo:
                    limits['limit_at_oo'] = sympy.limit(expr, x, interval.end)
                    if isinstance(limits['limit_at_oo'],AccumBounds):
                        a=limits['limit_at_oo']
                        response.append(f"La fonction oscille entre {a.min} et {a.max} mais la limite n'existe pas")
                else:
                    response.append(f"limite en oo : {limits['limit_at_oo']}")
            else:
                limits[f'limit_at_{interval.end}'] = expr.subs(x, interval.end)
                response.append(f"limite en {interval.end} : {limits[f'limit_at_{interval.end}']}")
    
    return [response, limits]

def get_boundary_point(interval1:Interval|Union, interval2:Interval|Union) -> int | None:
    # Helper function to extract the boundaries from a Set (Interval or Union)
    def get_boundaries(interval:Interval|Union)->list:
        if isinstance(interval, Interval):
            return [interval]
        elif isinstance(interval, Union):
            return [sub_interval for sub_interval in interval.args]
        else:
            raise ValueError

    # Get individual intervals (handles Unions and single Intervals)
    intervals1:list = get_boundaries(interval1)
    intervals2:list = get_boundaries(interval2)

    # Check each combination of sub-intervals for a shared boundary
    for sub_interval1 in intervals1:
        for sub_interval2 in intervals2:
            end_first_interval = sub_interval1.sup
            start_second_interval = sub_interval2.inf
            if end_first_interval == start_second_interval:
                return end_first_interval
    return None
def continuité(expr:Piecewise,boundary_point:int)->array:
    response=[]
    f1=expr.args[0][0]
    f2=expr.args[1][0]
    limit_at_right=limit(f1,x,boundary_point,dir="+")
    if limit_at_right:
        limit_at_left=limit(f2,x,boundary_point,dir="-")
    else:
        limit_at_right=limit(f1,x,boundary_point,dir="+")
        limit_at_left=limit(f2,x,boundary_point,dir="-")
    response.append(f"limite à gauche en {boundary_point}:{limit_at_left}")
    response.append(f"limite à droite en {boundary_point}:{limit_at_right}")
    match is_numeric_string(limit_at_left),is_numeric_string(limit_at_right):
        case True,True:
            response.append(f"la fonction est continue en {boundary_point}")
        case False,True:
            response.append(f"la fonction est continue à droite mais pas à gauche\nElle n'est pas continue en {boundary_point}")
        case True,False:
            response.append("la fonction continue à gauche mais pas à droite\nElle n'est pas continue en {boundary_point}")
        case False,False:
            response.append(f"La fonction n'est pas continue en {boundary_point}")
        case _:
            response.append("Erreur dans le calcul de la continuité")
    return response
         
def Piecewise_dérivabilité(expr:Piecewise,boundary_point:int)->dict:
    round(boundary_point,3)
    response=[]
    f1=expr.args[0][0]
    f2=expr.args[1][0]
    limit_at_right=limit(f1,x,boundary_point,dir="+")
    if limit_at_right:
        limit_at_left=limit(f2,x,boundary_point,dir="-")
    else:
        limit_at_right=limit(f1,x,boundary_point,dir="+")
        limit_at_left=limit(f2,x,boundary_point,dir="-")
    response.append(f"limite à gauche en {boundary_point}:{limit_at_left}")
    response.append(f"limite à droite en {boundary_point}:{limit_at_right}")
    match is_numeric_string(limit_at_left),is_numeric_string(limit_at_right):
        case True,True:
            response.append(f"la fonction est dérivable en {boundary_point}")
        case False,True:
            response.append("la fonction est dérivable à droite mais pas à gauche")
        case True,False:
            response.append("la fonction est dérivable à gauche mais pas à droite")
        case False,False:
            response.append(f"La fonction n'est pas dérivable en {boundary_point}")
        case _:
            response.append("Erreur dans le calcul de la dérivabilité")
    return response
    
def double_function_main(function1,function1_a,function1_b,function2,function2_a,function2_b,interval_style1,interval_style2):
    expr:Piecewise
    expr,fulldomain,subdomain1,subdomain2=get_piecewise_function_info(
    function1=function1,function1_a=function1_a,function1_b=function1_b,         
    function2=function2,function2_a=function2_a,function2_b=function2_b,
    interval_style1=interval_style1,interval_style2=interval_style2          
    )
    response0=[f"Expression complete:{expr}",
               f"Domaine complet:{format_domain(fulldomain)}",
               f"Domaine de f1(x):{format_domain(subdomain1)}",
               f"Domaine de f2(x):{format_domain(subdomain2)}"]
    for i in response0:
        print(f"{i}\n")
    response1={}
    print(f"----f1(x)={latex(sympify(expr.args[0][0]))} ----")
    limites_aux_bornes,limits=calculate_domain_and_border_limits2(expr.args[0][0],subdomain1)
    bi=branche_infinie(expr.args[0][0],limits)
    bi_sans_oo=branche_infinie_sans_oo(limits)
    dériv=dérivabilité(expr.args[0][0],subdomain1)
    response1["expression1"]=f"\\({latex(sympify(expr.args[0][0]))}\\)"
    response1["domaine_de_définition1"]=format_domain(subdomain1)
    response1["limites_aux_bornes1"]=limites_aux_bornes
    response1["branches_infinies1"]=bi
    response1["bisi1"]=bi_sans_oo
    response1["dérivabilité1"]=dériv
    print(response1)
    print(f"----f2(x)={latex(sympify(expr.args[1][0]))}----")
    response2={}
    limites_aux_bornes,limits=calculate_domain_and_border_limits2(expr.args[1][0],subdomain2)
    bi=branche_infinie(expr.args[1][0],limits)
    bi_sans_oo=branche_infinie_sans_oo(limits)
    dériv=dérivabilité(expr.args[1][0],subdomain2)
    response2["expression2"]=f"\\({latex(sympify(expr.args[1][0]))}\\)"
    response2["domaine_de_définition2"]=format_domain(subdomain2)
    response2["limites_aux_bornes2"]=limites_aux_bornes
    response2["branches_infinies2"]=bi
    response2["bisi2"]=bi_sans_oo
    response2["dérivabilité2"]=dériv
    print(response2)
    print("----Continuité et Dérivabilité de la fonction complete----")
    response3={}
    boundary_point=get_boundary_point(subdomain1,subdomain2)
    cont=[]
    dériv=[]
    if boundary_point!=None:
        cont=continuité(expr,boundary_point)
        dériv=Piecewise_dérivabilité(expr,boundary_point)
    response3["continuité"]=cont
    response3["dériv"]=dériv
    
    print(response3)
    final_response={**response1,**response2,**response3}
    return final_response
    # function1="x**2-4",         
    # function1_a=-oo,         
    # function1_b=-2,         
    # function2="x+1",     
    # function2_a=-2,         
    # function2_b=2   


    