# -*- coding: utf-8 -*-

import os

from ludaweb import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9002))
    app.run('0.0.0.0', port=port)
