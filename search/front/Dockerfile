FROM python:3.6.5

RUN pip3.6 install --upgrade pip
RUN pip3 install flask

COPY . ./front
WORKDIR ./front

EXPOSE 5000
ENV FLASK_APP=search_app.py
# ENTRYPOINT ["python3"]
CMD ["flask", "run"]
