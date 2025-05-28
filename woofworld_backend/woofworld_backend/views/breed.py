from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError, HTTPBadRequest
import requests # Library untuk membuat HTTP request
import os
import logging

log = logging.getLogger(__name__)

THE_DOG_API_KEY = os.environ.get('THE_DOG_API_KEY', 'live_LjTiXLNveHjkoh664tkodk7f4L3A4pIPGVi8Bx0jUXvlpXI5bZiyzotUSHsOapxo')
THE_DOG_API_BASE_URL = 'https://api.thedogapi.com/v1'

def make_dog_api_request(endpoint, params=None):
    headers = {'x-api-key': THE_DOG_API_KEY}
    try:
        log.info(f"Requesting TheDogAPI: {THE_DOG_API_BASE_URL}/{endpoint} with params: {params}")
        response = requests.get(f"{THE_DOG_API_BASE_URL}/{endpoint}", headers=headers, params=params, timeout=15) # Timeout diperpanjang
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        log.error(f"HTTP error occurred: {http_err} - Status: {response.status_code} - Response: {response.text}")
        if response.status_code == 404:
            # Untuk search, 404 bisa berarti tidak ada hasil, bukan error server
            if "search" in endpoint:
                return [] # Kembalikan array kosong jika search tidak menemukan apa-apa
            raise HTTPNotFound(json_body={'message': f'Data tidak ditemukan dari TheDogAPI: {endpoint}'})
        elif response.status_code == 400: # Bad request dari TheDogAPI
             raise HTTPBadRequest(json_body={'message': f'Bad request ke TheDogAPI ({response.status_code}): {response.text}'})
        raise HTTPInternalServerError(json_body={'message': f'Error dari TheDogAPI ({response.status_code}): {response.text}'})
    except requests.exceptions.RequestException as req_err:
        log.error(f"Request error occurred: {req_err}")
        raise HTTPInternalServerError(json_body={'message': 'Gagal menghubungi TheDogAPI.'})


@view_config(route_name='list_breeds', request_method='GET', renderer='json', permission='view_public')
def list_breeds_view(request):
    try:
        page_str = request.params.get('page', '0') 
        limit_str = request.params.get('limit', '12')
        search_query = request.params.get('q', None)

        try:
            page = int(page_str)
            limit = int(limit_str)
        except ValueError:
            raise HTTPBadRequest(json_body={'message': 'Parameter page dan limit harus berupa angka.'})

        api_params = {'page': page, 'limit': limit}
        
        if search_query:
            endpoint = 'breeds/search'
            api_params['q'] = search_query
            # TheDogAPI untuk /breeds/search juga mendukung `limit` dan `page`
            # jadi tidak perlu menghapusnya.
        else:
            endpoint = 'breeds'
            
        breeds_data = make_dog_api_request(endpoint, params=api_params)
        
        # Penting: TheDogAPI /breeds/search mengembalikan array langsung, 
        # sedangkan /breeds mengembalikan array langsung.
        # Frontend mengharapkan object dengan key 'breeds'.
        # Jadi, kita bungkus hasilnya jika belum berupa object.
        # Namun, dari kode frontend: `const newBreeds = data.breeds || data;`
        # Ini berarti frontend bisa menangani jika `data` adalah array langsung atau `data.breeds` adalah array.
        # Untuk konsistensi, backend akan selalu mengembalikan `{'breeds': hasil_dari_api}`
        
        return {'breeds': breeds_data} 
    except (HTTPNotFound, HTTPInternalServerError, HTTPBadRequest) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Unexpected error in list_breeds_view: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan tak terduga.'}

@view_config(route_name='get_breed', request_method='GET', renderer='json', permission='view_public')
def get_breed_view(request):
    try:
        breed_api_id = request.matchdict['id']
        # TheDogAPI menggunakan endpoint /images/search?breed_ids={id} untuk mendapatkan detail termasuk gambar
        # atau /breeds/{id} untuk info breed saja. Frontend kamu mengambil dari /breeds.
        # Jika frontend mengambil semua breed lalu filter by id, maka backend tidak perlu endpoint ini
        # Namun, jika frontend `DogBreedDetail.jsx` memanggil `/api/breeds/{id}`, kita bisa proxy ke
        # `https://api.thedogapi.com/v1/breeds` dan filter di backend,
        # atau langsung ke `https://api.thedogapi.com/v1/breeds/{breed_api_id}` jika API-nya mendukung.
        # Dari `DogBreedDetail.jsx` sepertinya frontend mengambil semua breeds dan filter,
        # tapi ada juga fetch ke `/breeds` dengan `parseInt(id)`. Ini agak membingungkan.
        # Asumsi frontend akan call `/api/breeds/{id}` dan backend meneruskannya.

        # Cari breed berdasarkan ID dari list semua breed (jika ID bukan ID asli API tapi index/urutan)
        # Ini kurang efisien. Lebih baik jika frontend menggunakan ID asli dari TheDogAPI.
        # Mari kita asumsikan `id` di route adalah ID asli dari TheDogAPI.
        # Endpoint TheDogAPI: /breeds/{breed_id} (Ini tidak ada di dokumentasi mereka, biasanya search by ID)
        # Alternatif: /images/search?breed_ids={breed_id}&include_breed=1
        
        # Frontend (DogBreedDetail.jsx) melakukan fetch ke 'https://api.thedogapi.com/v1/breeds' lalu find.
        # Jika frontend memanggil backend `/api/breeds/{id}`, backend bisa melakukan hal serupa.
        all_breeds_data = make_dog_api_request('breeds')
        
        selected_breed = None
        try:
            # Coba konversi id ke integer karena ID dari TheDogAPI adalah integer
            target_id = int(breed_api_id)
            for breed in all_breeds_data:
                if breed.get('id') == target_id:
                    selected_breed = breed
                    break
        except ValueError:
            # Jika ID bukan integer (misal nama breed), maka cari berdasarkan nama
             for breed in all_breeds_data:
                if breed.get('name', '').lower() == breed_api_id.lower():
                    selected_breed = breed
                    break
        
        if not selected_breed:
            raise HTTPNotFound(json_body={'message': f'Ras anjing dengan ID/nama "{breed_api_id}" tidak ditemukan.'})
        
        return selected_breed # Langsung return data dari API
        
    except (HTTPNotFound, HTTPInternalServerError) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Unexpected error in get_breed_view for id {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan tak terduga.'}

# @view_config(route_name='popular_breeds', request_method='GET', renderer='json', permission='view_public')
# def popular_breeds_view(request):
#     try:
#         # Get all breeds and sort by popularity/weight/height
#         breeds_data = make_dog_api_request('breeds')
        
#         # Sort by weight as a simple popularity metric
#         # You could implement a more sophisticated popularity algorithm
#         sorted_breeds = sorted(
#             breeds_data,
#             key=lambda x: int(x.get('weight', {}).get('metric', '0').split('-')[0] or '0'),
#             reverse=True
#         )
        
#         # Return top 10 breeds
#         return {'breeds': sorted_breeds[:10]}
        
#     except Exception as e:
#         log.error(f"Error in popular_breeds_view: {e}", exc_info=True)
#         request.response.status = 500
#         return {'message': 'Terjadi kesalahan saat mengambil ras populer.'}

# @view_config(route_name='videos', request_method='GET', renderer='json', permission='view_public')
# def videos_view(request):
#     try:
#         # Since TheDogAPI doesn't have videos endpoint,
#         # returning mock data or you could integrate with YouTube API
#         videos = [
#             {
#                 'id': 1,
#                 'title': 'Pelatihan Dasar Anjing',
#                 'url': 'https://www.youtube.com/watch?v=example1',
#                 'thumbnail': 'https://example.com/thumbnail1.jpg'
#             },
#             {
#                 'id': 2, 
#                 'title': 'Tips Merawat Anjing',
#                 'url': 'https://www.youtube.com/watch?v=example2',
#                 'thumbnail': 'https://example.com/thumbnail2.jpg'
#             }
#         ]
#         return {'videos': videos}
        
#     except Exception as e:
#         log.error(f"Error in videos_view: {e}", exc_info=True)
#         request.response.status = 500
#         return {'message': 'Terjadi kesalahan saat mengambil video.'}