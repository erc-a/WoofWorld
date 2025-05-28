import os
import sys
from pyramid.paster import bootstrap, setup_logging
from datetime import datetime
from ..models import Video

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)

    with bootstrap(config_uri) as env:
        try:
            request = env['request']
            
            # Sample videos data with proper embed URLs
            videos = [
                {
                    'title': 'Anjing Galau',
                    'description': '@certifiedfreedomlover',
                    'video_url': 'https://www.tiktok.com/@certifiedfreedomlover?refer=embed">@certifiedfreedomlover',
                    'is_public': True
                },
                {
                    'title': 'Cute Puppy Training',
                    'description': 'Watch this adorable puppy learn new tricks',
                    'video_url': 'https://www.tiktok.com/embed/v2/7485970811037240123',
                    'is_public': True
                },
                {
                    'title': 'Dog Tricks Compilation',
                    'description': 'Amazing tricks performed by talented dogs',
                    'video_url': 'https://www.tiktok.com/embed/v2/7483970811037240789',
                    'is_public': True
                }
            ]

            # Clear existing videos first
            request.dbsession.query(Video).delete()

            # Add videos to database
            for video_data in videos:
                video = Video(
                    title=video_data['title'],
                    description=video_data['description'],
                    video_url=video_data['video_url'],
                    is_public=video_data['is_public']
                )
                request.dbsession.add(video)

            print("Sample videos added successfully!")

        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    main()
