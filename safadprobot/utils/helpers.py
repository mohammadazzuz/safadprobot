# Utility functions
from safadprobot.db.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)

