from get-data import get_redis_data
def test_init():
    assert get_redis_data.RedisHost == "redis-13849.c9.us-east-1-4.ec2.cloud.redislabs.com"
