"""
strompris fastapi app entrypoint
"""
import datetime
from typing import Union

from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from strompris import (
    LOCATION_CODES,
    ACTIVITIES,
    fetch_prices,
    plot_activity_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    """Renders the `strompris.html` template

    Args:
        request: the Request

    Returns:
        The 'strompris' html page
    """

    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "today": datetime.date.today(),
        },
    )


@app.get("/plot_prices.json")
def plot_prices_json(
    locations: list = Query(list(LOCATION_CODES.keys()), convert_underscores=False),
    end: Union[datetime.date, str, None] = None,
    days: int = 7,
) -> dict:
    """Plots a electricity price graph of the given locations and days up to and
    including the end date

    Args:
        locations: List of location codes to plot. Defaults to all regions.
        end: End date to plot to (inclusive)
        days: Number of days to plot up to and including end date

    Returns:
        vega-lite chart JSON dictionary
    """

    if isinstance(end, str):
        year, month, day = end.split("-")
        end = datetime.date(int(year), int(month), int(day))

    try:
        return plot_prices(
            fetch_prices(end_date=end, locations=locations, days=days)
        ).to_dict()
    except AssertionError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/activity", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    """Renders the `strompris.html` template

    Args:
        request: the Request

    Returns:
        The 'strompris' html page
    """

    return templates.TemplateResponse(
        "activity.html",
        {
            "request": request,
            "activities": ACTIVITIES.keys(),
            "location_codes": LOCATION_CODES,
            "today": datetime.date.today(),
        },
    )


@app.get("/plot_activity.json")
def plot_prices_json(
    location: str = "NO1",
    activity: str = "shower",
    minutes: int = 10,
) -> dict:
    """Plots a electricity price graph for the current day of the given activity.

    Args:
        locations: The location code to fetch prices for. Defaults to "NO1".
        activity: The activity to calculate the electricity consumption for. Defaults to "shower".
        minutes: The integer duration of the activity in minutes. Defaults to 10.

    Returns:
        dict: A vega-lite chart JSON dictionary.
    """
    try:
        return plot_activity_prices(
            fetch_prices(locations=[location], days=1),
            activity=activity,
            minutes=minutes,
        ).to_dict()
    except AssertionError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Mount sphinx static file docs
app.mount("/help", StaticFiles(directory="./docs/_build/html", html=True), name="help")


def main():
    """Launches the application with uvicorn on localhost port 5000

    Args:
        None

    Returns:
        None
    """
    import uvicorn

    uvicorn.run(app, port=5000)


if __name__ == "__main__":
    main()
