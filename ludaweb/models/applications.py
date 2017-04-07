from ludaweb.models.models import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appId = db.Column(db.String(255), nullable=False)
    appName = db.Column(db.String(255), nullable=False)
    appDes = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    xybz = db.Column(db.Integer(), nullable=False)

    args = db.relationship('Param', backref='applications')

    def __repr__(self):
        return '<Application %r>' % self.appName

    def to_json(self):
        return {
            'id': self.id,
            'appId': self.appId,
            'appName':  self.appName,
            'appDes': self.appDes,
            'url': self.url,
            'xybz': self.xybz,
        }