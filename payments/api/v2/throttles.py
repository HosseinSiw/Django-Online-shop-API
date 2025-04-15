from rest_framework.throttling import UserRateThrottle


class PaymentRequestThrottle(UserRateThrottle):
    rate = '5/min'