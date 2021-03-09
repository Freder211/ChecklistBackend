FROM python:3

WORKDIR /backend_cl

RUN pip install --upgrade pip

COPY requirements.txt /backend_cl/requirements.txt

RUN pip install -r requirements.txt
RUN pip install djangorestframework
RUN pip install djangorestframework-simplejwt

RUN python -m pip install uvicorn[standard] gunicorn

COPY . /backend_cl/

EXPOSE 8000

RUN chmod +x run_container.sh
CMD ["./run_container.sh"]