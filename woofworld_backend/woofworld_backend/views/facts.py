from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import desc
from ..models.fact import Fact

@view_config(route_name='list_facts', renderer='json', permission='view')
def get_facts(request):
    try:
        # Get all facts from database
        facts = request.dbsession.query(Fact).order_by(desc(Fact.created_at)).all()
        
        response = Response(json={
            'status': 'success',
            'data': {
                'facts': [fact.to_json() for fact in facts]
            }
        })
        
        # Add CORS headers
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        })
        
        return response
        
    except Exception as e:
        response = Response(
            json={'status': 'error', 'message': str(e)},
            status=500
        )
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        })
        return response
