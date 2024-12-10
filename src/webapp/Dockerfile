FROM python:3.11-slim
RUN mkdir /app
RUN mkdir /model
COPY sentiment-analyzer-model /model
WORKDIR /app
RUN pip install mlflow fastapi uvicorn
COPY . /app


ARG MLFLOW_SERVER_URI
ARG MODEL_NAME
ARG MODEL_VERSION

#RUN python get_mlflow_model.py --mlflow_server_uri=${MLFLOW_SERVER_URI} --model_name=${MODEL_NAME} --model_version=${MODEL_VERSION} --target_path=/model


RUN pip install -r /model/requirements.txt


EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]