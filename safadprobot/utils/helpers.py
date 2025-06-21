# Utility functions
from safadprobot.utils.helpers import init_db

def init_db():
    Base.metadata.create_all(bind=engine)
