from builtins import type

from db import db


class EventModel(db.Model):
    __tablename__= 'Events'

    """ Attribures """
    eventID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    adv_origin = db.Column(db.String(200), nullable=False)
    adv_organization = db.Column(db.String(200), nullable=False)
    adv_camp = db.Column(db.String(200), nullable=False)
    target_sector = db.Column(db.String(200), nullable=False)
    target_name = db.Column(db.String(200), nullable=False)
    target_origin = db.Column(db.String(200), nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    details = db.Column(db.String(800), nullable=False)
    type = db.Column(db.String(200), nullable=False)
    reporter = db.Column(db.String(200), nullable=False)
    """ Attribures """

    """ CTOR """
    def __init__(self,
                 date,
                 adv_origin,
                 adv_organization,
                 adv_camp,
                 target_sector,
                 target_name,
                 target_origin,
                 reference,
                 status,
                 details,
                 type,
                 reporter
                 ):
        self.date = date
        self.adv_origin = adv_origin
        self.adv_organization = adv_organization
        self.adv_camp = adv_camp
        self.target_sector = target_sector
        self.target_name = target_name
        self.target_origin = target_origin
        self.reference = reference
        self.status = status
        self.details = details
        self.type = type
        self.reporter = reporter
    """ CTOR """

    """ JSON """
    def json(self):
        return {
            'eventID': self.eventID,
            'date': self.date,
            'adv_origin': self.adv_origin,
            'adv_organization': self.adv_organization,
            'adv_camp': self.adv_camp,
            'target_sector': self.target_sector,
            'target_name': self.target_name,
            'target_origin': self.target_origin,
            'reference': self.reference,
            'status': self.status,
            'details': self.details,
            'type': self.type,
            'reporter': self.reporter
        }
    """ JSON """

    """ Class methods """
    @classmethod
    def find_by_id(cls, eventID):
        return cls.query.filter_by(eventID=eventID).first()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    @classmethod
    def find_by_adv_origin(cls, adv_origin):
        return cls.query.filter_by(adv_origin=adv_origin).all()

    @classmethod
    def find_by_adv_organization(cls, adv_organization):
        return cls.query.filter_by(adv_organization=adv_organization).all()

    @classmethod
    def find_by_adv_camp(cls, adv_camp):
        return cls.query.filter_by(adv_camp=adv_camp).all()

    @classmethod
    def find_by_target_sector(cls, target_sector):
        return cls.query.filter_by(target_sector=target_sector).all()

    @classmethod
    def find_by_target_name(cls, target_name):
        return cls.query.filter_by(target_name=target_name).all()

    @classmethod
    def find_by_origin(cls, target_origin):
        return cls.query.filter_by(target_origin=target_origin).all()

    @classmethod
    def find_by_reference(cls, reference):
        return cls.query.filter_by(reference=reference).all()

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).all()

    @classmethod
    def find_by_details(cls, details):
        return cls.query.filter_by(details=details).all()

    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(type=type).all()

    @classmethod
    def find_by_reporter(cls, reporter):
        return cls.query.filter_by(reporter=reporter).all()

    """ Class methods """

    """ DB methods """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    """ DB methods """