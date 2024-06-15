"""TODO: Write docstring"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from thousand_api.db.database import database_init
from thousand_api.endpoints.game_endpoints import router as games_router
from thousand_api.endpoints.main_endpoints import router as main_router
from thousand_api.endpoints.player_endpoints import router as player_router
from thousand_api.endpoints.table_endpoints import router as table_router

origins = ["http://localhost:5000", "http://127.0.0.1:5000", "http://147.78.130.54:5000"]  # Frontend URLs
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(main_router, prefix="", tags=["Main"])
app.include_router(games_router, prefix="/game", tags=["Game Utilities"])
app.include_router(player_router, prefix="/player", tags=["Player Utilities"])
app.include_router(table_router, prefix="/table", tags=["Table utilities"])

if __name__ == "__main__":
    database_init()
    uvicorn.run(app, host="0.0.0.0", port=5002)
