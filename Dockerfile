FROM python:3.12.0

WORKDIR /app

COPY . .
RUN pwd 
RUN ls 
RUN ls /app

# 返回

# # 安装uv和poetry
# # 如果是中国大陆用户，可以设置国内源
# # RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip install --no-cache-dir uv \
#     && pip install --no-cache-dir poetry \
#     # && uv venv && chmod +x .venv/bin/activate \
#     # && .venv/bin/activate \
#     && ls \
#     && ls /app \
#     && rm -rf /app/.venv \
#     && poetry install  --no-root

# EXPOSE 8020

# CMD ["uv", "run", "main.py", "--host", "0.0.0.0", "--port", "8020"]