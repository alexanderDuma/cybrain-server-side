from flask_restful import Resource
from models.event import EventModel

from flask import request, render_template, make_response
import json


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
            return make_response(render_template("event_feed.html", events=events), 200, headers)
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

class GetEventByParamaters(Resource):
    """ GET """
    def get(self, query):

        date = request.args.get('date')
        adv_origin = request.args.get('adv_origin')
        adv_organization = request.args.get('adv_organization')
        adv_camp = request.args.get('adv_camp')
        target_sector = request.args.get('target_sector')
        target_name = request.args.get('target_name')
        target_origin = request.args.get('target_origin')
        reference = request.args.get('reference')
        status = request.args.get('status')
        details = request.args.get('details')
        type = request.args.get('type')
        reporter = request.args.get('reporter')

        if date:
            response = EventModel.query.filter_by(date=date)
        if adv_origin:
            response = EventModel.query.filter_by(adv_origin=adv_origin)


class eventList(Resource):
    """ GET """
    def get(self):
        events = [event.json() for event in EventModel.query.order_by(EventModel.eventID).all()]
        headers = {'content-type': 'text/html'}
        return make_response(render_template("event_feed.html", events=events), 200, headers)
    """ GET """


class getLastEvent(Resource):
    """ GET """
    def get(self):
        return EventModel.query.order_by(EventModel.id.desc()).first()
    """ GET """


class getByParameters(Resource):
    """ GET """
    def get(self):
        dic = []
        date = request.args.get('date')
        if date:
            dic.append({"date": date})
        adv_origin = request.args.get('adv_origin')
        if adv_origin:
            dic.append({"adv_origin": adv_origin})
        adv_organization = request.args.get('adv_organization')
        if adv_organization:
            dic.append({"adv_organization": adv_organization})
        adv_camp = request.args.get('adv_camp')
        if adv_camp:
            dic.append({"adv_camp": adv_camp})
        target_sector = request.args.get('target_sector')
        if target_sector:
            dic.append({"target_sector": target_sector})
        target_name = request.args.get('target_name')
        if target_name:
            dic.append({"target_name": target_name})
        target_origin = request.args.get('target_origin')
        if target_origin:
            dic.append({"target_origin": target_origin})
        reference = request.args.get('reference')
        if reference:
            dic.append({"reference": reference})
        status = request.args.get('status')
        if status:
            dic.append({"status": status})
        details = request.args.get('details')
        if details:
            dic.append({"details": details})
        type = request.args.get('type')
        if type:
            dic.append({"type": type})

        # return dic
        return EventModel.query.filter()
    """ GET """
