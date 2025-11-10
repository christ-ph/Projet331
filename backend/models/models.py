from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash , check_password_hash

db=SQLAlchemy()
# ===== Enums =====
class UserRole(Enum):
    FREELANCE = "FREELANCE"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"

class Availability(Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    PART_TIME = "PART_TIME"


class MissionStatus(Enum):
    DRAFT="DRAFT"
    PUBLISHED = "PUBLISHED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"

class ApplicationStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


# ===== Models =====
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.FREELANCE, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    freelance_profile = db.relationship("FreelanceProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    client_profile = db.relationship("ClientProfile",  back_populates="user", uselist=False, cascade="all, delete-orphan")
    missions_created = db.relationship("Mission", back_populates="client", foreign_keys="Mission.client_id")
    applications = db.relationship("Application", back_populates="freelance")
    sent_messages = db.relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = db.relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class FreelanceProfile(db.Model):
    __tablename__ = 'freelance_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)

    try:
        skills = db.Column(ARRAY(db.String), default=list)
    except Exception:
        skills = db.Column(db.JSON, default=list)

    hourly_rate = db.Column(db.Float, nullable=True)
    availability = db.Column(db.Enum(Availability), default=Availability.AVAILABLE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    portfolio_items = db.relationship("PortfolioItem", backref="freelance_profile", cascade="all, delete-orphan")
    user = db.relationship("User", back_populates="freelance_profile", uselist=False)

    def to_dict(self, include_user=False, include_portfolio=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "description": self.description,
            "skills": self.skills or [],
            "hourly_rate": self.hourly_rate,
            "availability": self.availability.value if self.availability else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id
        }
        if include_user and self.user:
            data["user"] = self.user.to_dict()
        if include_portfolio:
            data["portfolio_items"] = [p.to_dict() for p in self.portfolio_items]
        return data

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    project_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    freelance_profile_id = db.Column(db.Integer, db.ForeignKey('freelance_profiles.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "project_url": self.project_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "freelance_profile_id": self.freelance_profile_id
        }

class ClientProfile(db.Model):
    __tablename__ = 'client_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    user = db.relationship("User", back_populates="client_profile", uselist=False)
    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "description": self.description,
            "user_id": self.user_id
        }


class Mission(db.Model):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    budget_type = db.Column(db.String(50), default='FIXED')  # FIXED, HOURLY
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(MissionStatus), default=MissionStatus.DRAFT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client = db.relationship("User", back_populates="missions_created", foreign_keys=[client_id])
    applications = db.relationship("Application", back_populates="mission", cascade="all, delete-orphan")
    required_skills = db.Column(db.JSON, default=list)  # Liste des compétences requises

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "budget": self.budget,
            "budget_type": self.budget_type,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status.value if self.status else None,
            "client_id": self.client_id,
            "client": self.client.to_dict() if self.client else None,
            "required_skills": self.required_skills,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "applications_count": len(self.applications)
        }

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proposal = db.Column(db.Text, nullable=False)
    proposed_budget = db.Column(db.Float)
    delivery_time = db.Column(db.String(100))
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=False)
    freelance_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    mission = db.relationship("Mission", back_populates="applications")
    freelance = db.relationship("User", back_populates="applications")

    def to_dict(self):
        return {
            "id": self.id,
            "proposal": self.proposal,
            "proposed_budget": self.proposed_budget,
            "delivery_time": self.delivery_time,
            "status": self.status.value if self.status else None,
            "mission_id": self.mission_id,
            "freelance_id": self.freelance_id,
            "freelance": self.freelance.to_dict() if self.freelance else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=True)

    sender = db.relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = db.relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])
    mission = db.relationship("Mission")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_read": self.is_read,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "mission_id": self.mission_id,
            "sender": self.sender.to_dict() if self.sender else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }