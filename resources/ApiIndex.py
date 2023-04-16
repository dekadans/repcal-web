from . import Resource


class ApiIndex(Resource):
    def type(self) -> str: return 'apiindex'

    def to_dict(self) -> dict:
        return {
            'name': 'repcal.info',
            'description': 'An API for accessing datetime data in the styles used by the French First Republic.'
        }