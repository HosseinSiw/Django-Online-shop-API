from rest_framework.throttling import AnonRateThrottle


class UserPasswordResetRequestThrottle(AnonRateThrottle):
    rate = '1/hour'