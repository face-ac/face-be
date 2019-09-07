#!/usr/bin/python
# -*- coding: utf-8 -*-

from face.app import create_app
from face.db.config import DevelopmentConfig, ProductionConfig
import os

if __name__ == "__main__":
    if os.environ.get("ENV") == "PROD":
        app = create_app(ProductionConfig)
        app.run(
            port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", use_reloader=False
        )
    else:
        app = create_app(DevelopmentConfig)
        app.run(port=8080, host="0.0.0.0", use_reloader=True)
