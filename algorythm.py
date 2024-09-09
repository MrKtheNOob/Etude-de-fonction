

import random
from typing import List
from urllib import response
import sympy
from sympy import  N, AccumBounds, Intersection, Union, diff, solve, symbols, S, limit, sympify,oo,simplify
from sympy.calculus.util import continuous_domain
from sympy.sets import Interval



x = symbols('x')
def calculate_expression_at_random_point(expression,domain)->dict:
    response={}#dict that is going to be returned
    if isinstance(domain, Union) or isinstance(domain,Intersection):
        for interval in domain.args:
            if interval.left_open:
                if "-oo" in str(interval.start):
                    start=-1000
                else:
                    start=interval.start+0.000001
            else:
                start=interval.start
            if interval.right_open:
                if "oo" in str(interval.end):
                    end=1000
                else:
                    end=interval.end-0.000001
            else:
                end=interval.end
            random_point=random.uniform(start,end)
            response[domain]=expression.subs(x,random_point)
    else:#the domain is a single interval
        if domain.left_open:
            if "-oo" in str(domain.start):
                start=-1000
            else:
                start=domain.start+0.000001
        else:
            start=domain.start
        if domain.right_open:
            if "oo" in str(domain.end):
                end=1000
            else:
                end=domain.end-0.000001
        else:
            end=interval.end
            
        random_point=random.uniform(start,end)
        response[domain]=expression.subs(x,random_point)
    return response
def calculate_derivative_image_between_critical_points(derivative, domain, critical_points):
    response = {}
    numeric_values=[]    
    for point in critical_points:
        numeric_values.append(point.evalf())
    numeric_values.sort()

    
    # Assume critical_points is already sorted
    def recurse_interval(interval, numeric_values):
        # Find critical points within the interval (they're already sorted)
        critical_in_interval = [p for p in numeric_values if interval.start < p < interval.end]

        if not critical_in_interval:
            # Base case: No critical points within the interval, evaluate at a random point
            response.update(calculate_expression_at_random_point(derivative,interval))
        else:
            # Slice interval at the critical points and recurse
            last_point = interval.start
            for point in critical_in_interval:
                left_interval = Interval(last_point, point, interval.left_open if last_point == interval.start else True, True)
                recurse_interval(left_interval, [])  # Recurse on the left part (no need for more critical points)
                last_point = point
            # Process the last interval (from last critical point to the interval's end)
            right_interval = Interval(last_point, interval.end, True, interval.right_open)
            recurse_interval(right_interval, [])

    if isinstance(domain, Union) or isinstance(domain, Intersection):
        for interval in domain.args:
            recurse_interval(interval, critical_points)
    else:
        recurse_interval(domain, critical_points)

    return response

def format_interval(interval)-> str:
    
    if "Reals" in str(interval):
        return "R"
    if interval.left_open:
        left_bracket = "("  
    else:
       left_bracket= "["
    
    if interval.right_open:
        right_bracket = ")" 
    else:
        right_bracket="]"
        
    start = "-∞" if interval.start == oo else interval.start
    end = "∞" if interval.end == oo else interval.end
    return f"{left_bracket}{start}, {end}{right_bracket}"

def format_domain(domain)->str:
    if isinstance(domain, Union):
        intervals = [format_interval(interval) for interval in domain.args]
        return " ∪ ".join(intervals)
    else:
        return format_interval(domain)

def calculate_domain_and_border_limits(expression)->List:
    response = []
    limits = {}
    print("fonction :", expression)
    expr = sympify(expression)        
    
    # Calculate the domain of the expression
    domain = continuous_domain(expr, x, S.Reals)
    print(f"Domaine de défintion: {domain}")
    
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
                    if isinstance(limits['limit_at_-oo'],AccumBounds):
                        a=limits['limit_at_-oo']
                        response.append(f"La fonction oscille entre {a.min} et {a.max} mais la limite n'existe pas")
                else:
                    response.append(f"limite en oo : {limits['limit_at_oo']}")
            else:
                limits[f'limit_at_{interval.end}'] = expr.subs(x, interval.end)
                response.append(f"limite en {interval.end} : {limits[f'limit_at_{interval.end}']}")
    
    return [response, limits, domain]


def is_numeric_string(s):
    try:
        float(s)  # Convert to float to check if it's a numeric value
        return True
    except :
        return False


def branche_infinie_sans_oo(limits):
    response = []
    for key, limit in limits.items():
        if "oo" in key or "f(x)/x" in key:
            continue
        else:
            match str(limit):
                case "oo" | "-oo":
                    response.append(f"La fonction admet une asymptote verticale à x={key[9:]}")
                case s if is_numeric_string(s):
                    pass
                case _:
                    response.append(f"None")
    return response


def branche_infinie(expression, limits):
    response = []
    
    if "limit_at_oo" in limits:
        # Branch at +oo
        if limits["limit_at_oo"] in [oo, -oo]:
            limits["limit_f(x)/x_oo"] = sympy.limit(sympify(f"({expression})/x"), x, oo)
            match str(limits["limit_f(x)/x_oo"]):
                case "oo" | "-oo":
                    response.append(f"limite en oo de f(x)/x={limits['limit_f(x)/x_oo']}\nLa fonction admet une branche parabolique suivant (OY) au voisinage de +oo.")
                case "0":
                    response.append(f"limite en oo de f(x)/x={limits['limit_f(x)/x_oo']}\nLa fonction admet une branche parabolique suivant (OX) au voisinage de +oo.")
                case s if is_numeric_string(s):
                    a = limits["limit_f(x)/x_oo"]
                    response.append(f"limite en oo de f(x)/x={a}")
                    b = sympy.limit(sympify(f"{expression} - {a}*x"), x, oo)  # limite f(x) - ax
                    if is_numeric_string(b):
                        response.append(f"La fonction admet une asymptote oblique y={a}x + {b} au voisinage de +oo")
                    elif b == oo:
                        response.append(f"La fonction admet une branche parabolique de direction y={a}x au voisinage de +oo")
        elif is_numeric_string(limits["limit_at_oo"]):
            response.append(f"La fonction admet une asymptote horizontale y={limits['limit_at_oo']} au voisinage de +oo")
        del limits["limit_at_oo"]
    
    if "limit_at_-oo" in limits:
        # Branch at -oo
        if limits["limit_at_-oo"] in [oo, -oo]:
            limits["limit_f(x)/x_-oo"] = sympy.limit(sympify(f"({expression})/x"), x, -oo)
            match str(limits["limit_f(x)/x_-oo"]):
                case "oo" | "-oo":
                    response.append(f"limite en -oo de f(x)/x={limits['limit_f(x)/x_-oo']}\nLa fonction admet une branche parabolique suivant (OY) au voisinage de -oo.")
                case "0":
                    response.append(f"limite en -oo de f(x)/x={limits['limit_f(x)/x_-oo']}\nLa fonction admet une branche parabolique suivant (OX) au voisinage de -oo.")
                case s if is_numeric_string(s):
                    a = limits["limit_f(x)/x_-oo"]
                    b = sympy.limit(sympify(f"{expression} - {a}*x"), x, -oo)
                    if is_numeric_string(b):
                        response.append(f"La fonction admet une asymptote oblique y={a}x + {b} au voisinage de -oo")
                    elif b == oo:
                        response.append(f"La fonction admet une branche parabolique de direction y={a}x au voisinage de -oo")
        elif is_numeric_string(limits["limit_at_-oo"]):
            response.append(f"La fonction admet une asymptote horizontale y={limits['limit_at_-oo']} au voisinage de -oo")
        del limits["limit_at_-oo"]
    
    return response
def dérivabilité(expression,domain):
    response=[]
    #assuming the function is already sympified
    # Find the domain of the function (excluding points where it is undefined)
    # Compute the derivative
    f_prime = diff(expression, x)

    # Find the domain of the derivative
    domain_f_prime = continuous_domain(f_prime, x, domain)
   # Find critical points where the derivative is zero if 0 is its domain
    
    if domain_f_prime.contains(0):
        critical_points = solve(f_prime, x)
        critical_points = [point for point in critical_points if point.is_real]
        #sympy can sometimes tweak out and return a complex number to an expression that doesn't have complex numbers
        response.append(f"La fonction admet une tangente horizontale aux points :{critical_points}")
        print("La fonction admet une tangente horizontale aux points :")
        for point in critical_points:
            # Check if the critical point is in the domain
            if domain_f_prime.contains(point):
                print(f"   x={point}")
    else:
        response.append("0 n'appartient pas au domain de la dérivée donc la fonction n'admet pas de tangente horizontalle")
        print("0 n'appartient pas au domain de la dérivée donc la fonction n'admet pas de tangente horizontalle")
        critical_points=[]
    # Check where the function is differentiable and where it's not
    if domain == domain_f_prime:
        response.append(f"La fonction est dérivable sur l'entiereté du domaine de défnition.")
        print(f"La fonction est dérivable sur l'entiereté du domaine de défintion.")
        #the sign of the derivative at a random point inside the domain
        derivative_at_random_point=calculate_derivative_image_between_critical_points(f_prime,domain,critical_points)
     
        for k,v in derivative_at_random_point.items():
        
            if v>0:
                response.append(f"La fonction est strictement croissante sur {format_domain(k)}")
                print(f"La fonction est strictement croissante sur {format_domain(k)}")
            elif v<0:
                response.append(f"La fonction est strictement décroissante sur {format_domain(k)}")
                print(f"La fonction est strictement décroissante sur {format_domain(k)}")
    else:#the derivative is not differentiable in the function's domain
        
        response.append(f"La fonction est dérivable sur : {format_domain(domain_f_prime)}.")
        print(f"La fonction est dérivable sur : {format_domain(domain_f_prime)}.")
        derivative_at_random_point=calculate_derivative_image_between_critical_points(f_prime,domain_f_prime,critical_points)
        for k,v in derivative_at_random_point.items():
            
            if v>0:
                response.append(f"La fonction est strictement croissante sur {format_domain(k)}")
                print(f"La fonction est strictement croissante sur {format_domain(k)}")
            elif v<0:
                response.append(f"La fonction est strictement décroissante sur {format_domain(k)}")
                print(f"La fonction est strictement décroissante sur {format_domain(k)}")
        #repetitive code here,gotta make it a helper function
    

    response.append(f"Dérivée:{f_prime}")
    print(f"Dérivée:{f_prime}")
    return response


def print_dict_pretty(d):
    for key, value in d.items():
        # Check if the value is a list to handle multi-line values
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")
#il reste la continuité monotonie
def main(expression):
    full_response={}
    limites_aux_bornes,limits,domain=calculate_domain_and_border_limits(expression)
    bi=branche_infinie(expression,limits)
    bi_sans_oo=branche_infinie_sans_oo(limits)
    dériv=dérivabilité(expression,domain)
    full_response["expression"]=expression
    full_response["domaine de définition"]=domain
    full_response["limites aux bornes"]=limites_aux_bornes
    full_response["branches infinies"]=bi
    full_response[r"branches infinies sans \(\infty\)"]=bi_sans_oo
    full_response["dérivabilité"]=dériv
    #made this so that None appears on the frontend
    if len(full_response[r"branches infinies sans \(\infty\)"])==0:
        full_response[r"branches infinies sans \(\infty\)"].append("None")
    if len(full_response["branches infinies"])==0:
        full_response["branches infinies"].append("None")
    print_dict_pretty(full_response)
    return full_response

if __name__ == "__main__":
    main("x**2+sqrt(2*x+5)")
     
    


#exercices generaly ask things this way
#domain
#edge limits 
#infinite branches
#differentiability (where it is differentiable)
#the derivative 
#other shenanigans depending on the exercice (bijection ,solution ....)