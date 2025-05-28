#!/usr/bin/env python3

from pyramid.paster import get_app
from wsgiref.simple_server import make_server
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

try:
    log.info("Loading application...")
    app = get_app('development.ini')
    log.info("Application loaded successfully")
    
    log.info("Starting server on port 6544...")
    server = make_server('0.0.0.0', 6544, app)
    log.info("Server started. Press Ctrl+C to stop")
    
    server.serve_forever()
    
except Exception as e:
    log.error(f"Failed to start server: {e}", exc_info=True)
