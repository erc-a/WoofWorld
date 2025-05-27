from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk
from ..models import Fact
from sqlalchemy import desc
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list_facts', request_method='GET', renderer='json', permission='view_public')
def list_facts_view(request):
    try:
        page = int(request.params.get('page', 1))
        limit = int(request.params.get('limit', 5)) # Sesuaikan dengan frontend
        offset = (page - 1) * limit

        query = request.dbsession.query(Fact).order_by(desc(Fact.created_at))
        total = query.count()
        facts = query.offset(offset).limit(limit).all()

        return {
            'status': 'success', # Frontend mengharapkan ini
            'data': {
                'facts': [fact.to_dict() for fact in facts],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total,
                    'hasMore': (offset + limit) < total
                }
            }
        }
    except ValueError:
        request.response.status_code = 400
        return {'status': 'error', 'message': 'Parameter page atau limit tidak valid.'}
    except Exception as e:
        log.error(f"Error listing facts: {e}", exc_info=True)
        request.response.status_code = 500
        return {'status': 'error', 'message': 'Gagal mengambil data fakta.'}