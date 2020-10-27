# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import getpass
import json
import requests as req
from flask import Flask, render_template, request, jsonify, g, redirect, url_for, send_from_directory
from functools import lru_cache

# ----------------------------------------------------------------------------#
# Configs
# ----------------------------------------------------------------------------#

frontend_port = 5000
app = Flask(__name__, static_folder='static', template_folder='templates')

# TODO: Remove before prod
running_user = getpass.getuser()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
debug_mode = True

# ----------------------------------------------------------------------------#
# Renders
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("index.html", heroes=get_heroes())


# ----------------------------------------------------------------------------#
# API
# ----------------------------------------------------------------------------#


# ----------------------------------------------------------------------------#
# Helpers
# ----------------------------------------------------------------------------#

@lru_cache(maxsize=32)
def get_heroes():
    with open("data/heroes.json", "r") as fp:
        heroes = json.load(fp)

    # remove prefix from name, add avatar url
    for hero in heroes:
        hero["id"] = int(hero["id"])
        hero["name"] = str(hero["name"]).replace("npc_dota_hero_", "")
        hero["pretty_name"] = str(hero["name"].replace("_", " ").title())

    return heroes


if __name__ == '__main__':
    # Custom jinja functions
    # app.jinja_env.globals.update(prettify_float=prettify_float, prettify_label=prettify_label)
    app.jinja_env.cache = {}

    app.run(debug=debug_mode, host='127.0.0.1', port=frontend_port)
