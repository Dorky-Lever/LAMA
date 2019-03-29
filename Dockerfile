# Use an official Python runtime as a parent image
FROM ubuntu:18.04

# Enable neurodebian
#RUN wget -O- http://neuro.debian.net/lists/bionic.de-md.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
#RUN apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9

RUN apt update 
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt install -y tzdata
RUN apt install -y r-base 
RUN apt install -y python3-pip
RUN apt install nano
RUN apt install wget
RUN apt install -y python3-tk
RUN apt install -y nfs-common
RUN apt install -y nfs-client

#RUN apt install neurodebian
#RUN apt install fsl-5.0-core

WORKDIR /lama

# Make a mount point for scratch space and mount it
RUN mkdir /IMPC_research

# Copy the current directory contents into the container at /lama
ADD . /lama

RUN touch /root/.bashrc
RUN echo "export PS1="[docker:$container@\N]# "" >> /root/.bashrc
RUN echo "mount -t nfs -o rw,bg,hard,intr,tcp,vers=3,timeo=1000,retrans=10,rsize=32768,wsize=32768,nolock walter:/IMPC_research /IMPC_research" >> /root/.bashrc
RUN echo "export LC_ALL=C.UTF-8"  >> /root/.bashrc
RUN echo "export LANG=C.UTF-8" >> /root/.bashrc
#RUN echo "export PYTHONPATH=$PYTHONPATH:/lama:/lama/stats" >> /root/.bashrc


# Make port 80 available to the world outside this container
EXPOSE 80

# Install any needed packages specified in requirements.txt
#RUN chmod u+x /lama/setup_LAMA.sh
#RUN /lama/setup_LAMA.sh
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip3 install pipenv
# Was getting an error installing pyradiomics otherwise. See https://github.com/pypa/pipenv/issues/2924
RUN pipenv run pip install pip==18.0
#using pip
RUN pipenv install --system  --deploy