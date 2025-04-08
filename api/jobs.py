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

@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonyfy({"error": "Error adding job"}), 400)
    if not all(key in ["job","work_size","colobaratoras","leader.name", "is_finished"] for key in flask.request.json.keys()):
        return flask.make_response(flask.jsonyfy({"error": "Error adding job"}), 400)
    job = Jobs()
    job.job = flask.request.json["job"]
    job.work_size = int(flask.request.json["work_size"])
    job.collaborators = flask.request.json["collaborators"]
    job.is_finished = flask.request.json["is_finished"]
    job.team_leader = flask.request.json["team_leader"]

    sess = db_session.create_session()
    sess.add(job)
    sess.commit()

    return flask.make_response(flask.jsonyfy({"ok": str(job.id)}), 201)

@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    sess = db_session.create_session()
    job = sess.get(Jobs, job_id)

    if not job:
        return flask.make_response(flask.jsonify({"error": "Not Found"}), 404)
        sess.delete(job)
        sess.commit()

    return flask.make_response(flask.jsonify({"success": f"Job {job_id} deleted"}), 200)