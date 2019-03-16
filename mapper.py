import operator
from functools import reduce


def deep_get(path, obj):
    try:
        return reduce(operator.getitem, path, obj)
    except:
        return None


def apply_projection(projection, obj):
    if isinstance(projection, Mapper):
        return projection.apply(obj)
    elif isinstance(projection, list):
        return deep_get(projection, obj)
    elif isinstance(projection, str):
        return obj[projection]
    raise Exception('Wrong projection type')


class Mapper:
    def __init__(self):
        self.keys = []
        self.props = {}
        self.projections = {}
        self.list_projections = {}

    def has_prop(self, key):
        return key in self.props

    def has_projection(self, key):
        return key in self.projections

    def has_list_projection(self, key):
        return key in self.list_projections

    def has_key(self, key):
        return self.has_prop(key) or self.has_projection(key) or self.has_list_projection(key)

    def prop(self, key, value):
        if self.has_key(key):
            raise Exception('Key "{}" already exist'.format(key))

        self.props[key] = value
        self.keys.append(key)

    def project_one(self, key, mapper):
        if self.has_key(key):
            raise Exception('Key "{}" already exist'.format(key))

        self.projections[key] = mapper
        self.keys.append(key)

    def project_list(self, key, mapper):
        if self.has_key(key) and not self.has_list_projection(key):
            raise Exception('Key "{}" already exist'.format(key))

        if not self.has_list_projection(key):
            self.list_projections[key] = []

        self.list_projections[key].append(mapper)
        self.keys.append(key)

    def apply(self, obj):
        result = {}

        for key in self.keys:
            if key in self.props:
                result[key] = self.props[key]

            elif key in self.projections:
                result[key] = apply_projection(self.projections[key], obj)

            elif key in self.list_projections:
                result[key] = []

                for projection in self.list_projections[key]:
                    result[key].append(apply_projection(projection, obj))

        return result
