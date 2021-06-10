from src import db
from src.models.model_base import ModelBase


class SiteModel(ModelBase):
    __tablename__ = 'sites'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.String(80), nullable=True)
    zip = db.Column(db.String(80), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    lat = db.Column(db.String(80), nullable=True)
    lon = db.Column(db.String(80), nullable=True)
    time_zone = db.Column(db.String(80), nullable=True)
