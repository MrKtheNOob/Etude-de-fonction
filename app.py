from typing import Any, Optional
from fastapi import FastAPI, Form,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from sympy import oo, sympify,latex
from fastapi.templating import Jinja2Templates
import os
from algorythm import main,format_domain
from db import insert_feedback
from double_functions import double_function_main,format_expression_for_mathjax

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def generate_html(data:dict):
    html_string = ""
    for key, values in data.items():
        html_string += f"<h2>{key}</h2>\n<ul>\n"
        if isinstance(values, list):
            for value in values:
                if 'expression' in key:
                    # Format expression values for MathJax
                    value = format_expression_for_mathax(sympify(value))
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

@app.get("/",response_class=HTMLResponse)
async def home():
    file_path = os.path.join("templates", "home.html")
    with open(file_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/feedback",response_class=HTMLResponse)
async def feedback(answer:str=Form(...),suggestion:str=Form(...)):
    print(f"FEEDBACK:answer={answer},suggestion={suggestion}")
    try:
        insert_feedback(answer,suggestion)
    except:
        return HTMLResponse(content="<h3>Erreur</h3>")
    return HTMLResponse(content="<h3>Merci pour votre retour 👍🙏</h3>")

@app.post("/calculate/étude",response_class=HTMLResponse)
async def étude(fonction: str = Form(...)):
    try:
        response_dict=main(expression=fonction)   
    except:
        return HTMLResponse(content="<h2>Erreur,vérifiez comment vous avez écrit votre fonction</h2>") 
    return HTMLResponse(content=generate_html(response_dict))

@app.post("/calculate/piecewise-étude")
async def receive_piecewise_data(request:Request,
    as_json:Optional[bool]=None,                                 
    function1: str = Form(...), 
    function1_a: str = Form(...),
    function1_b: str = Form(...),
    function2: str = Form(...),
    function2_a: str = Form(...), 
    function2_b: str = Form(...),
    interval_style1:str=Form(...),
    interval_style2:str=Form(...)
):
    function1_a, function1_b, function2_a, function2_b = [
    -oo if var == "-oo" else oo if "oo" in str(var) else int(var) 
    for var in [function1_a, function1_b, function2_a, function2_b]
    ]
    print(sympify(function1))
    print(function1_a)
    print(function1_b)
    print(sympify(function2))
    print(function2_a)    
    print(function2_b)
    print(interval_style1)
    print(interval_style2)
    data:dict=double_function_main(
        function1,function1_a,function1_b,function2,function2_a,function2_b,interval_style1,interval_style2
        )
    data.update({"request":request})
    if as_json:
        return JSONResponse(content=data)
    else:
        return templates.TemplateResponse("/components/piecewiseresult.html",context=data)
        

@app.get("/getintervalstyleselector",response_class=HTMLResponse)
async def get_interval_style_selector(request:Request):
    function_id=request.query_params.get("function_id")
    content=f"""
    <span class="variable">x</span>
    <span>∈</span>
    <select name="interval-style" class="interval-style" hx-get="/getinterval?function_id={function_id}" hx-target="closest .math-box"
    hx-swap="innerHTML">
        <option value="">Select interval style</option>
        <option value="[a,b]">[a, b]</option>
        <option value="[a,b[">[a, b[</option>
        <option value="]a,b[">]a, b[</option>
        <option value="]a,b]">]a, b]</option>
    </select>"""
    return HTMLResponse(content=content)
@app.get("/getinterval",response_class=HTMLResponse)
async def get_interval_form(request: Request):
    # Get interval style and function identifier from query parameters
    selected_interval = request.query_params.get("interval-style")
    function_id = request.query_params.get("function_id")  # 'function1' or 'function2'

    if not function_id:
        return HTMLResponse(content="<p>Invalid function identifier.</p>")

    # Create appropriate field names based on the function identifier
    a_field_name = f"{function_id}_a"
    b_field_name = f"{function_id}_b"
    id="1" if "1" in function_id else "2"
    #Using jinja might be more efficient here too but I'm focusing on making things work rn
    if selected_interval == "[a,b]":
        content = f"""
        <label for="interval-style{id}">
            <input type="hidden" name="interval_style{id}" id="interval-style{id}" value={selected_interval} >
        </label>
        <span class="variable">x</span>
         <span>∈</span>
        <label for="{a_field_name}"><span>&#91</span>
            <input id="input" type="text" name="{a_field_name}" placeholder="a" required>
        </label>
        <span>,</span>
        <label for="{b_field_name}">
            <input id="input" type="text" name="{b_field_name}" placeholder="b" required>&#93
        </label>
        <button hx-get="/getintervalstyleselector?function_id={function_id}" hx-target="closest .math-box" hx-swap="innerHTML swap:1s">Changer</button>
        """
    elif selected_interval == "[a,b[":
        content = f"""
        <label for="interval-style{id}">
            <input type="hidden" name="interval_style{id}" id="interval-style{id}" value={selected_interval} >
        </label>
        <span class="variable">x</span>
        <span>∈</span>
        <label for="{a_field_name}"><span> &#91</span>
            <input id="input" type="text" name="{a_field_name}" placeholder="a" required>
        </label>
        <span>,</span>
        <label for="{b_field_name}">
            <input id="input" type="text" name="{b_field_name}" placeholder="b" required>&#91
        </label>
        <button hx-get="/getintervalstyleselector?function_id={function_id}" hx-target="closest .math-box" hx-swap="innerHTML swap:1s">Changer</button>
        """
    elif selected_interval == "]a,b[":
        content = f"""
        <label for="interval-style{id}">
            <input type="hidden" name="interval_style{id}" id="interval-style{id}" value={selected_interval} >
        </label>
        <span class="variable">x</span>
        <span>∈</span>
        <label for="{a_field_name}"><span> &#93</span>
            <input id="input" type="text" name="{a_field_name}" placeholder="a" required>
        </label>
        <span>,</span>
        <label for="{b_field_name}">
            <input id="input" type="text" name="{b_field_name}" placeholder="b" required>&#91
        </label>
        <button hx-get="/getintervalstyleselector?function_id={function_id}" hx-target="closest .math-box" hx-swap="innerHTML swap:1s">Changer</button>        
        """
    elif selected_interval == "]a,b]":
        content = f"""
        <label for="interval-style{id}">
            <input type="hidden" name="interval_style{id}" id="interval-style{id}" value={selected_interval} >
        </label>
        <span class="variable">x</span>
        <span>∈</span>
        <label for="{a_field_name}"><span> &#93</span>
            <input id="input" type="text" name="{a_field_name}" placeholder="a" required>
        </label>
        <span>,</span>
        <label for="{b_field_name}">
            <input id="input" type="text" name="{b_field_name}" placeholder="b" required>&#93
        </label>
        <button hx-get="/getintervalstyleselector?function_id={function_id}" hx-target="closest .math-box" hx-swap="innerHTML swap:1s">Changer</button>                
        """
    else:
        content = "<p>Invalid interval style selected.</p>"

    return HTMLResponse(content=content)

@app.get("/components/{component_name}")
async def load_component(component_name:str):
    file_path = os.path.join("templates","components",f"{component_name}.html")
    with open(file_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
if __name__ == "__main__":
    import uvicorn
    try:
        port= os.environ['PORT']
    except KeyError:
        port=80
    uvicorn.run("app:app", host="0.0.0.0", port=port)
    
