from forms import *
from models import *

admin = User.query.filter_by(email='admin@travely.lv').first()
admin.role_id = 1
db.session.commit()
