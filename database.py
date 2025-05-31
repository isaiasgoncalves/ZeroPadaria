import os
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from dotenv import load_dotenv
import hashlib

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
   return pd.read_sql("""
                      SET SEARCH_PATH = zeropadaria; 
                      SELECT userID, 
                             userName, 
                             userEmail, 
                             userRole 
                      FROM users;
                      """, engine)

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

def hashpassword(password):
   """Cria hash da senha para armazenamento"""
   return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
   """Verifica credenciais de acesso no login"""
   try:
      password_hash = hashpassword(password)
      query = """
              SET SEARCH_PATH = zeropadaria;
              SELECT user_id, username, usaremail, userrole
              FROM users
              WHERE useremail = %s AND userpassword = %s
            """
      
      with engine.connect() as conn:
         result = conn.execute(text(query), (email, password_hash))
         user = result.fetchone()

         if user:
            return{
               'userid'    : user[0],
               'username'  : user[1],
               'useremail' : user[2],
               'userrole'  : user[3]

            }
         else:
            return None

   except Exception as e:
      print("Erro na autenticação: ", e)
      return None
   

def check_user_permissions(required_role):
   """Verifica a permissão do usuário"""
   if 'user' not in st.session_state:
      return False
   
   user_role = st.session_state['user']['userrole']

   # Libera tudo pro adm
   if user_role == "admin":
      return True
   
   if required_role == 'usr' and user_role == 'usr':
      return True
   
   return False


