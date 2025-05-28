# Modul ini tidak lagi digunakan karena breeds data diambil dari TheDogAPI
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest, HTTPCreated
import logging

log = logging.getLogger(__name__)

@view_config(route_name='admin_list_breeds', request_method='GET', renderer='json', permission='manage_breeds')
def admin_list_breeds_view(request):
    try:
        # TODO: Implementasi pagination dan search jika daftar breed sangat banyak
        breeds = request.dbsession.query(DogBreed).order_by(DogBreed.name).all()
        return {'breeds': [breed.to_dict() for breed in breeds]}
    except Exception as e:
        log.error(f"Error listing admin breeds: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar ras anjing.'}

@view_config(route_name='admin_add_breed', request_method='POST', renderer='json', permission='manage_breeds')
def admin_add_breed_view(request):
    try:
        data = request.json_body
        required_fields = ['name'] # Tambahkan field lain jika wajib
        for field in required_fields:
            if field not in data or not data[field]:
                raise HTTPBadRequest(json_body={'message': f'Field "{field}" dibutuhkan.'})

        # Cek apakah breed dengan nama yang sama sudah ada
        existing_breed = request.dbsession.query(DogBreed).filter_by(name=data['name']).first()
        if existing_breed:
            raise HTTPBadRequest(json_body={'message': f'Ras anjing dengan nama "{data["name"]}" sudah ada.'})

        new_breed = DogBreed(
            name=data.get('name'),
            breed_group=data.get('breed_group'),
            temperament=data.get('temperament'),
            origin=data.get('origin'),
            life_span=data.get('life_span'),
            weight_metric=data.get('weight_metric'),
            height_metric=data.get('height_metric'),
            image_url=data.get('image_url')
        )
        request.dbsession.add(new_breed)
        request.dbsession.flush() # Untuk mendapatkan ID
        return HTTPCreated(json_body=new_breed.to_dict())
    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error adding breed: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menambahkan ras anjing.'}


@view_config(route_name='admin_get_breed', request_method='GET', renderer='json', permission='manage_breeds')
def admin_get_breed_view(request):
    try:
        breed_id = int(request.matchdict['id'])
        breed = request.dbsession.query(DogBreed).get(breed_id)
        if not breed:
            raise HTTPNotFound(json_body={'message': 'Ras anjing tidak ditemukan.'})
        return breed.to_dict()
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID ras tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error getting admin breed {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil detail ras anjing.'}


@view_config(route_name='admin_update_breed', request_method='PUT', renderer='json', permission='manage_breeds')
def admin_update_breed_view(request):
    try:
        breed_id = int(request.matchdict['id'])
        breed_to_update = request.dbsession.query(DogBreed).get(breed_id)
        if not breed_to_update:
            raise HTTPNotFound(json_body={'message': 'Ras anjing tidak ditemukan.'})

        data = request.json_body
        # Update field yang ada di data
        for key, value in data.items():
            if hasattr(breed_to_update, key):
                setattr(breed_to_update, key, value)
        
        request.dbsession.flush()
        return HTTPOk(json_body=breed_to_update.to_dict())
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID ras tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error updating breed {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal memperbarui ras anjing.'}

@view_config(route_name='admin_delete_breed', request_method='DELETE', renderer='json', permission='manage_breeds')
def admin_delete_breed_view(request):
    try:
        breed_id = int(request.matchdict['id'])
        breed_to_delete = request.dbsession.query(DogBreed).get(breed_id)
        if not breed_to_delete:
            raise HTTPNotFound(json_body={'message': 'Ras anjing tidak ditemukan.'})

        # Hapus juga dari tabel favorites jika ada relasi (cascade delete seharusnya menangani ini jika diset di model)
        # request.dbsession.query(Favorite).filter_by(breed_id=breed_id).delete()

        request.dbsession.delete(breed_to_delete)
        return HTTPOk(json_body={'message': f'Ras anjing ID {breed_id} berhasil dihapus.'})
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID ras tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body    except Exception as e:
        log.error(f"Error deleting breed {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menghapus ras anjing.'}
"""