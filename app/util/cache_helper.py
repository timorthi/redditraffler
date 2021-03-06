from flask import current_app

from app.extensions import cache


def fetch(key, value_generator=None, ttl_seconds=None):
    cached_value = cache.get(key)
    if cached_value:
        current_app.logger.debug(f"Using cached value for '{key}'")
        return cached_value

    if not (value_generator and ttl_seconds):
        current_app.logger.debug(
            "Cache missed and either value_generator or ttl_seconds are missing. Short \
                circuiting."
        )
        return None

    value = value_generator()  # Let any error here bubble up.
    succeeded = cache.set(key, value, timeout=ttl_seconds)
    if not succeeded:
        raise RuntimeError("Error while trying to set cache key")

    current_app.logger.debug(
        f"Using fresh value for '{key}', TTL {ttl_seconds} seconds"
    )
    return value
