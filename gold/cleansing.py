import re
import pandas as pd
import sqlite3
from db import db_connect, db_insert_csv

conn = db_connect()
db_insert_csv(conn)

#Import dataframe abusive dan ubah jadi list
data_abusive = pd.read_sql('Select abusive_words from abusive', conn)
abusive_list = data_abusive.values.flatten()

# Import dataframe kata alay dan formal
data_alay_word = pd.read_sql('Select * from alay', conn)
# Mengubah dataframe menjadi dictionary
dict_alay = dict(zip(data_alay_word['alay_words'],data_alay_word['formal_words']))
conn.close()


def text_cleansing(text):
    # Menghilangkan Non-alphabet dan angka
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Mengecilkan kata
    cleaned_text = cleaned_text.lower()
   
    # Mengubah kata abusive menjadi ***
    regex_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, abusive_list)) + r')\b', flags=re.IGNORECASE)
    replacement_string = "***"
    cleaned_text = regex_pattern.sub(replacement_string, cleaned_text)

    # Mengganti kata alay dengan kata formal
    cleaned_text = " ".join(dict_alay.get(word, word) for word in cleaned_text.split())

    return cleaned_text

def file_cleansing(file_upload):
    # Read csv file
    df_upload = pd.read_csv(file_upload, encoding="latin-1")

    # Ambil kolom text
    df_upload = pd.DataFrame(df_upload.iloc[:,0])

    # Rename kolom menjadi "raw_text"
    df_upload.columns = ["raw_text"]

    # Bersihkan text menggunakan fungsi text_cleansing dan simpan di kolom "clean_text"
    df_upload["clean_text"] = df_upload["raw_text"].apply(text_cleansing)
    print("Cleansing text success!")
    return df_upload

