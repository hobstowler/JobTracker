import abc


class BaseController(abc.ABC):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseController, cls).__new__(cls, *args, **kwargs)

        return cls.instance


# b = BaseController()
# c = BaseController()
# print(b is c)
