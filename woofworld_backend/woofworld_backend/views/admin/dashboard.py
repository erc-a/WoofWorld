from pyramid.view import view_config
from ...models import User, Fact, Video
from sqlalchemy import func
import logging

log = logging.getLogger(__name__)

@view_config(route_name='admin_stats', renderer='json', permission='admin_dashboard')
def admin_stats_view(request):
    try:
        dbsession = request.dbsession
        stats = {
            'totalUsers': dbsession.query(func.count(User.id)).scalar(),
            'totalBreeds': dbsession.query(func.count(DogBreed.id)).scalar(),
            'totalFacts': dbsession.query(func.count(Fact.id)).scalar(),
            'totalVideos': dbsession.query(func.count(Video.id)).scalar(),
            # Dummy data untuk recentActivities dan userGrowth, sesuaikan dengan logic sebenarnya
            'recentActivities': [
                {'id': 1, 'icon': '🐾', 'description': 'User baru mendaftar: John Doe', 'timestamp': '2023-05-27T10:00:00Z'},
                {'id': 2, 'icon': '🦴', 'description': 'Breed baru ditambahkan: Labrador', 'timestamp': '2023-05-27T09:30:00Z'}
            ],
            'userGrowth': [
                {'date': '2023-05-01', 'users': 10},
                {'date': '2023-05-15', 'users': 25},
                {'date': '2023-05-27', 'users': 40}
            ]
        }
        return stats
    except Exception as e:
        log.error(f"Error fetching admin stats: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil statistik admin.'}

@view_config(route_name='admin_analytics', renderer='json', permission='view_analytics')
def admin_analytics_view(request):
    # Implementasikan logic untuk mengambil data analytics
    # Ini hanya contoh data dummy
    try:
        analytics_data = {
            'userGrowth': [
                {'date': '2023-01-01', 'users': 100},
                {'date': '2023-02-01', 'users': 150},
                {'date': '2023-03-01', 'users': 220},
                {'date': '2023-04-01', 'users': 300},
                {'date': '2023-05-01', 'users': 380},
            ],
            'popularBreeds': [
                {'name': 'Labrador', 'views': 1200},
                {'name': 'German Shepherd', 'views': 950},
                {'name': 'Golden Retriever', 'views': 800},
                {'name': 'Poodle', 'views': 700},
                {'name': 'Bulldog', 'views': 650},
            ],
            'engagement': [
                {'date': '2023-05-01', 'pageViews': 5000, 'interactions': 1200},
                {'date': '2023-05-08', 'pageViews': 5200, 'interactions': 1250},
                {'date': '2023-05-15', 'pageViews': 5500, 'interactions': 1300},
                {'date': '2023-05-22', 'pageViews': 5300, 'interactions': 1280},
            ],
            'deviceStats': [
                {'name': 'Desktop', 'value': 60},
                {'name': 'Mobile', 'value': 35},
                {'name': 'Tablet', 'value': 5},
            ]
        }
        return analytics_data
    except Exception as e:
        log.error(f"Error fetching admin analytics: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil data analitik.'}