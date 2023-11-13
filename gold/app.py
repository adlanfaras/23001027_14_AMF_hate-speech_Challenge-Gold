from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

from cleansing import text_cleansing, file_cleansing
from db import db_connect, db_insert_cleaned_form, db_insert_cleaned_csv, show_cleansing_result

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API Text Cleansing"),
        'version' : LazyString(lambda: "1.0.0"),
        'description' : LazyString(lambda: "Dokumentasi API untuk Text Cleansing kata alay dan abusive"),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/home.yml", methods = ['GET'])
@app.route('/', methods=['GET'])
def home():
    json_response = {
        'status_code': 200,
        'description': "Gold Challenge Binar Academy",
        'Nama': "Adlan Muhammad Faras",
    }
    response_data = jsonify(json_response)
    return response_data

#form cleaning api
@swag_from('docs/cleansing_form.yml', methods=['POST'])
@app.route('/cleansing_form', methods=['POST'])
def cleansing_form_api():

    # Input text dari user
    raw_text = request.form["raw_text"]

    # Text cleansing
    clean_text = text_cleansing(raw_text)
    result_response = {"raw_text": raw_text, "clean_text": clean_text}

    # Insert result ke database
    db_connection = db_connect()
    db_insert_cleaned_form(db_connection, raw_text, clean_text)
    return jsonify(result_response)

#csv cleaning api
@swag_from('docs/cleansing_csv.yml', methods=['POST'])
@app.route('/cleansing_csv', methods=['POST'])
def cleansing_csv_api():

    # Input csv dari user
    uploaded_csv = request.files['upload_csv']

    # CSV cleansing
    df_cleansing = file_cleansing(uploaded_csv)

    # Insert result ke database
    db_connection = db_connect()
    db_insert_cleaned_csv(db_connection, df_cleansing)
    print("Upload result to database success!")
    result_response = df_cleansing.T.to_dict()
    return jsonify(result_response)

@swag_from('docs/show_cleansing_result.yml', methods=['GET'])
@app.route('/show_cleansing_result', methods=['GET'])
def show_cleansing_result_api():
    db_connection = db_connect()
    cleansing_result = show_cleansing_result(db_connection)
    return jsonify(cleansing_result)


if __name__ == '__main__':
    app.run()