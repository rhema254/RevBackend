from flask import Flask, jsonify, render_template, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import *
from exts import db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)

app.config.from_object(DevConfig)
app.config['SQL_ALCHEMY_DATABASE_URI']= ('mysql+pymsql://mark:2580_Mark@localhost/rev_eng')

db.init_app(app)
CORS(app)


api = Api(app,doc='/docs')

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}

# Model to help us marshal/serialise/expose our model into json. 
job_model=api.model(
    "job",
    {
    "id": fields.Integer(),
    "title": fields.String(),
    "description": fields.String(),
    "requirement": fields.String(),
    "location": fields.String(),
    "salary": fields.Float(),
    "posted_by": fields.String(),
    "posted_date": fields.Date(),
    "closing_date": fields.Date(),
    "status": fields.String(),
    "job_type": fields.String(),
    "job_level": fields.String(),
    "request": fields.Boolean()

   }
)

subscriber_model = api.model(
    "subscribers",
    {
        "id": fields.Integer(),
        "email": fields.String(),
        "date": fields.DateTime()
    }
)


@api.route('/jobs')
class jobsResource(Resource):   
    
    @api.marshal_list_with(job_model)
    def get(self):
        """ Get all jobs"""
        jobs_list = jobs.query.filter_by(request = False).all()  
        return jobs_list
    

    @api.expect(job_model)
    @api.marshal_with(job_model)
    def post(self):
        """ Create a new job"""
        data = request.get_json()

        new_job = jobs(
            title=data.get('title'),
            description=data.get('description'),
            requirement=data.get('requirement'),
            location=data.get('location'),
            salary=data.get('salary'),
            posted_by=data.get('posted_by'),
            posted_date=data.get('posted_date'),
            closing_date=data.get('closing_date'),
            status=data.get('status', 'Open'),
            job_type=data.get('job_type'),
            job_level=data.get('job_level')
        )

        new_job.save()
        
        return new_job,200

@api.route('/jobs/<int:id>', methods =['GET', 'PUT', 'DELETE'])
class jobResoure(Resource):
    @api.marshal_with(job_model)
    def get(self, id):
        """ Get a single job"""
        job = jobs.query.get_or_404(id)
        return job

    @api.marshal_with(job_model)
    @api.expect(job_model)
    def put(self, id):
        """ Update a job"""
        job_to_update = jobs.query.get_or_404(id)
        data = request.get_json()
        
        job_to_update.update(
            title=data.get('title', job_to_update.title),
            description=data.get('description', job_to_update.description),
            requirement=data.get('requirement', job_to_update.requirement),
            location=data.get('location', job_to_update.location),
            salary=data.get('salary', job_to_update.salary),
            posted_by=data.get('posted_by', job_to_update.posted_by),
            closing_date=data.get('closing_date', job_to_update.closing_date),
            status=data.get('status', job_to_update.status),
            job_type=data.get('job_type', job_to_update.job_type),
            job_level=data.get('job_level', job_to_update.job_level)
            )
        return job_to_update

    @api.marshal_with(job_model)
    def delete(self, id):
        """ Delete a job"""
        job_to_delete = jobs.query.get_or_404(id)
        job_to_delete.delete()
        
        return job_to_delete

@app.shell_context_processor
def make_shell_context():
    return {
        'db':db,
        'jobs':jobs
    }

@app.route('/jobs/<int:id>', methods=['GET'])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'posted_by': job.posted_by,
        'location': job.location,
        'job_type': job.job_type,
        'level': job.level,
        'posted_date': job.posted_date.strftime('%Y-%m-%d'),
        'description': job.description,
    })

@api.route('/request', methods=['GET'])
class requestsResource(Resource):

    @api.marshal_list_with(job_model)
    def get(self):
        """ Get all job requests """
        request = jobs.query.filter_by(verified=False).all()

        return request, 200


@api.route('/requests/<int:id>', methods=['GET', 'PUT', 'DELETE'])  
class requestResource(Resource):
    
    @api.marshal_with(job_model)
    def get(self, id):
        """ Get a specific job """
    
        job = jobs.query.get_or_404(id)
        return job, 200 
    
    @api.marshal_with(job_model)
    def put(self, id):
        """ Update the 'Verify' column """

        job_to_verify = jobs.query.get_or_404(id)
        data = request.get_json()
        job_to_verify.verify(
            title=data.get('title', job_to_verify.title),
            description=data.get('description', job_to_verify.description),
            location=data.get('location', job_to_verify.location),
            salary=data.get('salary', job_to_verify.salary),
            posted_by=data.get('posted_by', job_to_verify.posted_by),
            closing_date=data.get('closing_date', job_to_verify.closing_date),
            status=data.get('status', job_to_verify.status),
            job_type=data.get('job_type', job_to_verify.job_type),
            job_level=data.get('job_level', job_to_verify.job_level),
            verified=data.get('verified', job_to_verify.verified),
            website=data.get('website', job_to_verify.website)
        )

        return job_to_verify, 200
    
    @api.marshal_with(job_model)
    def delete(self, id):
        """ Delete a Job Request """

        job_to_delete = jobs.query.get_or_404(id)
        job_to_delete.delete()

        return job_to_delete, 200 

@api.route('/subscribers')
class newsletterResource(Resource):
    
    @api.expect(subscriber_model)
    @api.marshal_with(subscriber_model)
    def post(self):
        """ Subscribe to our newsletter"""
        data = request.get_json()   
        new_subscriber = subscribers(email=data.get('email'))

        new_subscriber.save()

        return new_subscriber, 200
    
    @api.marshal_list_with(subscriber_model)
    def get(self):
        
        subscription_list = subscribers.query.all()

        return subscription_list

    @api.marshal_with(subscriber_model)
    def delete(self, id):
        email_to_delete = subscribers.query.get_or_404(id)
        email_to_delete.delete()

        return email_to_delete
@api.route('/partners')
class partnersResource(Resource):

    @api.expect(job_model)
    @api.marshal_with(job_model)
    def post(self):
        """ Creating a new Advert  """
        data = request.get_json()
        new_advert = jobs(
            title=data.get('title'),
            description=data.get('description'),
            requirement=data.get('requirement'),
            location=data.get('location'),
            salary=data.get('salary'),
            posted_by=data.get('posted_by'),
            posted_date=data.get('posted_date'),
            closing_date=data.get('closing_date'),
            status=data.get('status', 'Open'),
            job_type=data.get('job_type'),
            job_level=data.get('job_level'), 
            website = data.get('website'),
            verified = False
        )

        new_advert.save()

        return new_advert, 
    
    @api.marshal_list_with(job_model)
    def get(self):
        """" Get the list of all job advert requests"""
        jobs_list = jobs.query.filter_by(verified=False).all()

        return jobs_list,200
    
    
    @api.marshal_list_with(job_model)
    def get_adverts(self):
        """" Get the list of all verified gigs """
        adverts = jobs.query.filter_by(verified=False).all() 

        return adverts, 200

# @app.route('/jobs')
# def get_jobs():
#     return jobsResource


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()