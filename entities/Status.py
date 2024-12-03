from enum import Enum


class Status(Enum):
    AT_HUB, EN_ROUTE, DELIVERED, DELAYED_IN_FLIGHT = range(4)
