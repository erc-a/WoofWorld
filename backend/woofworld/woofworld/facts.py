from pyramid.view import view_config
from pyramid.response import Response
from ..models.fact import Fact
from sqlalchemy import desc

@view_config(route_name='facts', renderer='json')
def get_facts(request):
    try:
        page = int(request.params.get('page', 1))
        limit = int(request.params.get('limit', 5))
        offset = (page - 1) * limit

        query = request.dbsession.query(Fact).order_by(desc(Fact.created_at))
        total = query.count()
        facts = query.offset(offset).limit(limit).all()

        return {
            'status': 'success',
            'data': {
                'facts': [fact.to_json() for fact in facts],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total,
                    'hasMore': offset + limit < total
                }
            }
        }
    except Exception as e:
        return Response(
            json={'status': 'error', 'message': str(e)},
            status=500
        )