FROM python:3.9.19-slim 

# تنظیم منطقه زمانی به تهران
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# make dir
RUN mkdir -p /logs 
WORKDIR /bot

# copy all file to dir '/bot'
COPY . .

# install requrment 
RUN pip install --no-cache-dir -r requirements.txt

# کپی فایل تنظیمات logrotate
#COPY logrotate.conf /etc/logrotate.d/bot-logrotate.conf

#run code
CMD ["python", "main.py"]
# CMD ["sh", "-c", "python main.py > /logs/output.log 2>&1"]
