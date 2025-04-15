from rest_framework.throttling import AnonRateThrottle


class ProductEndpointsThrottle(AnonRateThrottle):
    rate = '30/min'
