from flask_restful import Resource
from models.event import EventModel

from flask import request
import json


class Event(Resource):
    """ Parser """
    def parse_to_new_event(self, query):
        data = request.data.decode('utf-8')
        data_dic = json.loads(data)
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
            return event.json()
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


class eventList(Resource):
    """ GET """
    def get(self):
        return {'events': [event.json() for event in EventModel.query.order_by(EventModel.eventID).all()]}
    """ GET """

# # # # # #
# # # # # class eventByDate(Resource):
# # # #     """ GET """
# # #     def get(self, query):
# #         return {'event': [event.json() for event in EventModel.find_by_date(query).all()]}
#     """ GET """
