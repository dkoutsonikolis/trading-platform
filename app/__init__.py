from flask import Flask, Blueprint

from .config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

trading_stats_bp = Blueprint("trading_stats_bp", __name__, url_prefix="/api/trading-statistics")

from .api.views import trading_statistics

app.register_blueprint(trading_stats_bp)
