import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase



class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    #id
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # team_leader (id) (id руководителя, целое число)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("martians.id"))
    # job (description) (описание работы)
    job = sqlalchemy.Column(sqlalchemy.String)
    # work_size (hours) (объем работы в часах)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    # collaborators (list of id of participants) (список id участников)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    # start_date (дата начала)
    start_date =sqlalchemy.Column(sqlalchemy.DateTime)
    # end_date (дата окончания)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    #is_finished (bool) (признак завершения)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    leader = sqlalchemy.orm.relationship("User")