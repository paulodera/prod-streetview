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

    player_scores = db.relationship("PlayerLeaderboard", backref="player")

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def serialize(self):
        return {
            'name': self.name,
            'phone': self.phone
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_players(cls):
        return [p.serialize() for p in cls.query.all()]


class PlayerLeaderBoard(Base):

    __tablename__ = 'player_leaderboard'

    treasure_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('treasure.id', ondelete='Cascade', onupdate='Cascade')
    )

    time = db.Column(
        db.Integer,
        nullable = False
    )

    points = db.Column(
        db.Integer,
        nullable = False
    )

    player_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('player.id', ondelete='Cascade', onupdate='Cascade')
    )
