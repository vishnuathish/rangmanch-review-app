from sqlmodel import Session, create_engine, SQLModel

DATABSE_URL = "sqlite:///./reviews.db"
engine = create_engine(DATABSE_URL, echo=True)  

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


#TEST
