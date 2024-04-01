FROM python:3.10.13-bookworm


RUN apt-get update
RUN apt-get install apt-transport-https aptitude -y
RUN apt-get install wget -y
RUN apt-get update
RUN apt-get install gcc pandoc texlive-xetex texlive-fonts-recommended texlive-plain-generic -y

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code

CMD ["bash"]
