from sqlalchemy.dialects.postgresql import UUID
from app import db
import sqlalchemy


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
        db.String(20),
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
            'description': self.description,
            'endpoint': self.endpoint,
            'startpoint': self.startpoint,
            'slug': self.slug,
            'marker_pos': self.marker_pos,
            'is_correct': self.is_correct,
            'options': [opt.serialize() for opt in self.clue_options]
        }

    @classmethod
    def get_next_clue(cls, slug, treasure_id):
        res = cls.query.filter_by(slug=slug, treasure_id=treasure_id).first()
        if res:
            return res.serialize()
        else:
            return None

    @classmethod
    def get_clue(cls, treasure_id):
        return cls.query.filter_by(startpoint=True, treasure_id=treasure_id).first()


class ClueOptions(Base):

    __tablename__ = 'clue_options'

    name = db.Column(
        db.String(500),
        nullable=False,
        unique=True
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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'points': self.points,
            'coordinates': self.coordinates,
            'is_correct': self.is_correct,
            'was_endpoint': self.clue.endpoint
        }

    @classmethod
    def get_clue_options(cls, clue_id):
        return [c.serialize() for c in cls.query.filter_by(clue_id=clue_id).all()]

    @classmethod
    def get_clue_details(cls, option_id):
        res = cls.query.filter_by(id=option_id).first()
        return res.serialize()