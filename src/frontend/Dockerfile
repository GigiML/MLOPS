FROM python:3.11-slim

WORKDIR /frontend

RUN pip install streamlit

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]