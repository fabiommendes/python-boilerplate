from django.conf.urls import url
from django import http


def index_view(request):
    return http.HttpResponse("""<!DOCTYPE html>

<html>
<head>
    <title>Dockerized Django Test Server</title>
    <!-- This stylesheet is served by Nginx! -->
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>
    <h1>Congratulations!</h1>
    <p>Your docker container is working! Of course you must still configure it 
    for your application. The best way to do it is to create a Dockerfile that
    is based on this image:
    
<code><pre>
# Dockerfile
FROM pythonboilerplate/django:base

# Tell docker the python path of your application
ENV GUNICORN_WSGI_APPLICATION=my_application.wsgi 

# Assuming that your project files are under src/:
ADD . /app
 
</pre></code>
    </p>
    <p>Enjoy :)</p>
        
</body>
</html>
""")

urlpatterns = [
    url(r'^$', index_view),
]
