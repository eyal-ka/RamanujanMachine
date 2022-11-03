configuration = {
    'pool_size': 10,
    'jobs_to_run': {
        'poly_pslq': {
            'args': { 'degree': (2, 1), 'bulk': 1000, 'subdivide': {
                'PcfCanonical': { 'count': 1, 'balanced_only': True },
                'Named': { 'count': 2 }
                }
            },
            'run_async': True,
            'cooldown': 30,
            'no_work_timeout': 60
        }
    }
}

# If you make your own database, 'name' must match the name in 'create_db.sql' in the line 'CREATE DATABASE <name>'
db_configuration = {
    'host': 'database-1.c1keieal025m.us-east-2.rds.amazonaws.com',
    'port': 5432,
    'user': '',
    'passwd': '',
    'name': 'ramanujanv3'
}

def get_connection_string(db_name=None):
    import sys
    conf = db_configuration.copy()
    if len(sys.argv) >= 2:
        user_pass = sys.argv[1]
        username, password = user_pass.split(",")
        conf["user"] = username
        conf["passwd"] = password
    if db_name:
        conf['name'] = db_name
    return 'postgresql://{user}:{passwd}@{host}:{port}/{name}'.format(**conf)
