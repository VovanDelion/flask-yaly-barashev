from flask_restful import reqparse


job_parser = reqparse.RequestParser()
job_parser.add_argument('team_leader', required=True, type=int, help='Team leader id is required')
job_parser.add_argument('job', required=True, help='Job description is required')
job_parser.add_argument('work_size', required=True, type=int, help='Work size is required')
job_parser.add_argument('collaborators', required=True, help='Collaborators are required')
job_parser.add_argument('start_date', help='Start date (optional)')
job_parser.add_argument('end_date', help='End date (optional)')
job_parser.add_argument('is_finished', type=bool, help='Is job finished (optional)')