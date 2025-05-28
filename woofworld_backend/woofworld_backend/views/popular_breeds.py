from pyramid.view import view_config
from pyramid.httpexceptions import HTTPInternalServerError
import logging
from .breed import make_dog_api_request # Pastikan impor ini benar

log = logging.getLogger(__name__)

POPULAR_BREED_IDS = [121, 113, 226, 196] 
POPULAR_BREED_STATIC_IMAGES = {
    121: "/dog-1.jpg", 
    113: "/dog-2.jpg", 
    226: "/dog-3.jpg", 
    196: "/dog-4.jpg"
}

@view_config(route_name='list_popular_breeds', renderer='json', permission='view_public')
def list_popular_breeds_view(request):
    log.info(f"====== API {request.path} DIPANGGIL (list_popular_breeds_view) ======") # Tambahkan ini
    popular_breeds_details = []
    try:
        all_breeds = make_dog_api_request('breeds', params={'limit': 300, 'page': 0})

        for breed_id in POPULAR_BREED_IDS:
            breed_info = next((b for b in all_breeds if b.get('id') == breed_id), None)
            if breed_info:
                image_url_from_api = breed_info.get('image', {}).get('url')
                final_image_url = image_url_from_api if image_url_from_api else POPULAR_BREED_STATIC_IMAGES.get(breed_id)
                popular_breeds_details.append({
                    'id': breed_info.get('id'),
                    'name': breed_info.get('name'),
                    'description': breed_info.get('temperament', 'No description available.'),
                    'image': {'url': final_image_url },
                    'traits': breed_info.get('temperament', '').split(', ')[:3]
                })
            else:
                log.warning(f"Popular breed with ID {breed_id} not found in TheDogAPI results.")
        return {'popular_breeds': popular_breeds_details}
    except Exception as e:
        log.error(f"Error fetching popular breeds: {e}", exc_info=True)
        raise HTTPInternalServerError(json_body={'message': 'Gagal mengambil ras anjing populer.'})