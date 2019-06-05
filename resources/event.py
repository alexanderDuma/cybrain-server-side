from flask_restful import Resource
from models.event import EventModel
from sqlalchemy import text
from flask import request, render_template, make_response, send_file, send_from_directory
import json
from db import db


class Event(Resource):
    """ Parser """
    def parse_to_new_event(self, query):
        data_dic = request.form
        # data = request.data.decode('utf-8')
        # data_dic = json.loads(data)
        event = EventModel(
            data_dic["date"],
            data_dic["adv_origin"],
            data_dic["adv_organization"],
            data_dic["adv_camp"],
            data_dic["target_sector"],
            data_dic["target_name"],
            data_dic["target_origin"],
            data_dic["reference"],
            data_dic["status"],
            data_dic["details"],
            data_dic["type"],
            data_dic["reporter"]
        )
        return event

    def update_event(self, event):
        data = request.data.decode('utf-8')
        data_dic = json.loads(data)
        event.eventID = data_dic["eventID"]
        event.date = data_dic["date"]
        event.adv_origin = data_dic["adv_origin"]
        event.adv_organization = data_dic["adv_organization"]
        event.adv_camp = data_dic["adv_camp"]
        event.target_sector = data_dic["target_sector"]
        event.target_name = data_dic["target_name"]
        event.target_origin = data_dic["target_origin"]
        event.reference = data_dic["reference"]
        event.status = data_dic["status"]
        event.details = data_dic["details"]
        event.type = data_dic["type"]
        event.reporter = data_dic["reporter"]
        return event

    """ Parser """

    """ GET """
    def get(self, query):
        event = EventModel.find_by_id(query)
        if event:
            return event.json()
        return {'message': 'event not found'}, 404
    """ GET """



    """ POST """
    def post(self, query):
        event = self.parse_to_new_event(query)
        currentEvent = EventModel.find_by_reference(event.reference)
        if not currentEvent:
            try:
                event.save_to_db()
            except:
                return {"message": "An error occurred inserting the item."}, 500
            events = [event.json() for event in EventModel.query.order_by(EventModel.eventID).all()]
            headers = {'content-type': 'text/html'}
            return make_response(render_template("events.html", events=events), 200, headers)
            # return event.json()
        return {'message': 'event by that reference already exists'}, 400
    """ POST """

    """ DELETE """
    def delete(self, query):
        event = EventModel.find_by_id(query)
        if event:
            event.delete_from_db()
            return {'message': 'event deleted'}
        return {'message': 'event couldn\'t be found'}
    """ DELETE """

    """ PUT """
    def put(self, query):
        event = EventModel.find_by_id(query)
        if event:
            event = self.update_event(event)
        else:
            event = self.parse_to_new_event(query)
        event.save_to_db()
        return event.json()

    """ PUT """


class EventFeed(Resource):
    def get(self):
        headers = {'content-type': 'text/html'}
        return make_response(render_template("event_feed.html"), 200, headers)


class eventList(Resource):
    """ GET """
    def get(self):
        events = [event.json() for event in EventModel.query.order_by(EventModel.eventID).all()]
        headers = {'content-type': 'text/html'}
        return make_response(render_template("events.html", events=events), 200, headers)
    """ GET """


class getLastEvent(Resource):
    """ GET """
    def get(self):
        return EventModel.query.order_by(EventModel.id.desc()).first()
    """ GET """


class getUniqueColumn(Resource):
    """ GET """
    def get(self):
        column = request.args.get('column')
        if column:
            query = f"SELECT DISTINCT {column} FROM data.Events"
            sql_query = text(query)
            result = db.engine.execute(sql_query)
            names = [row[0] for row in result]

            return names
        else:
            return {'message': 'No such column.'}
    """ GET """


class getAllUniqueColumns(Resource):
    """ GET """
    def get(self):
        result = {}
        columns = ['date', 'adv_origin', 'adv_organization', 'adv_camp', 'target_sector', 'target_name', 'target_origin', 'reference', 'status', 'details', 'type', 'reporter']
        for column in columns:
            query = f"SELECT DISTINCT {column} FROM data.Events"
            sql_query = text(query)
            result[column] = db.engine.execute(sql_query)
            result[column] = [row[0] for row in result[column]]

        return result
    """ GET """


class getByParameters(Resource):
    """ GET """
    def get(self):
        dic = {}
        date = request.args.get('date')
        if date:
            dic["date"] = date.split(',')
        adv_origin = request.args.get('adv_origin')
        if adv_origin:
            dic["adv_origin"] = adv_origin.split(',')
        adv_organization = request.args.get('adv_organization')
        if adv_organization:
            dic["adv_organization"] = adv_organization.split(',')
        adv_camp = request.args.get('adv_camp')
        if adv_camp:
            dic["adv_camp"] = adv_camp.split(',')
        target_sector = request.args.get('target_sector')
        if target_sector:
            dic["target_sector"] = target_sector.split(',')
        target_name = request.args.get('target_name')
        if target_name:
            dic["target_name"] = target_name.split(',')
        target_origin = request.args.get('target_origin')
        if target_origin:
            dic["target_origin"] = target_origin.split(',')
        reference = request.args.get('reference')
        if reference:
            dic["reference"] = reference.split(',')
        status = request.args.get('status')
        if status:
            dic["status"] = status.split(',')
        details = request.args.get('details')
        if details:
            dic["details"] = details.split(',')
        type = request.args.get('type')
        if type:
            dic["type"] = type.split(',')
        reporter = request.args.get('reporter')
        if reporter:
            dic["reporter"] = reporter.split(',')


        query = "SELECT * FROM data.Events WHERE "
        for k,v in dic.items():
            if len(v) == 1:
                query += f"{k} = '{v[0]}' AND "
            else:
                query += '('
                for value in v:
                    query += f"{k} = '{value}' OR "
                query = query[:-4]
                query += ") AND "
        query = query[:-5]

        sql_query = text(query)
        result = db.engine.execute(sql_query)
        events = [EventModel.find_by_id(row[0]).json() for row in result]
        headers = {'content-type': 'text/html'}

        return make_response(render_template("events.html", events=events), 200, headers)
    """ GET """


class Dashboard(Resource):
    def get(self):
        result = {}
        columns = ['date', 'adv_origin', 'adv_organization', 'adv_camp', 'target_sector', 'target_name',
                   'target_origin', 'reference', 'status', 'details', 'type', 'reporter']
        for column in columns:
            query = f"SELECT DISTINCT {column} FROM data.Events"
            sql_query = text(query)
            result[column] = db.engine.execute(sql_query)
            result[column] = [row[0] for row in result[column]]

        headers = {'content-type': 'text/html'}
        return make_response(render_template("dashboard.html",col_list=result), 200, headers)


class Login(Resource):
    def get(self):
        headers = {'content-type': 'text/html'}
        return make_response(render_template("index.html"), 200, headers)


class GetImage(Resource):
    def get(self):
        return send_file(r'C:\Users\brain\PycharmProjects\cybrain-server-side\templates\imgs\cybrain_logo.jpg', mimetype='image/gif')


class GetJS(Resource):
    def get(self):
        # return send_from_directory("C:/Users/brain/PycharmProjects/cybrain-server-side/templates/style/", "script.js")
        headers = {'content-type': 'text/js'}
        return send_file(r'C:\Users\brain\PycharmProjects\cybrain-server-side\templates\style\script.js',headers)


class GetCSS(Resource):
    def get(self):
        # return send_from_directory("C:/Users/brain/PycharmProjects/cybrain-server-side/templates/style/", "style.css")
        headers = {'content-type': 'text/css'}
        return send_file(r'C:\Users\brain\PycharmProjects\cybrain-server-side\templates\style\style.css', headers)
