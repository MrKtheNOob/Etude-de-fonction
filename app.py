from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sympy import symbols, limit,diff,sympify,oo,latex,S,SympifyError
from sympy.calculus.util import continuous_domain
from typing import Union
import os
from algorythm import main,format_domain

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_html(data):
    html_string = ""
    
    for key, values in data.items():
        html_string += f"<h2>{key}</h2>\n<ul>\n"
        if isinstance(values, list):
            for value in values:
                if key == 'expression':
                    try:
                        # Sympify the expression and convert to LaTeX
                        expr = sympify(values)
                        latex_expr = latex(expr)
                        html_string += f"  <li style='font-size:3em' >\\({latex_expr}\\)</li>\n"
                    except (SympifyError, ValueError):
                        # If the expression can't be sympified, show it as plain text
                        html_string += f"  <li style='font-size:3em' >\\({values}\\)</li>\n"
                elif key == 'domaine de définition':
                    # Format the domain using format_domain
                    formatted_value = format_domain(value)
                    html_string += f"  <li>{formatted_value}</li>\n"
                else:
                    html_string += f"  <li>{value}</li>\n"
        else:
            if key == 'expression':
                try:
                    # Sympify the expression and convert to LaTeX
                    expr = sympify(values)
                    latex_expr = latex(expr)
                    html_string += f"  <li style='font-size:3em'>\\({latex_expr}\\)</li>\n"
                except (SympifyError, ValueError):
                    # If the expression can't be sympified, show it as plain text
                    html_string += f"  <li style='font-size:3em'>\\({values}\\)</li>\n"
                
            elif key == 'domaine de définition':
                # Format the domain using format_domain
                formatted_value = format_domain(values)
                html_string += f"  <li>{formatted_value}</li>\n"
            else:
                html_string += f"  <li>{values}</li>\n"
        html_string += "</ul>\n"
    
    
    return html_string
@app.get("/limite", response_class=HTMLResponse)
async def limit_page():
    file_path = os.path.join("templates", "limit.html")
    with open(file_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
@app.get("/dérivée",response_class=HTMLResponse)
async def derivative_page():
    file_path = os.path.join("templates", "derivative.html")
    with open(file_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
@app.get("/home",response_class=HTMLResponse)
async def home():
    file_path = os.path.join("templates", "home.html")
    with open(file_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
# Endpoint to calculate the limit
@app.post("/calculate/limit", response_class=HTMLResponse)
async def calculate_limit(fonction: str = Form(...),variable: str = Form(...),target:Union[int,str] = Form(...)):
    target=int(target)
    print("fonction:",fonction)
    print("variable:",variable)
    print("valeur limit:",target)
    try:
        # Define the variable symbol
        x = symbols(variable)
        
        # Convert function string to SymPy expression
        expr = sympify(fonction)
        
        # Convert target to float (or handle as needed)
        target_value = float(target)
        
        # Compute the limit
        limit_value = float(limit(expr, x, target_value))
        return HTMLResponse(content=f'<h2 id="result">{round(limit_value,4)}</h2>')
    except Exception as e:
        # Return error message if something goes wrong
        return HTMLResponse(content=f"<p>Error: {e}</p>", status_code=400)
@app.post("/calculate/derivative",response_class=HTMLResponse)
async def calculate_derivative(fonction:str=Form(...)):
    try:
        print("function:",fonction)
        derivative=diff(fonction,symbols("x"))
        response = f"\\( {latex(derivative)} \\)"
        return HTMLResponse(content=f"<h2 id='result'>f'(x)={response}</h2>")
    except Exception as e:
        return HTMLResponse(content=f"<p>Error: {e}</p>", status_code=400)

@app.post("/calculate/domain",response_class=HTMLResponse)
async def calculate_domain(fonction: str=Form(...)):
    try:
        x = symbols('x')
        expr = S(fonction)
        domain = continuous_domain(expr, x, S.Reals)
        if str(domain)=="Reals":
            return HTMLResponse(content="<h2 id='result'> R </h2>")    
            # <p>Set of real numbers: \( \mathbb{R} \)</p>
        response = f"\\( {latex(domain)} \\)"
        return HTMLResponse(content=f"<h2 id='result'>{response}</h2>")
    except Exception as e:
        return {"Error":e}
@app.post("/calculate/étude",response_class=HTMLResponse)
async def étude(fonction: str = Form(...),):
    response_dict=main(expression=fonction)
    return HTMLResponse(content=generate_html(response_dict))

if __name__ == "__main__":
    import uvicorn
    try:
        port= os.environ['PORT']
    except KeyError:
        port=8080
    uvicorn.run("app:app", host="0.0.0.0", port=port)
    
