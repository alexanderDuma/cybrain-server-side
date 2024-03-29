from flask import Flask
from flask_restful import Api
from resources.event import *


"""Config"""
app = Flask(__name__)
""" will look for DATABAE_URL, if not found will take second arg. """
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://westbrook135:1q2w3e4r!@localhost/data'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
"""Config"""

""" If on server you should comment the next 8 lines"""
""" DB """


@app.before_first_request
def create_tables():
    db.create_all()


""" DB """

"""Api resources"""
api.add_resource(Event, '/event/<string:query>')
api.add_resource(eventList, '/events')
api.add_resource(getByParameters, '/event/getByParameters')
api.add_resource(getUniqueColumn, '/event/getUniqueColumn')
api.add_resource(getAllUniqueColumns, '/event/getAllUniqueColumns')
api.add_resource(EventFeed, '/event_feed')
api.add_resource(Dashboard, '/dashboard')
api.add_resource(Login, '/')
api.add_resource(GetImage, '/imgs/cybrain_logo.jpg')
api.add_resource(GetJS, '/style/script.js')
api.add_resource(GetCSS, '/style/style.css')
"""Api resources"""

""" Main """
if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(host='192.168.1.114', port=5000, debug=True)
""" Main """