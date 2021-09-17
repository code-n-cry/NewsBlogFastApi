import os
from databases import Database
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://jmbwrqtkciptar:49a7cc52b929258ba0667f13e3227601473c1245ef78dd5965ced615442a1dc0@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/d3vhsjgllvb4ht"
engine = create_engine(DATABASE_URL, echo=False)
database = Database(DATABASE_URL)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3j5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30