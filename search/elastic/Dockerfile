FROM python:3.6.5

RUN pip3.6 install --upgrade pip
RUN pip3 install elasticsearch tqdm numpy

RUN mkdir filler
COPY load_data.py ./filler/load_data.py
COPY configs ./filler/configs
WORKDIR ./filler

ENTRYPOINT ["python3"]
CMD ["load_data.py"]

