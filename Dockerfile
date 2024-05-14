# 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --upgrade pip

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 运行Django服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
