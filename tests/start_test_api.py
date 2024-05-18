"""Deploy API instance"""

import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from thousand_api.main import app
from thousand_api.model import Base

if __name__ == "__main__":

    engine = create_engine("sqlite:///games.db")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    uvicorn.run(app, host="localhost", port=5001)
