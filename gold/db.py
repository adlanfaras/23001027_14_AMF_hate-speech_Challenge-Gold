import pandas as pd
import sqlite3

# Sambung ke database
def db_connect():
    conn = sqlite3.connect('database.db')
    return conn

def db_insert_csv(conn):
    # Membaca csv menjadi dataframe
    df_abusive = pd.read_csv("data/abusive.csv")
    df_alay = pd.read_csv("data/kamus_alay.csv", encoding='latin-1', names=['alay_words', 'formal_words'])
    df_abusive.columns = ['abusive_words']
    
    # Simpan dataframe ke database
    df_abusive.to_sql('abusive', conn, if_exists='replace', index=False)
    df_alay.to_sql('alay', conn, if_exists='replace', index=False)
    

def db_insert_cleaned_form(conn, raw_text, cleaned_text):
    # Simpan result ke database
    df = pd.DataFrame({'raw_text': [raw_text], 'clean_text': [cleaned_text]})
    df.to_sql('cleansing_result', conn, if_exists='append', index=False)
    
def db_insert_cleaned_csv(conn, cleaned_df):
    # Simpan result ke database
    cleaned_df.to_sql('cleansing_result', conn, if_exists='append', index=False)  
  
def show_cleansing_result(conn):
    # Menunjukkan cleansing result
    df = pd.read_sql_query("SELECT * FROM cleansing_result", conn)
    return df.T.to_dict()
