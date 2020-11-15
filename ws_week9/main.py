from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import math
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import requests


matplotlib.use('Agg')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_roots(a, b, c):
    try:
        a, b, c = int(a), int(b), int(c)
    except:
        return None

    if a != 0:
        D = b**2-4*a*c
        if D < 0:
            roots = []
        elif D == 0:
            roots = [(-b + math.sqrt(D)) / (2*a)]
        else:
            roots = [(-b+math.sqrt(D))/(2*a), (-b-math.sqrt(D))/(2*a)]
    elif b != 0:
        roots = [-c/b]
    else:
        roots = [c]

    return roots


def f(x, a, b, c):
    return (a * x ** 2 + b * x + c)


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "picture": None})


@app.get("/solve")
async def solve(a, b, c):
    return {"roots": get_roots(a, b, c)}


@app.post("/show_plot")
async def show_plot(request: Request,
                     var_a: str = Form(...),
                     var_b: str = Form(...),
                     var_c: str = Form(...)):

    png_img = io.BytesIO()

    a, b, c = int(var_a), int(var_b), int(var_c)
    roots = get_roots(var_a, var_b, var_c)

    if roots is None:
        return templates.TemplateResponse("index.html",
                                          {"request": request, "roots": [], "picture": None})

    center = 0 if not roots else (roots[0] if len(roots) == 1 else (sum(roots)/len(roots)))

    X = [0.1*x+center for x in range(-50, 50, 1)]
    Y = [f(x, a, b, c) for x in X]
    fig = plt.figure()
    plt.plot(X, Y)
    if roots:
        if len(roots) > 1:
            plt.plot(roots[1], f(roots[1], a, b, c), 'ro')
        plt.plot(roots[0], f(roots[0], a, b, c), 'ro')

    plt.savefig(png_img)

    png_img_b64_str = base64.b64encode(png_img.getvalue()).decode("ascii")

    return templates.TemplateResponse("index.html", {"request": request, "roots": roots, "picture": png_img_b64_str})
