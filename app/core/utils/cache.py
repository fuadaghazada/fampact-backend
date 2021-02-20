import redis

# Redis
__cache = redis.Redis(host="redis", decode_responses=True)
DEFAULT_PRE_KEY = 'fampact'


def get_key(key, pre_key=DEFAULT_PRE_KEY):
    """Getting the value with the key fom cache"""
    return __cache.get(f'{pre_key}_{key}')


def set_key(key, value, pre_key=DEFAULT_PRE_KEY, **kwargs):
    """Setting a key to cache"""
    __cache.set(name=f'{pre_key}_{key}', value=value, **kwargs)


def remove_key(key, pre_key=DEFAULT_PRE_KEY):
    """Removing the key from the cache"""
    __cache.delete(f'{pre_key}_{key}')


def add_to_set(key, value, pre_key=DEFAULT_PRE_KEY):
    """Adding value to the set"""
    __cache.sadd(f'{pre_key}_{key}', value)


def add_to_list(key, value, pre_key=DEFAULT_PRE_KEY):
    """Adding value to the list"""
    __cache.rpush(f'{pre_key}_{key}', value)


def get_list(key, pre_key=DEFAULT_PRE_KEY):
    """Getting the list"""
    return __cache.lrange(f'{pre_key}_{key}', 0, -1)


def is_in_set(key, value, pre_key=DEFAULT_PRE_KEY):
    """Checking if the value in set"""
    return __cache.sismember(f'{pre_key}_{key}', value)


def find_keys(pattern):
    """Finding list of keys with the given pattern"""
    return __cache.keys(pattern)


def h_set(pre_name, name, key, value):
    """Setting in a hash map"""
    return __cache.hset(f'{pre_name}_{name}', key, value)


def h_get(pre_name, name, key):
    """Getting the hash map key value"""
    return __cache.hget(f'{pre_name}_{name}', key)


def h_get_all(pre_name, name):
    """Getting the hash map"""
    return __cache.hgetall(f'{pre_name}_{name}')


def incr(key, pre_key=DEFAULT_PRE_KEY, amount=1):
    """Incrementing the key value"""
    return __cache.incr(f'{pre_key}_{key}', amount)
