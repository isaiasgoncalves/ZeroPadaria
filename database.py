import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def test_connection():
   try:

      with engine.connect() as conn:
         result = conn.execute(text("SELECT version()"))
         print("Conexão funcionando", result.fetchone()[0])
         return True
   except Exception as e:
      print("Erro na conexão: ", e)
      return False

def seek_users():
   return pd.read_sql("SET SEARCH_PATH = zeropadaria; SELECT * FROM users;", engine)

def insert_diners(userID, date, almoco, janta,  cafe, lanche, marmita):

   with engine.connect() as conn:
      conn.execute(text("""
         SET SEARCH_PATH = zeropadaria;
         INSERT INTO registro (date, userID, cafe, almoco, janta, lanche, marmita)
         VALUES (:date, :userID, :cafe, :almoco, :janta, :lanche, :marmita)
      
      """), {
         "date" : date, "userID": userID, "almoco" : almoco, "janta" : janta,
         "cafe": cafe, "lanche" : lanche, "marmita" : marmita
      })

      conn.commit()

