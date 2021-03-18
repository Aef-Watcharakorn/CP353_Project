from flask_sqlalchemy import SQLAlchemy

 
db = SQLAlchemy()

class Developer(db.Model):        # Class User สืบทอดมาจาก UserMixin ต้องทำเวลาเราใช้ flask login
    ID = db.Column(db.Integer, primary_key=True) 
    Name = db.Column(db.String(100))
    Std_id = db.Column(db.Integer)
    Picture = db.Column(db.String(100))
    Facebook = db.Column(db.String(100))
    IG = db.Column(db.String(100))
