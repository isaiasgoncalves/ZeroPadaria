import streamlit as st
import pandas as pd
from datetime import date, datetime
from database import test_connection, seek_users, insert_diners, engine
from datetime import timedelta


st.set_page_config(page_title="ZeroPadaria, o novo sistema de comensais do CCUB", layout="wide")

def main():
   st.title("ZeroPadaria, o novo sistema de comensais do CCUB")

   # Sidebar
   st.sidebar.title("Menu")
   opcao = st.sidebar.selectbox("Escolha uma opção:", ["Registrar Comensais", 
                                                       "Visualizar Dados", 
                                                       "Relatórios",
                                                       "Detectar Padarias"])

   if opcao == "Registrar Comensais":
      register_diners()
   elif opcao == "Visualizar Dados":
      visualize_data()
   elif opcao == "Relatórios":
      show_reports()
   elif opcao == "Detectar Padarias":
      who_will_eat()


def register_diners():
   st.header("Registrar os comensais")

   # Formulário
   col1, col2 = st.columns(2)

   with col1:
      # Buscar usuários no banco
      users_df = seek_users()
      user_options = {f"{row['username']} ({row['useremail']})":row['userid'] for _, row in users_df.iterrows()}

      selected_user = st.selectbox("Selecione o usuário: ", list(user_options.keys()))

      date_diners = st.date_input("Data: ", value=date.today())

   with col2:
      almoco = st.selectbox("Almoço: ", ["Não", "Sim", "Cedo", "Tarde"])
      janta = st.selectbox("Jantar: ", ["Não", "Sim", "Tarde"])
      cafe = st.selectbox("Café da Manhã: ", ["Não", "Sim", "Cedo"])
      lanche = st.selectbox("Lanche: ", ["Não", "Sim"])
      marmita = st.selectbox("Marmita: ", ["Não", "Sim"])

   if st.button('Salvar Comensais'):
      try:
         userID = user_options[selected_user]
         insert_diners(userID, date_diners, almoco, janta, cafe, lanche, marmita)
         st.success("Comensais registrados com sucesso!")
      except Exception as e:
         st.error(f"Erro ao salvar: {e}")

def show_table(query):

   df = pd.read_sql(query, engine)

   if not df.empty:
      st.dataframe(df, use_container_width=True)

   else:
      st.info("Nenhuma informação a ser exibida")

def show_reports():
   st.header("Visualizar Comensais")
   date_diners = st.date_input("Data: ", value=date.today())

   query = """
   SET SEARCH_PATH = zeropadaria;
   SELECT date,
          COUNT(CASE WHEN almoco   = 'Cedo' THEN 1 END) AS almoco_cedo,
          COUNT(CASE WHEN almoco   = 'Sim' THEN 1 END) AS almoco_normal,
          COUNT(CASE WHEN almoco   = 'Tarde' THEN 1 END) AS almoco_tarde,
          COUNT(CASE WHEN janta    = 'Sim' THEN 1 END) AS janta_normal,
          COUNT(CASE WHEN janta    = 'Tarde' THEN 1 END) AS janta_tarde,
          COUNT(CASE WHEN cafe     = 'Cedo' THEN 1 END) AS cafe_cedo,
          COUNT(CASE WHEN cafe     = 'Sim' THEN 1 END) AS cafe_normal,
          COUNT(CASE WHEN lanche   = 'Sim' THEN 1 END) AS lanche,
          COUNT(CASE WHEN marmita  = 'Sim' THEN 1 END) AS marmita
   FROM registro
   WHERE date = '{date}'
   GROUP BY date
   ORDER BY date;
   """
   df = pd.read_sql(query.format(date=date_diners), engine)

   if not df.empty:
      st.dataframe(df, use_container_width=True)

   else:
      st.info("Nenhuma refeição registrada.")


def visualize_data():

   date_diners = st.date_input("Data: ", value=date.today())

   query = """
   SET SEARCH_PATH = zeropadaria;
   SELECT r.date,
          u.username,
          r.almoco,
          r.janta,
          r.cafe,
          r.lanche,
          r.marmita
   FROM registro as r
   INNER JOIN users AS u ON r.userid = u.userid
   WHERE r.date = '{date}';
   """
   df = pd.read_sql(query.format(date=date_diners), engine)

   if not df.empty:
      st.dataframe(df, use_container_width=True)

   else:
      st.info("Nenhuma refeição registrada.")


   pass

def show_table(query):
    df = pd.read_sql(query, engine)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma informação a ser exibida")

def who_will_eat():

   date_diners = st.date_input("Data: ", value=date)
   meal = st.selectbox("Escolha uma refeição:", ["Café da Manhã", "Almoço", "Jantar", "Lanche", "Marmita"])
    
   # Configurações por refeição
   meal_config = {
       "Café da Manhã": {
           "column": "cafe",
           "options": [("Café Cedo", "Cedo"), ("Café No Horário", "Sim")]
       },
       "Almoço": {
           "column": "almoco", 
           "options": [("Almoço Cedo", "Cedo"), ("Almoço no Horário", "Sim"), ("Almoço Tarde", "Tarde")]
       },
       "Jantar": {
           "column": "janta",
           "options": [("Janta no Horário", "Sim"), ("Janta Tarde", "Tarde")]
       },
       "Lanche": {
           "column": "lanche",
           "options": [("Lanche", "Sim")]
       },
       "Marmita": {
           "column": "marmita",
           "options": [("Marmita", "Sim")]
       }
   }
   
   # Query base reutilizável
   base_query = """
   SET SEARCH_PATH = zeropadaria;
   SELECT r.date AS Data, u.username AS Nome
   FROM registro AS r
   INNER JOIN users AS u ON r.userid = u.userid
   WHERE r.{column} = '{value}' AND r.date = '{date}'
   """
    
    # Executar para a refeição selecionada

   config = meal_config[meal]
   # date_diners is a datetime.date object from st.date_input
   # To subtract one day, use timedelta

   if meal in ["Café da Manhã", "Lanche", "Marmita"]:
      seek_date = date_diners - timedelta(days=1)
   else:
      seek_date = date_diners

   # Format seek_date as string for SQL query
   #seek_date = seek_date.strftime("%Y-%m-%d")
   for header, value in config["options"]:
      st.header(f"{header}:")
      query = base_query.format(column=config["column"], value=value, date=seek_date)
      show_table(query)

if __name__ == "__main__":
   main()