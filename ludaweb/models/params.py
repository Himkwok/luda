from ludaweb.models.models import db


class Param(db.Model):
    __tablename__ = 'params'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appId = db.Column(db.String(255),   db.ForeignKey('applications.appId'))
    argName = db.Column(db.String(255), nullable=False)

    require = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<Param %r>' % self.argName
