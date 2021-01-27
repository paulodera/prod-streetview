from sqlalchemy.dialects.postgresql import UUID
from application import db
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


class Auth(Base):

    __tablename__ = "auth"

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    authenticated = db.Column(
        db.Boolean,
        default=True
    )

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.authenticated = True

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
