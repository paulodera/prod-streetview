from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import ARRAY
from application import db
import sqlalchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects import postgresql as pg
# filter array columns
from sqlalchemy_filters import apply_filters


class Base(db.Model):

    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        default=sqlalchemy.text("uuid_generate_v4()"),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True
    )
    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    date_updated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class Clue(Base):

    __tablename__ = 'clue'

    treasure_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('treasure.id', ondelete='Cascade', onupdate='Cascade')
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    endpoint = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    startpoint = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    slug = db.Column(
        # # MutableList.as_mutable(db.PickleType),
        # # default=[]
        pg.ARRAY(db.String, dimensions=1),
        nullable=False
    )

    marker_pos = db.Column(
        db.String(150),
        nullable=False
    )

    is_correct = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    clue_options = db.relationship("ClueOptions", backref="clue")

    def __init__(self, treasure_id, description, endpoint, startpoint, slug, marker_pos, is_correct):
        self.treasure_id = treasure_id
        self.description = description
        self.endpoint = endpoint
        self.startpoint = startpoint
        self.slug = slug
        self.marker_pos = marker_pos
        self.is_correct = is_correct

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'endpoint': self.endpoint,
            'treasure_name': self.treasure.name,
            'startpoint': self.startpoint,
            'slug': self.slug,
            'marker_pos': self.marker_pos,
            'is_correct': self.is_correct,
            'options': [opt.serialize() for opt in self.clue_options]
        }
    
    def save(self):
        db.session.add(self)

    @classmethod
    def get_next_clue(cls, slug, treasure_id):
        query = db.session.query(Clue)
        filter_specs = [{'field': 'slug', 'op': 'any', 'value': slug}]
        result = apply_filters(query, filter_specs)
        more_filters = [{'field': 'treasure_id', 'op': '==', 'value': treasure_id}]
        next_clue = apply_filters(result, more_filters)
        return next_clue.first().serialize()

    @classmethod
    def get_clue(cls, treasure_id):
        return cls.query.filter_by(startpoint=True, treasure_id=treasure_id).first()

    @classmethod
    def get_option_clues(cls):
        return [(x.id, x.description) for x in cls.query.all()]

    @classmethod
    def return_to_start(cls, treasure_id):
        result = cls.query.filter_by(startpoint=False, endpoint=False, treasure_id=treasure_id, is_correct=True).first()
        return result.serialize()
    
    @classmethod
    def get_all_clues(cls):
        return [res.serialize() for res in cls.query.all()]
    
    @classmethod
    def get_clue_by_id(cls, clue_id):
        return cls.query.filter_by(id=clue_id).first()


class ClueOptions(Base):

    __tablename__ = 'clue_options'

    name = db.Column(
        db.String(500),
        nullable=False
    )

    clue_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('clue.id', ondelete='Cascade', onupdate='Cascade')
    )

    slug = db.Column(
        db.String(20),
        nullable=False
    )

    coordinates = db.Column(
        db.String(500),
        nullable = False
    )

    points = db.Column(
        db.Integer,
        nullable = False
    )

    is_correct = db.Column(
        db.Boolean,
        default=False
    )

    def __init__(self, name, clue_id, slug, coordinates, points, is_correct):
        self.name = name
        self.slug = slug
        self.clue_id = clue_id
        self.coordinatcoordinates =coordinates
        self.points = points
        self.is_correct = is_correct

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'clue': self.clue.description,
            'treasure': self.clue.treasure.name,
            'slug': self.slug,
            'points': self.points,
            'coordinates': self.coordinates,
            'is_correct': self.is_correct,
            'was_endpoint': self.clue.endpoint
        }
    
    def save(self):
        db.session.add(self)
    
    @classmethod
    def get_clue_options(cls, clue_id):
        return [c.serialize() for c in cls.query.filter_by(clue_id=clue_id).all()]

    @classmethod
    def get_start_position(cls, clue_id):
        data = cls.query.filter_by(clue_id=clue_id, is_correct=True).first()
        return data.coordinates

    @classmethod
    def get_clue_details(cls, option_id):
        res = cls.query.filter_by(id=option_id).first()
        return res.serialize()
    
    @classmethod
    def fetch_all_options(cls):
        return [res.serialize() for res in cls.query.all()]

    @classmethod
    def fetch_option_details(cls, option_id):
        return cls.query.filter_by(id=option_id).first()

