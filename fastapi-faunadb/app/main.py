import uvicorn
from typing import List, Dict 
from pydantic import ValidationError
from routes.users import router as UserRouter 
from routes.tweets import router as TweetRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException, Response, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Mini-Twitter with FastAPI and FaunaDB')

app.include_router(UserRouter, prefix='/api/v1', tags=['User Endpoints'])
app.include_router(TweetRouter, prefix='/api/v1', tags=['Tweet Router'])

# Adding the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
## DOCUMENTATION REFERENCE :- https://fastapi.tiangolo.com/tutorial/handling-errors/
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request,exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "status":False,
            "error": exc.detail
        }),
    )

# Run the app via uvicorn on PORT 8000
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)