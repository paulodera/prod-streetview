from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc
import uuid
from application import db
import sqlalchemy


class Base(db.Model):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
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

    player_leaderboard = db.relationship("PlayerLeaderBoard", backref="player")

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

    @classmethod
    def check_player_details(cls, phone):
        return cls.query.filter_by(phone=phone).first()


class PlayerLeaderBoard(Base):
    __tablename__ = 'player_leaderboard'

    treasure_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('treasure.id', ondelete='Cascade', onupdate='Cascade')
    )

    time = db.Column(
        db.String(50),
        nullable=False
    )

    points = db.Column(
        db.Integer,
        nullable=False
    )

    player_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('player.id', ondelete='Cascade', onupdate='Cascade')
    )

    def __init__(self, treasure_id, time, points, player_id):
        self.treasure_id = treasure_id
        self.time = time
        self.points = points
        self.player_id = player_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_play_status(cls, player_id, treasure_id):
        """
        check treasure hunt status of the player
        :return:
        """
        return cls.query.filter_by(treasure_id=treasure_id, player_id=player_id).first()

    @classmethod
    def get_player_rankings(cls):
        """
        generate player leaderboard on current active hunt
        {name, points}
        :return:
        """
        result = cls.query.filter().order_by(desc("points")).limit(5).all()
        filtered_result = [x for x in result if x.treasure.is_active == True]
        return filtered_result
