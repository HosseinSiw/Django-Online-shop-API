from rest_framework.throttling import AnonRateThrottle


class UserPasswordResetRequestThrottle(AnonRateThrottle):
    rate = '1/hour'
    
    
class UserRegisterationThrottle(AnonRateThrottle):
    rate = '5/min'