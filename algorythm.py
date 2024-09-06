
import sympy
from sympy import  diff, solve, symbols, S, limit, sympify,oo
from sympy.calculus.util import continuous_domain
from sympy.sets import Interval

#create an array for every function in which they are going to put in the print statements
#Ill create another array (yes an array of arrays) that is going to be a returned value that 
#the api will take to make the html response

x = symbols('x')

def calculate_domain_and_border_limits(expression):
    response=[]
    limits = {}
    print("fonction :",expression)
    expr = sympify(expression)        
    # Calculate the domain of the expression
    domain = continuous_domain(expr, x, S.Reals)
    # Prepare a dictionary to store limits
    # Check if the domain is an interval or union of intervals
    print(f"Domaine de défintion:{domain}")
    if isinstance(domain, Interval):
        
        #Im gonna remove the print statements or maybe duplicate thz file and in that file ill remove the print 
        #statements cuz they are all going to be (the msgs) in the response array
        # Single interval
        if domain.left_open:
            if "oo" not in str(domain.start):
                limits[f'limit_at_{domain.start}'] = sympy.limit(expr, x, domain.start, dir='-')
                response.append(f"limite à gauche en {domain.start} :{limits[f'limit_at_{domain.start}']}")
                print(f"limite à gauche en {domain.start} :{limits[f'limit_at_{domain.start}']}")
            elif "oo"==domain.start:
                limits[f'limit_at_{domain.start}'] =sympy.limit(expr, x, domain.start)
                response.append(f"limite en {domain.start} :{limits[f'limit_at_{domain.start}']}")
                print(f"limite en {domain.start} :{limits[f'limit_at_{domain.start}']}")
        else:
            limits['limit_at_left_edge'] = expr.subs(x, domain.start)
            response.append(f"limite en {domain.start}")
            print(f"limite en {domain.start}")
        if domain.right_open:
            if "oo" not in str(domain.end):
                limits[f'limit_at_{domain.end}'] =sympy.limit(expr, x, domain.end, dir='+')
                response.append(f"limite à droite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
                print(f"limite à droite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
            elif "oo" in str(domain.end):
                limits[f'limit_at_{domain.end}'] =sympy.limit(expr, x, domain.end)
                response.append(f"limite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
                print(f"limite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
        else:# the domain's right edge is closed
            limits['limit_at_right_edge'] = expr.subs(x, domain.end)
            response.append(f"limite à droite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
            print(f"limite à droite en {domain.end} :{limits[f'limit_at_{domain.end}']}")
        # return [limits,limits,domain]
    elif domain.is_Union or domain.is_Intersection:
        # Union of intervals
        intervals = domain.args
        for interval in intervals:
            if interval.left_open:
                if "oo" not in str(interval.start):
                    limits[f'limit_at_{interval.start}'] = limit(expr, x, interval.start, dir='-')
                    response.append(f"limite à gauche en {interval.start} :{limits[f'limit_at_{interval.start}']}")
                    print(f"limite à gauche en {interval.start} :{limits[f'limit_at_{interval.start}']}")   
                elif "oo" in str(interval.start):
                    limits[f'limit_at_{interval.start}'] =sympy.limit(expr, x, interval.start)
                    response.append(f"limite en {interval.start} :{limits[f'limit_at_{interval.start}']}")
                    print(f"limite en {interval.start} :{limits[f'limit_at_{interval.start}']}")
            else:
                #if the interval on the left is not opened ,meaning the value on the edge belongs to the domain
                #therefore there is no need to calculate limite à gauche ,the limit=f(value at the edge) 
                limits[f'limit_at_{interval.start}'] = expr.subs(x, interval.start)
                response.append(f"limite en {interval.start} :{limits[f'limit_at_{interval.start}']}")
                print(f"limite en {interval.start} :{limits[f'limit_at_{interval.start}']}")   

            if interval.right_open:
                if "oo" not in str(interval.end):
                    limits[f'limit_at_{interval.end}'] =sympy.limit(expr, x, interval.end, dir='+')
                    response.append(f"limite à droite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
                    print(f"limite à droite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
                elif "oo" in str(interval.end):
                    limits[f'limit_at_{interval.end}'] =sympy.limit(expr, x, interval.end)
                    response.append(f"limite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
                    print(f"limite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
            else:
                #same logic for the right side
                limits[f'limit_at_{interval.end}'] = expr.subs(x, interval.end)
                response.append(f"limite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
                print(f"limite en {interval.end} :{limits[f'limit_at_{interval.end}']}")
    return [response,limits,domain]
    # branche_infinie(expression,limits)
    # dérivabilité(expression,domain)


def is_numeric_string(s):
    try:
        float(s)  # Convert to float to check if it's a numeric value
        return True
    except ValueError:
        return False
def branche_infinie_sans_oo(limits):  
    response=[]
    for key, limit in limits.items():
        if "oo" in key or "f(x)/x" in key:
            continue
        else:
            match str(limit):
                case "oo" | "-oo":
                    response.append(f"La fonction admet une asymptote verticale à x={sympify(str(int(key[9:])))}")
                    
                    print(f"La fonction admet une asymptote verticale à x={sympify(str(int(key[9:])))}")
                case s if is_numeric_string(s):
                    pass
                case _:
                    response.append(f"pas de branche infinie en {key[9:]}")
                    print(f"pas de branche infinie en {key[9:]}")
    return response

def branche_infinie(expression,limits):
    response=[]
    
    if "limit_at_oo" in limits.keys():
        #branche infinie en +oo
        #remplace a par limits["limit_at_oo"] pour reduire les call au dictionaire qui sont couteux
        if limits["limit_at_oo"]==oo or limits["limit_at_oo"]==-oo:
            #la limite en oo =oo donc on calcule limite en oo de f(x)/x
            limits["limit_f(x)/x_oo"]=sympy.limit(sympify(f"({expression})/x"),x,oo)
            if "limit_f(x)/x_oo" in limits.keys():
                match str(limits["limit_f(x)/x_oo"]):
                    case "oo" | "-oo":
                        response.append(f"limite en oo de f(x)/x={limits["limit_f(x)/x_oo"]}\nLa fonction admet une branche parabolique suivant (OY) au voisinage de +oo.")
                        print(f"limite en oo de f(x)/x={limits["limit_f(x)/x_oo"]}")
                        print("La fonction admet une branche parabolique suivant (OY) au voisinage de +oo.")
                    case "0":
                        response.append(f"limite en oo de f(x)/x={limits['limit_f(x)/x_oo']}\nLa fonction admet une branche parabolique suivant (OX) au voisinage de +oo.")
                        print(f"limite en oo de f(x)/x={limits['limit_f(x)/x_oo']}\nLa fonction admet une branche parabolique suivant (OX) au voisinage de +oo.")
                    case s if is_numeric_string(s):
                        a=limits["limit_f(x)/x_oo"]
                        response.append(f"limite en oo de f(x)/x={a}")
                        print(f"limite en oo de f(x)/x={a}")
                        b=sympy.limit(sympify(f"{expression}-{a}*x"),x,oo) #limite f(x)-ax
                        if is_numeric_string(b):
                            response.append(f"la fonction admet une assymptote oblique y={a}x+{b} au voisinage de +oo")
                            print(f"la fonction admet une assymptote oblique y={a}x+{b} au voisinage de +oo")
                        elif b==oo:
                            response.append(f"la fonction admet une branche parabolique de direction y={a}x au voisinage de +oo")
                            print(f"la fonction admet une branche parabolique de direction y={a}x au voisinage de +oo")
                    case _:
                        pass
        elif is_numeric_string(limits["limit_at_oo"]):
            response.append(f"la fonction admet une assymptote horizontale y={limits["limit_at_oo"]} au voisinage de +oo")
            print(f"la fonction admet une assymptote horizontale y={limits["limit_at_oo"]} au voisinage de +oo")
        del limits["limit_at_oo"]
            
    elif "limit_at_-oo" in limits.keys():
        #branche infinie en -oo
        if limits["limit_at_-oo"]==oo or limits["limit_at_-oo"]==-oo:
            limits["limit_f(x)/x_-oo"]=sympy.limit(sympify(f"({expression})/x"),x,-oo)
            if "limit_f(x)/x_-oo" in limits:
                match str(limits["limit_f(x)/x_-oo"]):
                    case "oo" | "-oo":
                        response.append(f"limite en -oo de f(x)/x={limits["limit_f(x)/x_oo"]}\nLa fonction admet une branche parabolique suivant (OY) au voisinage de -oo.")
                        print(f"limite en -oo de f(x)/x={limits["limit_f(x)/x_oo"]}")
                        print("La fonction admet une branche parabolique suivant (OY) au voisinage de -oo.")
                    case "0":
                        response.append(f"limite en -oo de f(x)/x={limits["limit_f(x)/x_oo"]}\nLa fonction admet une branche parabolique suivant (OX) au voisinage de -oo.")
                        print(f"limite en -oo de f(x)/x={limits["limit_f(x)/x_oo"]}")
                        print("La fonction admet une branche parabolique suivant (OX) au voisinage de -oo.")
                    case s if is_numeric_string(s):
                        a=limits["limit_f(x)/x_-oo"]
                        b=sympy.limit(sympify(f"{expression}-{a}x"),x,oo) #limite f(x)-ax
                        if is_numeric_string(b):
                            response.append(f"limite en -oo de f(x)/x={a}\nlimite en -oo de f(x)-{a}x={b}\nla fonction admet une assymptote oblique y={a}x+{b} au voisinage de -oo")
                            print(f"la fonction admet une assymptote oblique y={a}x+{b} au voisinage de -oo")
                        elif b==oo:
                            print(f"limite en -oo de f(x)/x={a}\nlimite en -oo de f(x)-{a}x={b}")
                            response.append(f"limite en -oo de f(x)/x={a}\nlimite en -oo de f(x)-{a}x={b}\nla fonction admet une branche parabolique de direction y={a}x au voisinage de -oo")
                            print(f"la fonction admet une branche parabolique de direction y={a}x au voisinage de -oo")
                    case _:
                        pass
        elif is_numeric_string(limits["limit_at_-oo"]):
            response.append(f"la fonction admet une assymptote horizontale y={limits["limit_at_oo"]} au voisinage de -oo")
            print(f"la fonction admet une assymptote horizontale y={limits["limit_at_oo"]} au voisinage de -oo")
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

    # Check where the function is differentiable and where it's not
    if domain == domain_f_prime:
        response.append(f"la fonction est dérivable sur l'entiereté du domaine de défnition.")
        print(f"la fonction est dérivable sur l'entiereté du domaine de défnition.")
    else:
        differentiable_region = domain_f_prime
        response.append(f"la fonction est dérivable sur : {differentiable_region}.")
        print(f"la fonction est dérivable sur : {differentiable_region}.")
    
   # Find critical points where the derivative is zero if 0 is its domain
        if 0 in domain_f_prime:
            critical_points = solve(f_prime, x)
            response.append(f"La fonction admet une tangente horizontale aux points :{critical_points}")
            print("La fonction admet une tangente horizontale aux points :")
            for point in critical_points:
                # Check if the critical point is in the domain
                if point in differentiable_region:
                    print(f"   x={point}")
        else:
            response.append("0 n'appartient pas au domain de la dérivée donc la fonction n'admet pas de tangente horizontalle")
            print("0 n'appartient pas au domain de la dérivée donc la fonction n'admet pas de tangente horizontalle")
    response.append(f"Dérivée:{f_prime}")
    print(f"Dérivée:{f_prime}")
    return response
    

#il reste la continuité ,dérivabilité monotonie
def main(expression):
    full_response={}
    limites_aux_bornes,limits,domain=calculate_domain_and_border_limits(expression)
    bi=branche_infinie(expression,limits)
    bi_sans_oo=branche_infinie_sans_oo(limits)
    dériv=dérivabilité(expression,domain)
    full_response["expression"]=expression
    full_response["domain"]=domain
    full_response["limites aux bornes"]=limites_aux_bornes
    full_response["branches infinies"]=bi
    full_response["branches infinies sans oo"]=bi_sans_oo
    full_response["dérivabilité"]=dériv
    print(full_response)
    return full_response

if __name__ == "__main__":
    main("x**2")
     
    


#exercices generaly ask things this way
#domain
#edge limits (btw I need to point that out in the print statements)
#infinite branches
#differentiability (where it is differentiable)
#the derivative 
#other shenanigans depending on the exercice (bijection ,solution ....)