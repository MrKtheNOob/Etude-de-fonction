from sympy import Contains, Interval, Piecewise, oo, sympify
import sympy
from algorythm import format_domain
from app import format_expression_for_mathjax


x=sympy.symbols("x")
def generate_html(data:dict):
    html_string = ""
    for key, values in data.items():
        html_string += f"<h2>{key}</h2>\n<ul>\n"
        if isinstance(values, list):
            for value in values:
                if 'expression' in key:
                    # Format expression values for MathJax
                    value = format_expression_for_mathjax(sympify(value))
                elif 'domain' in key:
                    # Format domain values for proper math signs
                    value = format_domain(sympify(value))
                html_string += f"  <li>{value}</li>\n"
        else:
            if 'expression' in key:
                # Format expression value for MathJax
                values = format_expression_for_mathjax(sympify(values))
            elif 'domaine de définition' in key:
                # Format domain value for proper math signs
                values = format_domain(sympify(values))
            html_string += f"  <li>{values}</li>\n"
        html_string += "</ul>\n"  
    return html_string
    # using jinja might be better than this function
# Example usage with the mock dictionary
data1 = {'expression1': Piecewise((x**2 - 4, Contains(x, Interval(-oo, -2))), (x + 1, Contains(x, Interval(-2, 2)))), 
        'domaine de définition1': Interval(-oo, -2), 
        'limites aux bornes1': ['limite en -oo : oo', 'limite en -2 : 0'], 
        'branches infinies1': ['limite en -oo de f(x)/x=-oo\nLa fonction admet une branche parabolique suivant (OY) au voisinage de -oo.'], 
        'branches infinies sans \\(\\infty\\)1': [], 
        'dérivabilité1': ["0 n'appartient pas au domain de la dérivée donc la fonction n'admet pas de tangente horizontalle", 
        "La fonction est dérivable sur l'entiereté du domaine de défnition.", 'La fonction est strictement décroissante sur (-oo, -2]', 'Dérivée:2*x']}
data2={'expression2': x + 1,
       'domaine de définition2': Interval(-2, 2), 
       'limites aux bornes2': ['limite en -2 : -1', 'limite en 2 : 3'], 
       'branches infinies2': [], 
       'branches infinies sans \\(\\infty\\)2': [], 
       'dérivabilité2': ['La fonction admet une tangente horizontale aux points :[]', "La fonction est dérivable sur l'entiereté du domaine de défnition.", 'La fonction est strictement croissante sur [-2, 2]', 'Dérivée:1']}
data3=[['limite à gauche en -2:-1', 'limite à droite en -2:0', 'la fonction est continue en -2'], ['limite à gauche en -2:-1', 'limite à droite en -2:0', 'la fonction est dérivable en -2']]
html_result1 = generate_html(data1)
html_result2=generate_html(data2)
print(html_result1+html_result2)


