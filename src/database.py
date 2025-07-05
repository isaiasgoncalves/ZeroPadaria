""" Arquivo responsável pelas interações com o banco de dados """

import psycopg2
import os
import config
import pandas as pd


creation_query = config.CREATION_QUERY

conn = psycopg2.connect(config.DATABASE_URL)

with conn.cursor() as cursor:
    cursor.execute(creation_query)

def get_users():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=["userID", "userName", "userEmail", "userRole", "userPassword"])

def insert_user(userName, userEmail, userRole, userPassword):
    with conn.cursor() as cur:
        cur.execute("SELECT userId from Users ORDER BY userId DESC")
        userId = int(cur.fetchone()[0]) + 1
        cur.execute(f"""
                    INSERT INTO Users
                    VALUES ({userId}, '{userName}', '{userEmail}', '{userRole}', '{userPassword}');
                    """)
        print(f"Usuário {userName} adicionado com sucesso com o ID {userId}!")
        return userId




conn.commit()
conn.close()


