from flask_sqlalchemy import SQLAlchemy
from typing import Optional

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rules.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rule_string = db.Column(db.Text, nullable=False)
    rule_tree = db.Column(db.Text, nullable=False)

class Node:
    def __init__(self, left: Optional['Node'] = None, right: Optional['Node'] = None, value: Optional[str] = None):
        self.left = left
        self.right = right
        self.value = value