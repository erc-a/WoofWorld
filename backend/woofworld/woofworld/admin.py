from pyramid.view import view_config
from pyramid.response import Response
from ..models import User, DogBreed, Fact, Video
from sqlalchemy import func
from datetime import datetime, timedelta

@view_config(route_name='admin_stats', renderer='json')
def get_admin_stats(request):
    dbsession = request.dbsession
    
    stats = {
        'totalUsers': dbsession.query(func.count(User.id)).scalar(),
        'totalBreeds': dbsession.query(func.count(DogBreed.id)).scalar(),
        'totalFacts': dbsession.query(func.count(Fact.id)).scalar(),
        'totalVideos': dbsession.query(func.count(Video.id)).scalar()
    }
    
    return stats

@view_config(route_name='admin_breeds', renderer='json', request_method='GET')
def list_breeds(request):
    breeds = request.dbsession.query(DogBreed).all()
    return [breed.__json__() for breed in breeds]

@view_config(route_name='admin_breeds', renderer='json', request_method='POST')
def add_breed(request):
    breed = DogBreed(**request.json_body)
    request.dbsession.add(breed)
    return breed.__json__()