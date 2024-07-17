FROM python:3.10-bullseye

RUN apt update && apt install -y default-jdk

WORKDIR /app
ADD ./requirements.txt .
RUN python -m venv /app/venv && export PATH="/app/venv/bin:$PATH" &&  \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 10000 -r requirements.txt && \
    venv-pack -p /app/venv -o venv.tar.gz

COPY . .

ENV PATH="/app/venv/bin:$PATH"
ENV GIT_URL=-"https://github.com/ali21msh"
ENV GIT_ACCESS_TOKEN="glpat-GUAtbvckyfy8wqwnuwzw"
ENV GIT_REPO_ID=115
ENV PIPELINE_PATH=pipeline.yml
ENV PROFILE=production
ENV PYSPARK_DRIVER_PYTHON=python
ENV PYSPARK_PYTHON="./environment/bin/python"
CMD ["python","main.py"]
