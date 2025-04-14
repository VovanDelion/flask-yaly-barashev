from flask_restful import Resource, abort
from flask import jsonify
from app.models.db_session import db_session
from app.models.job import Job
from app.parsers.job_parser import job_parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Job).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        return jsonify({'job': job.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Job).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = job_parser.parse_args()
        session = db_session.create_session()
        job = session.query(Job).get(job_id)

        job.team_leader = args['team_leader']
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        if args['start_date']:
            job.start_date = args['start_date']
        if args['end_date']:
            job.end_date = args['end_date']
        if args['is_finished'] is not None:
            job.is_finished = args['is_finished']

        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Job).all()
        return jsonify({'jobs': [job.to_dict() for job in jobs]})

    def post(self):
        args = job_parser.parse_args()
        session = db_session.create_session()

        job = Job(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args.get('is_finished', False)
        )

        if args['start_date']:
            job.start_date = args['start_date']
        if args['end_date']:
            job.end_date = args['end_date']

        session.add(job)
        session.commit()
        return jsonify({'id': job.id}), 201