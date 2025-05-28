#!/usr/bin/env python3

# Test script to diagnose the Fact model and database issues
from pyramid.paster import get_app
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

try:
    # Load the application to initialize database connection
    log.info("Loading application...")
    app = get_app('development.ini')
    log.info("Application loaded")
    
    # Get registry and session factory
    registry = app.registry
    session_factory = registry['dbsession_factory']
    
    log.info("Creating database session...")
    from zope.sqlalchemy import mark_changed
    from pyramid.request import Request
    from woofworld_backend.models import Fact
    
    # Create a dummy request to test session
    request = Request.blank('/')
    request.registry = registry
    
    # Create session
    from woofworld_backend.models import get_tm_session
    import transaction
    
    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        request.dbsession = session
        
        log.info("Testing Fact model instantiation...")
        test_fact = Fact(content="Test fact for debugging")
        log.info(f"Fact created: {test_fact}")
        log.info(f"Fact content: {test_fact.content}")
        
        log.info("Adding fact to session...")
        session.add(test_fact)
        
        log.info("Flushing session...")
        session.flush()
        
        log.info(f"Fact ID after flush: {test_fact.id}")
        
        log.info("Converting to dict...")
        fact_dict = test_fact.to_dict()
        log.info(f"Fact dict: {fact_dict}")
        
        log.info("SUCCESS: All operations completed successfully!")
        
        # Don't commit, just test
        transaction.abort()
        
except Exception as e:
    log.error(f"Error during test: {e}", exc_info=True)
    sys.exit(1)
