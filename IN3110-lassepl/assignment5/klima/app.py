from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from klima import plot_mean_temperatures, get_monthly_mean_temperatures

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    """Renders the `klima.html` template

    Args:
        request: the Request

    Returns:
        The 'klima' html page
    """

    return templates.TemplateResponse("klima.html", {"request": request})


@app.get("/plot_climate.json")
def plot_climate(unit: str) -> dict:
    """Plots a global monthly average temperatures for each year

    Args:
        unit: Which unit used for the temperature, either "C" og "F"

    Returns:
        vega-lite chart JSON dictionary
    """

    try:
        return plot_mean_temperatures(
            get_monthly_mean_temperatures(unit=unit)
        ).to_dict()
    except AssertionError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Mount sphinx static file docs
app.mount("/help", StaticFiles(directory="./docs/_build/html", html=True), name="help")


def main():
    """Launches the application with uvicorn on localhost port 4000

    Args:
        None

    Returns:
        None
    """
    import uvicorn

    uvicorn.run(app, port=4000)


if __name__ == "__main__":
    main()
