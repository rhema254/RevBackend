""" To avoid relative imports, create a new file exts.py and import sqlalchemy class there and 
    create a db instance. Do not specify the db variable so that it becomes a global variable
    so that it can be accessed from other parts in the code.
"""

from exts import db
from datetime import datetime

class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirement = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float(10, 2))
    posted_by = db.Column(db.String(100))
    posted_date = db.Column(db.DateTime, default=db.func.now())
    closing_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Open')
    job_type = db.Column(db.Enum('remote', 'part-time', 'full-time', 'contract'))
    job_level = db.Column(db.Enum('senior', 'beginner', 'intermediate', 'advanced'))
    request = db.Column(db.Boolean, default=False)
 
    def __repr__(self):
        return f"< Job {self.title} >"
    
    #Convenience Methods
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title,description, requirement, location, salary, posted_by, closing_date, status, job_type, job_level):
        self.title = title
        self.description = description
        self.requirement = requirement
        self.location = location
        self.salary = salary
        self.posted_by = posted_by
        self.closing_date = closing_date
        self.status = status
        self.job_type = job_type
        self.job_level = job_level
        db.session.commit()

    def verify(self, title,description, location, salary, posted_by, closing_date, status, job_type, job_level, request, website):
        self.request = True
        self.title = title
        self.description = description
        self.location = location
        self.salary = salary
        self.posted_by = posted_by
        self.closing_date = closing_date
        self.status = status
        self.job_type = job_type    
        self.job_level = job_level
        self.website = website

        db.session.commit() 

class subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Subscriber {self.email}>"
    
    #Convenience Methods

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self, email):
        self.email = email

