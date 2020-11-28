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

    def __int__(self, name, time, description):
        self.name = name
        self.time = time
        self.description = description

    def __repr__(self):
        return "<Treasure %r>" % self.name