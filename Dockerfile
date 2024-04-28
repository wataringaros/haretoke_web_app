# # FROM python:3.10
# # USER root

# # RUN apt-get update
# # RUN apt-get -y install locales && \
# #     localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
# # ENV LANG ja_JP.UTF-8
# # ENV LANGUAGE ja_JP:ja
# # ENV LC_ALL ja_JP.UTF-8
# # ENV TZ JST-9
# # ENV TERM xterm

# # RUN apt-get install -y vim less
# # RUN pip install --upgrade pip
# # RUN pip install --upgrade setuptools

# # # requirements.txtを作業ディレクトリにコピー
# # COPY requirements.txt .

# # # requirements.txtに記載された依存関係をインストール
# # RUN pip install --no-cache-dir -r requirements.txt

# # RUN python -m pip install jupyterlab
# # Pythonのバージョン3.10を使用する
# FROM python:3.10
# USER root

# # ロケールの設定
# RUN apt-get update && apt-get -y install locales && \
#     localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# # 環境変数の設定
# ENV LANG ja_JP.UTF-8
# ENV LANGUAGE ja_JP:ja
# ENV LC_ALL ja_JP.UTF-8
# ENV TZ JST-9
# ENV TERM xterm

# # 必要なパッケージのインストール
# RUN apt-get install -y vim less && \
#     pip install --upgrade pip setuptools && \
#     python -m pip install jupyterlab

# # 作業ディレクトリを設定
# WORKDIR /app

# # requirements.txtをコピー
# COPY requirements.txt /app/

# # requirements.txtに記載された依存関係をインストール
# RUN pip install --no-cache-dir -r requirements.txt

# Pythonのバージョン3.10を使用する
FROM python:3.10
USER root

# ロケールの設定
RUN apt-get update && apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# 環境変数の設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# 必要なパッケージのインストール
RUN apt-get install -y vim less
RUN pip install --upgrade pip setuptools

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txtをコピー
COPY requirements.txt /app/

# requirements.txtに記載された依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# JupyterLabをインストール
RUN python -m pip install jupyterlab
