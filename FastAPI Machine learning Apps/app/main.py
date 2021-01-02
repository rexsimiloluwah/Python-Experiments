# Main FastAPI app 
import uvicorn
from fastapi import FastAPI,Request,HTTPException, Depends, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 
from heartdiseaseprediction.api import router as HeartDiseaseRouter
from moviessentimentanalysis.api import router as MovieSentimentRouter
# Initialize the app
app = FastAPI()

# Mount the static files dir
app.mount(
    "/static", 
    StaticFiles(directory = "static"),
    name = "static"
)

# Templates
templates = Jinja2Templates(directory = "templates")


@app.get("/", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request})

@app.get("/heartdisease", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("heartdiseaseprediction.html", {"request" : request})

@app.get("/moviesentiment", response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("sentimentanalysis.html", {"request" : request})

app.include_router(
    HeartDiseaseRouter,
    tags = ["Heart Disease Prediction"],
    prefix = "/heartdiseasemodel"
)

app.include_router(
    MovieSentimentRouter,
    tags = ["Movies Review Sentiment Analysis"],
    prefix = "/moviesentimentmodel"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "message": "An error occurred",
            "loc" : exc.errors()[0]["loc"],
            "detail": exc.errors()[0]["msg"]
        }),
    )

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 5000)