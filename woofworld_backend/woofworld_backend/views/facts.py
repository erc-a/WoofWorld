# from pyramid.view import view_config
# from pyramid.response import Response
# from sqlalchemy import desc
# from woofworld_backend.models.fact import Fact

# @view_config(route_name='list_facts', renderer='json', permission='view_public')
# def get_facts(request):
#     try:
#         # Get all facts from database
#         facts = request.dbsession.query(Fact).order_by(desc(Fact.created_at)).all()
        
#         response = Response(json={
#             'status': 'success',
#             'data': {
#                 'facts': [fact.to_dict() for fact in facts]
#             }
#         })
        
#         # Add CORS headers
#         response.headers.update({
#             'Access-Control-Allow-Origin': 'http://localhost:5173',
#             'Access-Control-Allow-Methods': 'GET,OPTIONS',
#             'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
#             'Access-Control-Allow-Credentials': 'true'
#         })
        
#         return response
        
#     except Exception as e:
#         response = Response(
#             json={'status': 'error', 'message': str(e)},
#             status=500
#         )
#         response.headers.update({
#             'Access-Control-Allow-Origin': 'http://localhost:5173',
#             'Access-Control-Allow-Methods': 'GET,OPTIONS',
#             'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
#             'Access-Control-Allow-Credentials': 'true'
#         })
#         return response


# woofworld_backend/woofworld_backend/views/facts.py
# woofworld_backend/woofworld_backend/views/facts.py
from pyramid.view import view_config
from sqlalchemy import desc
from ..models.fact import Fact # Pastikan Fact.to_dict() ada di model
import logging
log = logging.getLogger(__name__)

@view_config(route_name='list_facts', renderer='json', permission='view_public')
def get_facts(request):
    log.info("====== FUNGSI get_facts DIPANGGIL (VERSI BERSIH) ======")
    try:
        facts_query = request.dbsession.query(Fact).order_by(desc(Fact.created_at))
        facts = facts_query.all()

        # Menggunakan to_dict() sesuai model Fact yang kamu punya
        facts_data = [fact.to_dict() for fact in facts] 

        return {
            'status': 'success',
            'data': {
                'facts': facts_data
            }
        }
    except Exception as e:
        log.error(f"Error dalam get_facts: {e}", exc_info=True) # Log error detail
        # Saat development, mungkin lebih baik raise error agar traceback jelas
        # atau return error response yang lebih informatif jika diinginkan.
        # Untuk sekarang, kita return status 500 jika ada error.
        request.response.status_code = 500 
        return {'status': 'error', 'message': 'Terjadi kesalahan internal saat mengambil fakta.'}