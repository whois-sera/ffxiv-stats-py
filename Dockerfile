FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

ENTRYPOINT [ "python" ]

#CMD [ "ffxiv_stats.py" ]