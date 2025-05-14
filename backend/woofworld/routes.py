def includeme(config):
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login')
    config.add_route('facts_list', '/api/facts')