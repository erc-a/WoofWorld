from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest
from woofworld_backend.models import Video
import logging

log = logging.getLogger(__name__)

@view_config(route_name='list_public_videos', request_method='GET', renderer='json')
def list_videos_view(request):
    log.info("API /videos GET (list) dipanggil")
    try:
        videos_query = request.dbsession.query(Video).filter(Video.is_public == True).order_by(Video.created_at.desc())
        videos = videos_query.all()
        log.info(f"Ditemukan {len(videos)} video publik.")
        # Mengubah format respons agar sesuai dengan ekspektasi frontend
        return {
            'status': 'success',
            'data': {'videos': [video.to_dict() for video in videos]}
        }
    except Exception as e:
        log.error(f"Error saat mengambil daftar video: {e}", exc_info=True)
        request.response.status_code = 500
        # Respons error tetap sama, frontend akan menangani jika status bukan 2xx
        return {'status': 'error', 'message': 'Gagal mengambil daftar video.'}