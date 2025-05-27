from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest, HTTPCreated
from woofworld_backend.models import Video  # Sesuaikan path
import logging

log = logging.getLogger(__name__)

@view_config(route_name='admin_list_videos', request_method='GET', renderer='json', permission='manage_videos')
def admin_list_videos_view(request):
    try:
        # TODO: Implementasi pagination jika daftar video sangat banyak
        videos = request.dbsession.query(Video).order_by(Video.id.desc()).all()
        return {'videos': [video.to_dict() for video in videos]}
    except Exception as e:
        log.error(f"Error listing admin videos: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar video.'}

@view_config(route_name='admin_add_video', request_method='POST', renderer='json', permission='manage_videos')
def admin_add_video_view(request):
    try:
        data = request.json_body
        title = data.get('title')
        video_url = data.get('videoUrl') # Sesuaikan dengan nama field dari frontend
        description = data.get('description', '') # Deskripsi opsional

        if not title or not video_url:
            raise HTTPBadRequest(json_body={'message': 'Field "title" dan "videoUrl" dibutuhkan.'})
        
        # Validasi URL sederhana (bisa lebih kompleks)
        if not (video_url.startswith('http://') or video_url.startswith('https://')):
            raise HTTPBadRequest(json_body={'message': 'Format videoUrl tidak valid.'})


        new_video = Video(title=title, video_url=video_url, description=description)
        request.dbsession.add(new_video)
        request.dbsession.flush()
        return HTTPCreated(json_body=new_video.to_dict())
    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error adding video: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menambahkan video.'}

@view_config(route_name='admin_get_video', request_method='GET', renderer='json', permission='manage_videos')
def admin_get_video_view(request):
    try:
        video_id = int(request.matchdict['id'])
        video = request.dbsession.query(Video).get(video_id)
        if not video:
            raise HTTPNotFound(json_body={'message': 'Video tidak ditemukan.'})
        return video.to_dict()
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID video tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error getting admin video {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal mengambil detail video.'}

@view_config(route_name='admin_update_video', request_method='PUT', renderer='json', permission='manage_videos')
def admin_update_video_view(request):
    try:
        video_id = int(request.matchdict['id'])
        video_to_update = request.dbsession.query(Video).get(video_id)
        if not video_to_update:
            raise HTTPNotFound(json_body={'message': 'Video tidak ditemukan.'})

        data = request.json_body
        # Update field yang ada di data dan diizinkan untuk diupdate
        if 'title' in data:
            video_to_update.title = data['title']
        if 'videoUrl' in data: # Sesuaikan dengan nama field dari frontend
            video_url = data['videoUrl']
            if not (video_url.startswith('http://') or video_url.startswith('https://')):
                 raise HTTPBadRequest(json_body={'message': 'Format videoUrl tidak valid.'})
            video_to_update.video_url = video_url
        if 'description' in data:
            video_to_update.description = data['description']
        
        request.dbsession.flush()
        return HTTPOk(json_body=video_to_update.to_dict())
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID video tidak valid.'})
    except (HTTPNotFound, HTTPBadRequest) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error updating video {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal memperbarui video.'}

@view_config(route_name='admin_delete_video', request_method='DELETE', renderer='json', permission='manage_videos')
def admin_delete_video_view(request):
    try:
        video_id = int(request.matchdict['id'])
        video_to_delete = request.dbsession.query(Video).get(video_id)
        if not video_to_delete:
            raise HTTPNotFound(json_body={'message': 'Video tidak ditemukan.'})

        request.dbsession.delete(video_to_delete)
        return HTTPOk(json_body={'message': f'Video ID {video_id} berhasil dihapus.'})
    except ValueError:
        raise HTTPBadRequest(json_body={'message': 'ID video tidak valid.'})
    except HTTPNotFound as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Error deleting video {request.matchdict.get('id')}: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Gagal menghapus video.'}