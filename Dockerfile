FROM python:3.12.4-buster

RUN apt-get update -qq && apt-get -y install ffmpeg

WORKDIR /usr/src/app

COPY . .

RUN pip install -U -r requirements.txt

CMD [ "python", "-m", "bot.sample_video_bot" ]
