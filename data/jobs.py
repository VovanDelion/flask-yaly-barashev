import sqlalchemy
from .db_session import SqlAlchemyBase


jobs_to_category = sqlalchemy.Table(
    'jobs_to_category', SqlAlchemyBase.metadata,
    sqlalchemy.Column('job_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('category_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
)


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("martians.id"))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date =sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    leader = sqlalchemy.orm.relationship("User")
    department_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("departments.id"))
    department = sqlalchemy.orm.relationship("Department", back_populates="jobs")
    categories = sqlalchemy.orm.relationship(
        "Category",
        secondary=jobs_to_category,
        backref="jobs"
    )


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("martians.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    jobs = sqlalchemy.orm.relationship("Jobs", back_populates="department")
    leader = sqlalchemy.orm.relationship("User")


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
