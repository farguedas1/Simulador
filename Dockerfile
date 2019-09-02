FROM tailordev/pandas

COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

COPY . /tmp

ENTRYPOINT ["bokeh", "serve",  "app", "--port", "80", "--allow-websocket-origin=*"]
EXPOSE 80
