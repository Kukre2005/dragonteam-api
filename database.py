from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_aPkQJcwjm5T0@ep-raspy-surf-acmdy9ys-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# connect_args={"check_same_thread": False} logic is needed only for SQLite.
engine = create_engine( SQLALCHEMY_DATABASE_URL )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
