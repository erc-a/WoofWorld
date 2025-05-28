from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest, HTTPCreated
from woofworld_backend.models import Fact  # Sesuaikan path dengan struktur proyek
import logging

log = logging.getLogger(__name__)

@view_config(route_name='admin_list_facts', request_method='GET', renderer='json', permission='manage_facts')
def admin_list_facts_view(request):
    try:
        # TODO: Implementasi pagination jika daftar fakta sangat banyak
        facts = request.dbsession.query(Fact).order_by(Fact.id.desc()).all()
        return {'facts': [fact.to_dict() for fact in facts]}
    except Exception as e:
        log.error(f"Error listing admin facts: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar fakta.'}

@view_config(route_name='admin_add_fact', request_method='POST', renderer='json', permission='manage_facts')
def admin_add_fact_view(request):
    try:
        # Get and validate JSON data
        data = request.json_body
        content = data.get('content')
        
        if not content or not content.strip():
            raise HTTPBadRequest(json_body={
                'status': 'error', 
                'message': 'Field "content" dibutuhkan dan tidak boleh kosong.'
            })

        content = content.strip()

        # Create new fact - simple approach like the GET endpoint
        new_fact = Fact(content=content)
        request.dbsession.add(new_fact)
        
        # Let pyramid_tm handle the transaction commit automatically
        # Don't flush manually - just return success
        request.response.status = 201
        return {
            'status': 'success',
            'data': {
                'content': content,
                'message': 'Fakta berhasil ditambahkan.'
            }
        }

    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error adding fact: {e}", exc_info=True)
        request.response.status_code = 500
        return {
            'status': 'error',
            'message': 'Gagal menambahkan fakta. Silakan coba lagi.'
        }

@view_config(route_name='admin_get_fact', request_method='GET', renderer='json', permission='manage_facts')
def admin_get_fact_view(request):
    try:
        fact_id = int(request.matchdict['id'])
        fact = request.dbsession.query(Fact).get(fact_id)
        if not fact:
            raise HTTPNotFound(json_body={'message': 'Fakta tidak ditemukan.'})
        return fact.to_dict()
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID fakta tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error getting admin fact {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil detail fakta.'}

@view_config(route_name='admin_update_fact', request_method='PUT', renderer='json', permission='manage_facts')
def admin_update_fact_view(request):
    try:
        fact_id = int(request.matchdict['id'])
        fact_to_update = request.dbsession.query(Fact).get(fact_id)
        if not fact_to_update:
            raise HTTPNotFound(json_body={'message': 'Fakta tidak ditemukan.'})

        data = request.json_body
        content = data.get('content')
        if content is None: # Boleh update jadi string kosong, tapi field harus ada
             raise HTTPBadRequest(json_body={'message': 'Field "content" dibutuhkan untuk update.'})

        fact_to_update.content = content
        request.dbsession.flush()
        return HTTPOk(json_body=fact_to_update.to_dict())
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID fakta tidak valid.'})
    except (HTTPNotFound, HTTPBadRequest) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error updating fact {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal memperbarui fakta.'}

@view_config(route_name='admin_delete_fact', request_method='DELETE', renderer='json', permission='manage_facts')
def admin_delete_fact_view(request):
    try:
        fact_id = int(request.matchdict['id'])
        fact_to_delete = request.dbsession.query(Fact).get(fact_id)
        if not fact_to_delete:
            raise HTTPNotFound(json_body={'message': 'Fakta tidak ditemukan.'})

        request.dbsession.delete(fact_to_delete)
        return HTTPOk(json_body={'message': f'Fakta ID {fact_id} berhasil dihapus.'})
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID fakta tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error deleting fact {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menghapus fakta.'}