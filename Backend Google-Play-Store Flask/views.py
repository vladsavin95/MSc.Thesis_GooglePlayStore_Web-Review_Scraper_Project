import os
import json, uuid
from flask_restful import Resource
from flask import (
    render_template,
    redirect, request,
    url_for, jsonify
)
from main import run_analysis

#################
####  Views  ####
#################

# Index/Home Page View
def index():
    return render_template("index.html")

# Perform Search View
class Search(Resource):
    def post(self):
        try:
            data = request.get_json()
            app_link = data['appLink']
            mask = data['mask']
            color = data['color']
            font_ = data['font']
            maxwords = int(data['maxwords'])
            corpus = data['corpus']
            data_response = data['dataResponse']
            custom_blocked_words = []
            if len(data['words']):
                custom_blocked_words = data['words'].replace(" ", "").split(",")
            unique_filename = str(uuid.uuid4())

            if app_link == '' and data_response is None:
                retJson = {
                    "type": "error",
                    "message": "empty link and you haven't got previous results to change the mask "
                }

                return jsonify(retJson)

            if color == 'default':
                color = None

            if font_ == 'default':
                font = None
            else:
                font = 'font/{}.ttf'.format(font_)
                if os.path.isfile(font):
                    pass
                else:
                    font = 'font/{}.ttc'.format(font_)

            if data_response is not None and app_link == '':
                change_mask = True
            else:
                change_mask = False

            if change_mask:
                search_results = data_response['search_results']
                for key, value in search_results.items():
                    if key == 'histogram_image':
                        continue
                    os.remove(value)

            final_words, search_results = run_analysis(app_link, unique_filename, mask, color, font, maxwords, corpus, custom_blocked_words, data_response, change_mask)

            retJson = {
                "type": "success",
                "final_words": final_words,
                "search_results": search_results,
                "message": "Relevant cards fetched successfully!"
            }

            return jsonify(retJson)

        except Exception as err:
            print("Error: ", err)
            retJson = {
                "type": "error",
                "message": str(err)
            }
            return jsonify(retJson)