from ..main import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.UnicodeText(500), index=True)
    password = db.Column(db.UnicodeText(500), index=True)
    credit_card = db.Column(db.UnicodeText(32))
    expiry = db.Column(db.DateTime)
    ccv = db.Column(db.Integer())
    balance = db.Column(db.Integer(), default=1000)
    #
    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    def is_active(self):
        return self.is_enabled

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
