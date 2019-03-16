from mapper import Mapper

THRESHOLDS = [
    {
        'type': 'errors',
        'prefix': 'errors',
        'danger_value': 0.2
    },
    {
        'type': 'zeroes',
        'prefix': 'zeroes',
        'danger_value': 0.1
    },
    {
        'type': 'timeouts',
        'prefix': 'timeout',
        'danger_value': 0.1
    }
]

CONVERSIONS = [
    {
        'type': 'searches',
        'prefix': 'searches',
        'indicators': ['web_pessimizer', 'mobile_pessimizer']
    },
    {
        'type': 'clicks',
        'prefix': 'clicks',
        'indicators': ['ctr']
    },
    {
        'type': 'bookings',
        'prefix': 'bookings',
        'indicators': ['str', 'avg_price'],
        'final': True
    }
]

NON_PREFIXED_INDICATORS = ['web_pessimizer', 'mobile_pessimizer']


def make_data_path(key):
    return ['data', 0, key]


def make_threshold_mapper(period, threshold):
    mapper = Mapper()

    mapper.prop('type', threshold.get('type'))
    mapper.prop('dangerValue', threshold.get('danger_value'))

    value_key = '_'.join([threshold.get('prefix'), period])
    mapper.project_one('value', make_data_path(value_key))

    return mapper


def make_indicator_mapper(period, indicator):
    mapper = Mapper()
    mapper.prop('type', indicator)

    value_key = indicator
    if indicator not in NON_PREFIXED_INDICATORS:
        value_key = '_'.join([indicator, period])
    mapper.project_one('value', make_data_path(value_key))

    return mapper


def make_conversion_mapper(period, conversion):
    mapper = Mapper()
    mapper.prop('type', conversion.get('type'))

    value_key = '_'.join([conversion.get('prefix'), 'current', period])
    mapper.project_one('value', make_data_path(value_key))

    prev_value_key = '_'.join([conversion.get('prefix'), 'previous', period])
    mapper.project_one('prevValue', make_data_path(prev_value_key))

    if conversion.get('final', False):
        mapper.prop('final', True)

    for indicator in conversion.get('indicators', []):
        mapper.project_list(
            'indicators', make_indicator_mapper(period, indicator))

    return mapper


def make_stats_mapper(periods):
    period_mappers = {period: Mapper() for period in periods}

    mapper = Mapper()

    for period, period_mapper in period_mappers.items():
        for threshold in THRESHOLDS:
            period_mapper.project_list(
                'thresholds', make_threshold_mapper(period, threshold))

        period_mapper.project_one('errorLevels', ['errors_' + period])

        for conversion in CONVERSIONS:
            period_mapper.project_list(
                'conversions', make_conversion_mapper(period, conversion))

        mapper.project_one(period, period_mapper)

    return mapper
