from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#connection url
SQLALCHEMY_DATABSE_URL= f'postgresql://{settings.database_password}:{settings.database_username}@{settings.database_hostname}/{settings.database_name}'

#create an engine responsable to connect sqlachamy to postgres

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# we are using sqlalchemy instead 

# while True:
#     try:
#         conn = psycopg2.connect(jost ='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor
#         print('Database connection was succesfull')
#         break
#     except Exception as e:
#         print(f" Failed to connnect to database {e}")
#         time.sleep(2)