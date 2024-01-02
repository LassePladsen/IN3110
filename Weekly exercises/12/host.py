from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

greetings = list()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@app.post("/")
def root(request: Request, name: str = Form(...)):
    url = f"/greet/{name}"
    return RedirectResponse(url=url)


@app.get("/hello/")
def hello():
    return {"Hello world"}


@app.get("/greet/{name}")
@app.post("/greet/{name}")
def greet(request: Request, name):
    greetings.append(name)
    return templates.TemplateResponse("greet.html", {"request": request, "name": name})

@app.get("/greetings")
def all_greetings(request: Request):
    return templates.TemplateResponse("greetings.html", {"request": request, "greetings": greetings})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)