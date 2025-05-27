from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest
from woofworld_backend.models import User  # Sesuaikan path jika berbeda
from woofworld_backend.security import get_user  # Sesuaikan path
import logging

log = logging.getLogger(__name__)

@view_config(route_name='admin_list_users', request_method='GET', renderer='json', permission='manage_users')
def admin_list_users_view(request):
    try:
        users = request.dbsession.query(User).order_by(User.id).all()
        # Jangan sertakan password hash. Email hanya untuk admin.
        return {'users': [user.to_dict(include_email=True) for user in users]}
    except Exception as e:
        log.error(f"Error listing admin users: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar pengguna.'}

@view_config(route_name='admin_delete_user', request_method='DELETE', renderer='json', permission='manage_users')
def admin_delete_user_view(request):
    try:
        user_id_to_delete = int(request.matchdict['id'])
        
        # Jangan biarkan admin menghapus dirinya sendiri
        current_admin_user = get_user(request)
        if current_admin_user and current_admin_user.id == user_id_to_delete:
            raise HTTPBadRequest(json_body={'message': 'Admin tidak dapat menghapus akun sendiri.'})

        user_to_delete = request.dbsession.query(User).get(user_id_to_delete)
        if not user_to_delete:
            raise HTTPNotFound(json_body={'message': 'Pengguna tidak ditemukan.'})

        request.dbsession.delete(user_to_delete)
        return HTTPOk(json_body={'message': f'Pengguna ID {user_id_to_delete} berhasil dihapus.'})
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID pengguna tidak valid.'})
    except (HTTPNotFound, HTTPBadRequest) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error deleting user {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menghapus pengguna.'}

# Kamu bisa tambahkan view untuk update role user jika diperlukan
# @view_config(route_name='admin_update_user_role', request_method='PUT', renderer='json', permission='manage_users')
# def admin_update_user_role_view(request):
#     # ... implementasi ...