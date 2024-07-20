FROM python:3.9-slim-buster

RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501

ENV PORT 8051

CMD [ "streamlit",'run',"virtual_doc.py" ]