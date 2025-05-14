from woofworld.models import get_tm_session
from woofworld.models.fact import Fact
from pyramid.paster import bootstrap, setup_logging
import sys
import transaction

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
    
    env = bootstrap(config_uri)
    with env['request'].tm:
        dbsession = env['request'].dbsession
        
        facts = [
            Fact(content="Dogs have a sense of time and can differentiate between 5 minutes and 2 hours."),
            Fact(content="A dog's nose print is unique, much like a person's fingerprint."),
            Fact(content="Dogs can understand over 150 words and can count up to five.")
        ]
        
        dbsession.add_all(facts)

if __name__ == '__main__':
    main()