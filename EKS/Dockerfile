FROM ubuntu:20.04
WORKDIR ./home/bot/
RUN apt update -y
RUN apt install git -y
RUN apt install python3-pip -y
RUN pip install keras 
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.5.0-cp38-cp38-manylinux2010_x86_64.whl
RUN pip install asyncio
RUN pip install boto3 
RUN pip install pandas 
RUN pip install mlflow 
RUN apt install ufw -y
RUN apt install iptables -y
RUN git clone https://github.com/CEDipEngineering/docker_exec_file