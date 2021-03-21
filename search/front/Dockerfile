FROM python:3.6.5

RUN pip3.6 install --upgrade pip
RUN pip3 install flask numpy

COPY . ./front
WORKDIR ./front

# EXPOSE 5000
ENV FLASK_APP=search_app.py
ENV FLASK_ENV=development
# ENTRYPOINT ["python3"]
CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["python3", "wait.py"]
