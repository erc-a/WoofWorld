from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest
from woofworld_backend.models import Fact # Sesuaikan path dengan struktur proyek
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list_facts', request_method='GET', renderer='json')
def list_facts_view(request):
    log.info("API /facts GET (list) dipanggil")
    try:
        facts_query = request.dbsession.query(Fact).order_by(Fact.id.desc())
        facts = facts_query.all()
        log.info(f"Ditemukan {len(facts)} fakta publik.")
        return {
            'status': 'success',
            'data': {'facts': [fact.to_dict() for fact in facts]}
        }
    except Exception as e:
        log.error(f"Error saat mengambil daftar fakta: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar fakta.'}