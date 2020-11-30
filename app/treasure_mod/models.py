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


class Treasure(Base):

    __tablename__ = 'treasure'

    name = db.Column(
        db.String(500),
        nullable=False,
        unique=True
    )
    time = db.Column(
        db.Integer,
        nullable=False
    )
    description = db.Column(
        db.Text,
        nullable=True
    )
    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __int__(self, name, time, description, is_active):
        self.name = name
        self.time = time
        self.description = description
        self.is_active = True

    """
    def __repr__(self):
        return "<Treasure %r>" % self.name
    """

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_active_hunts(cls):
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_treasure_details(cls, treasure_id):
        return cls.query.filter_by(id=treasure_id, is_active=True).first()
