from backend.databases.connection import Base,engine
from backend.databases.models import User,AnalysisRun

def create_tables():
    Base.metadata.create_all(
        bind=engine
    )
    print("Tables created successfully!")
    
if __name__ == "__main__":
    create_tables()