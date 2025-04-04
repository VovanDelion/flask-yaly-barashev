import flask

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    jobs = db_session.create_session().query(Jobs).all()
    return flask.jsonify({
        "jobs": [j.to_dict(only=("job",
                                 "work_size",
                                 "colobaratoras",
                                 "leader.name",
                                 "is_finished")) for j in jobs]
    })

@blueprint.route('/api/jobs.<int:job_id>')
def get_jobs_by_id(job_id):
    job = db_session.create_session().get(Jobs, job_id)
    if job:
        return flask.jsonify({job})
    else:
        flask.make_response(flask.jsonyfy({"error": "Not Found"}))

@blueprint.errorhandler(404)
def not_found():
    return flask.make_response(flask.jsonyfy({"error": "Not Found"}))