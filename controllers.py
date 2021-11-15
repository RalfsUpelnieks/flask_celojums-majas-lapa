from models import Agency, Trip

def get_agencies():
    return Agency.query.all()

def get_trips():
    return Trip.query.all()
