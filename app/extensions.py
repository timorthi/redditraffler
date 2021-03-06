from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate(directory="app/db/migrations")
rq = RQ()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second"])
csrf = CSRFProtect()
cache = Cache()
talisman = Talisman()
