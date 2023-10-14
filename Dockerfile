FROM python

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install Flask

COPY . /app

WORKDIR /app

CMD [ "python", "-u","redirector.py" ]
