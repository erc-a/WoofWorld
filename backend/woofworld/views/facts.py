from pyramid.view import view_config
from pyramid.response import Response
from ..models import Fact

@view_config(route_name='facts_list', renderer='json')
def list_facts(request):
    try:
        page = int(request.params.get('page', 1))
        limit = int(request.params.get('limit', 5))
        offset = (page - 1) * limit

        query = request.dbsession.query(Fact)
        total = query.count()
        facts = query.offset(offset).limit(limit).all()
        
        return {
            'status': 'success',
            'data': {
                'facts': [fact.to_json() for fact in facts],
                'pagination': {
                    'total': total,
                    'page': page,
                    'limit': limit,
                    'hasMore': total > (offset + limit)
                }
            }
        }
    except Exception as e:
        request.response.status = 500
        return {
            'status': 'error',
            'message': str(e)
        }