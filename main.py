#!/usr/bin/python3
'''Script to display the error message'''
from flask import Flask, render_template
from urllib.request import Request, urlopen
import json
import urllib.error


app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


url = "https://comicvine.gamespot.com/api/"
url_issue = "https://comicvine.gamespot.com/api/issue/4000-"
url_characters = "https://comicvine.gamespot.com/api/characters/"
url_teams = "https://comicvine.gamespot.com/api/teams/"
url_locations = "https://comicvine.gamespot.com/api/locations/"
url_concepts = "https://comicvine.gamespot.com/api/concepts/"
api = "?api_key=6f7e42c1a04a1903ca5c2a635e441781e12a537b"
resources = ["characters", "issues", "publishers", "series",
             "series_List", "teams", "volumes", "search"]

@app.route('/')
def index():
    """
        Method to render the Issues
        fields : id, date_added, image(url), volume, issue_number
        sort   : date_added
        format : json
    """

    items = {}
    fields = "&field_list=name,id,date_added,image,volume,issue_number&sort=date_added:desc&format=json"

    req = Request("{}{}/{}{}".format(url, resources[1], api, fields))
    with urlopen(req) as res:
        Issues = json.loads(res.read().decode('utf-8'))

    items['issues'] = Issues.get('results')
    for item in items['issues']:
        print(item)
        print("--------------------------")
    return render_template('issues.html', items=items['issues'])


@app.route('/description/<id>')
def description(id):
    """
        Method to render the description of the Issue
        fields : location_credits, character_credits,
                 team_credits, concept_credits, description
        format : json
    """

    id_characters = {}
    items = {}
    items['characters'] = []
    items['teams'] = []
    items['locations'] = []
    items['concepts'] = []
    fields = "&field_list=location_credits,character_credits,team_credits,\
concept_credits,image&format=json"
    filters = ["&filter=id:"]
    req = Request("{}{}/{}{}".format(url_issue, id, api, fields))
    with urlopen(req) as res:
        Issues = json.loads(res.read().decode('utf-8'))

    image_url = Issues.get('results')['image']['medium_url']


    for id_character in (Issues.get('results')['character_credits']):
        req_char = Request("{}{}{}{}{}".format(url_characters, api, filters[0], id_character['id'], "&format=json"))
        with urlopen(req_char) as res_c:
            res_characters = json.loads(res_c.read().decode('utf-8'))
            if len(res_characters['results']):
                items['characters'].append({'name' : res_characters['results'][0]['name'],
                                      'img_url' : res_characters['results'][0]['image']['icon_url']})


    for id_team in (Issues.get('results')['team_credits']):
        req_team = Request("{}{}{}{}{}".format(url_teams, api, filters[0], id_team['id'], "&format=json"))
        with urlopen(req_team) as res_t:
            res_teams = json.loads(res_t.read().decode('utf-8'))
            if len(res_teams['results']):
                items['teams'].append({'name' : res_teams['results'][0]['name'],
                                  'img_url' : res_teams['results'][0]['image']['icon_url']})


    for id_location in (Issues.get('results')['location_credits']):
        req_location = Request("{}{}{}{}{}".format(url_locations, api, filters[0], id_location['id'], "&format=json"))
        with urlopen(req_location) as res_l:
            res_locations = json.loads(res_l.read().decode('utf-8'))
            if len(res_locations['results']):
                items['locations'].append({'name' : res_locations['results'][0]['name'],
                                  'img_url' : res_locations['results'][0]['image']['icon_url']})


    for id_concepts in (Issues.get('results')['concept_credits']):
        req_concepts = Request("{}{}{}{}{}".format(url_locations, api, filters[0], id_concepts['id'], "&format=json"))
        with urlopen(req_concepts) as res_c:
            res_concepts = json.loads(res_c.read().decode('utf-8'))
            if len(res_concepts['results']):
                items['concepts'].append({'name' : res_concepts['results'][0]['name'],
                                  'img_url' : res_concepts['results'][0]['image']['icon_url']})

    return render_template('description.html', items=items, image_url=image_url)
    #return items

if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
