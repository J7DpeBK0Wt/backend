from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from stats_store import StatsStore

STATS_PERIODS = ['last_hour', 'yesterday', 'last_3days']

app = Flask(__name__)
CORS(app, resources=r'/api/*')

stats = StatsStore('data/stats.json', STATS_PERIODS)


@app.route('/api/stats')
def get_stats():
    period = request.args.get('period', '')

    periodStats = stats.get_period(period)

    if periodStats is None:
        abort(404)

    return jsonify({
        'period': period,
        'stats': periodStats
    })
