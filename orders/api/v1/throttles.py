from rest_framework.throttling import UserRateThrottle


class OrderEndpointsCustomThrottle(UserRateThrottle):
    rate = '5/minutes'
    
    
class OrderCreationThrottle(UserRateThrottle):
    rate = '5/hour'  # Only 5 orders per hour for each user.