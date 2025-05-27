from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest, HTTPForbidden
from woofworld_backend.models import Favorite # User sudah diimport di get_user
from woofworld_backend.security import get_user
# Impor fungsi untuk request ke Dog API jika perlu fetch detail saat add favorite
from .breed import make_dog_api_request, THE_DOG_API_BASE_URL # Asumsi ada di views/breed.py
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list_favorites', request_method='GET', renderer='json', permission='access_favorites')
def list_favorites_view(request):
    user = get_user(request)
    if not user:
        raise HTTPForbidden(json_body={'message': 'Akses ditolak.'})
    
    try:
        # Ambil semua favorit untuk user tersebut
        favorites_query = request.dbsession.query(Favorite).filter_by(user_id=user.id)
        favorites = favorites_query.all()
        
        # Ubah ke format yang diharapkan frontend
        # Frontend `Favorites.jsx` mengharapkan `id`, `name`, `image.url`, `temperament`
        
        # Cek file `Favorites.jsx`
        # `dog.image?.url`, `dog.name`, `dog.temperament`, `dog.id`
        # Model Favorite kita sekarang punya `breed_api_id`, `breed_name`, `breed_image_url`, `breed_temperament`
        
        result = []
        for fav in favorites:
            result.append({
                "id": fav.breed_api_id, # ID breed
                "name": fav.breed_name,
                "image": {"url": fav.breed_image_url} if fav.breed_image_url else None,
                "temperament": fav.breed_temperament
            })
        return result # Langsung list of breed objects
        # atau return {'favorites': result} jika frontend mengharapkan object dengan key 'favorites'

    except Exception as e:
        log.error(f"Error listing favorites for user {user.id}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil data favorit.'}


@view_config(route_name='add_favorite', request_method='POST', renderer='json', permission='access_favorites')
def add_favorite_view(request):
    user = get_user(request)
    if not user:
        raise HTTPForbidden(json_body={'message': 'Akses ditolak.'})

    try:
        # Frontend `DogBreedDetail.jsx` mengirimkan `breed` object saat `addToFavorites(breed)`
        # Asumsi data yang dikirim dari frontend adalah objek breed dari TheDogAPI
        breed_data = request.json_body 
        
        # ID breed dari TheDogAPI bisa integer atau string, kita simpan sebagai string untuk konsistensi
        breed_api_id = str(breed_data.get('id')) 
        breed_name = breed_data.get('name')
        breed_image_url = breed_data.get('image', {}).get('url') if breed_data.get('image') else None
        breed_temperament = breed_data.get('temperament')

        if not breed_api_id or not breed_name:
            raise HTTPBadRequest(json_body={'message': 'Data breed (id, name) dibutuhkan.'})

        existing_favorite = request.dbsession.query(Favorite).filter_by(user_id=user.id, breed_api_id=breed_api_id).first()
        if existing_favorite:
            return HTTPOk(json_body={'message': 'Sudah ada di favorit.', 
                                     'favorite': existing_favorite.to_dict()})

        new_favorite = Favorite(
            user_id=user.id, 
            breed_api_id=breed_api_id,
            breed_name=breed_name,
            breed_image_url=breed_image_url,
            breed_temperament=breed_temperament
        )
        request.dbsession.add(new_favorite)
        request.dbsession.flush() 
        return HTTPCreated(json_body={'message': 'Berhasil ditambahkan ke favorit.', 
                                      'favorite': new_favorite.to_dict()})
    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error adding favorite for user {user.id}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menambahkan favorit.'}


@view_config(route_name='remove_favorite', request_method='DELETE', renderer='json', permission='access_favorites')
def remove_favorite_view(request):
    user = get_user(request)
    if not user:
        raise HTTPForbidden(json_body={'message': 'Akses ditolak.'})

    try:
        # `breed_id` di sini adalah `breed_api_id`
        breed_api_id_to_delete = str(request.matchdict['breed_id']) 
        
        favorite_to_delete = request.dbsession.query(Favorite).filter_by(user_id=user.id, breed_api_id=breed_api_id_to_delete).first()

        if not favorite_to_delete:
            raise HTTPNotFound(json_body={'message': 'Favorit tidak ditemukan.'})

        request.dbsession.delete(favorite_to_delete)
        return HTTPOk(json_body={'message': 'Berhasil dihapus dari favorit.'})
    except (ValueError, TypeError): # Jika konversi str gagal (seharusnya tidak jika route benar)
        raise HTTPBadRequest(json_body={'message': 'breed_id tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error removing favorite for user {user.id}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menghapus favorit.'}