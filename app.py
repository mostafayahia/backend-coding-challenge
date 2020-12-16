import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import sys
import json
import requests

from github_query_params import (
    ORDER, PAGE, PER_PAGE, SORT, MAX_PER_PAGE
)

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    @app.route('/trending_repos', methods=['GET'])
    def retrieve_trending_repos():

        # 'repos_num' query param that was sending for our api is useful for testing
        # few etries and getting more control for the data which is fetched
        per_page = request.args.get('repos_num', PER_PAGE, int)

        # if requested repos > MAX_PER_PAGE, Will be considered 404 error
        if (per_page > MAX_PER_PAGE):
            abort(404)

        today = datetime.today()

        # construct the url to retrieve the data from github api
        # get all repos which was created since month ago from today
        url = 'https://api.github.com/search/repositories?' + \
            'q=created:%3E' + '{}-{}-{}'.format(today.year, 12 if today.month == 1 else today.month - 1, today.day) + \
            '&sort=' + SORT + \
            '&order=' + ORDER + \
            '&page=' + str(PAGE) + \
            '&per_page=' + str(per_page)

        data = json.loads(requests.get(url).text)['items']

        # extract from every entry -> the language and the coresponding repo for this language
        # using this info to construct our dictionary to send it as a response
        language_dict = {}
        for e in data:
            if not e['language']:
                continue
            language = e['language'].lower().strip()
            repo_url = e['html_url']
            repo_url_list = language_dict.get(language, [])
            repo_url_list.append(repo_url)
            language_dict[language] = repo_url_list

        return jsonify({
            'success': True,
            'repos': [
                {
                    'language': language,
                    'count': len(language_dict[language]),
                    'repos': language_dict[language]
                } for language in language_dict
            ]
        })

    # handling errors

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
