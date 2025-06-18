from fastapi import FastAPI, APIRouter, Depends
from starlette.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI(
    title='DimaTech Ltd',
    description='Тестовое задание на позицию Python разработчик by piravky',
    version='0.1.0',
    docs_url='/api/docs/',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)