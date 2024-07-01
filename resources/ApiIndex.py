from . import Resource


class ApiIndex(Resource):
    def type(self) -> str: return 'apiindex'

    def to_dict(self) -> dict:
        return {}
