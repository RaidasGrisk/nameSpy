from fastapi import FastAPI
from endpoints.db_queries import router as db_routes
from endpoints.server_status import router as server_status_routes

app = FastAPI()

app.include_router(db_routes, prefix='/db_routes')
app.include_router(server_status_routes, prefix='/server_status')

@app.get('/ping')
async def root():
    return {'message': 'Hi!'}