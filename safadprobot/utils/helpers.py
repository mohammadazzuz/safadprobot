# Utility functions
from safadprobot.db.database import Base, engine
from safadprobot.db import models
def init_db():
    Base.metadata.create_all(bind=engine)

