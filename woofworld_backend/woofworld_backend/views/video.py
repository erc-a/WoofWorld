from pyramid.view import view_config
from ..models import Video 
from ..models.video import Video
import logging
import traceback
from pyramid.response import Response
import json

log = logging.getLogger(__name__)

@view_config(route_name='list_public_videos', renderer='json', permission='view_public')
def list_public_videos_view(request):
    log.info("====== API /api/videos DIPANGGIL (list_public_videos_view) ======")
    try:
        log.info("Attempting to query public videos...")
        videos_query = request.dbsession.query(Video).filter(Video.is_public == True).order_by(Video.created_at.desc())
        
        # Log the SQL query being executed
        log.info(f"SQL Query: {str(videos_query)}")
        
        videos = videos_query.all()
        log.info(f"Found {len(videos)} public videos")

        videos_data = []
        for video in videos:
            try:
                video_dict = video.to_dict()
                videos_data.append(video_dict)
                log.info(f"Processed video: {video_dict['title']}")
            except Exception as e:
                log.error(f"Error converting video to dict: {str(e)}")
                log.error(traceback.format_exc())

        response_data = {
            'status': 'success',
            'data': {
                'videos': videos_data
            }
        }
        log.info(f"Returning response with {len(videos_data)} videos")
        return response_data

    except Exception as e:
        log.error(f"Error listing public videos: {str(e)}")
        log.error(traceback.format_exc())
        request.response.status_code = 500
        return {'message': 'Gagal mengambil daftar video.', 'error': str(e)}

