# Use latest Python runtime as image
FROM python:3.6.10-slim

# Set the working directory to /app and copy current dir
WORKDIR /app
#COPY . /app
COPY requirements.txt .
COPY templates/ .
COPY static/ .
COPY erie_server.py .
COPY erie_model_45005.h5 .

# See: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN pip install virtualenv
RUN virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP=erie_server.py

EXPOSE 5000

# Run Python script when the container launches
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

#RUN mkdir /opt/erie_server/
#WORKDIR /opt/erie_server/
#
#COPY requirements.txt .
#COPY templates/ .
#COPY static/ .
#COPY erie_server.py .
#COPY erie_model_45005.h5 .
#
#RUN pip install numpy
#RUN pip install pandas
#RUN pip install tensorflow
#RUN pip install flask
#
#CMD [ "ls" ]
#CMD [ "python", "erie_server.py" ]