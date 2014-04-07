
from werkzeug.contrib.fixers import ProxyFix

import os
from audience import app

#port = int(os.environ.get('PORT', 33507))
app.wsgi_app = ProxyFix(app.wsgi_app)
app.run(host='0.0.0.0')#, port=port)

app = app