from sqlalchemy.dialects.postgresql import UUID
from app import db
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.sql import label


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


class Player(Base):
    __tablename__ = 'player'

    name = db.Column(
        db.String(50),
        nullable=False
    )

    phone = db.Column(
        db.BIGINT,
        unique=True,
        nullable=False
    )

    player_scores = db.relationship("PlayerLeaderBoard", backref="player")

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def serialize(self):
        return {
            'name': self.name,
            'phone': self.phone
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_players(cls):
        return [p.serialize() for p in cls.query.all()]

    @classmethod
    def get_player_details(cls, phone):
        return cls.query.filter_by(phone=phone).first()


class PlayerLeaderBoard(Base):

    __tablename__ = 'player_leaderboard'

    treasure_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('treasure.id', ondelete='Cascade', onupdate='Cascade')
    )

    player_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('player.id', ondelete='Cascade', onupdate='Cascade')
    )

    time = db.Column(
        db.Integer,
        unique = True,
        nullable = False
    )

    points = db.Column(
        db.Integer,
        unique = True,
        nullable = False
    )

    def __init__(self, treasure_id, time, points, player_id):
        self.treasure_id = treasure_id
        self.time = time
        self.points =  points
        self.player_id = player_id

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_player_integrity(cls, treasure_id, player_id):
        return cls.query.filter_by(treasure_id=treasure_id, player_id=player_id).first()

    @classmethod
    def rank_players(cls):
        pass


