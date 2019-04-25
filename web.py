import os
import sys

sys.path.append(os.path.dirname(__name__))

from web import create_app

# create an app instance
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
