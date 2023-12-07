# start from base
FROM ubuntu:20.04

# install system-wide deps for python
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg build-essential vim git

# copy our application code
RUN mkdir /PROJECT
WORKDIR /PROJECT

# install required elements
RUN pip3 install --upgrade pip
RUN pip3 install nnf
RUN pip3 install bauhaus
RUN pip3 install aenum
RUN pip3 install datetime
RUN pip3 install requests
RUN pip3 install flask
RUN pip3 install flask_cors


# install dsharp to run in the container
RUN curl https://mulab.ai/cisc-204/dsharp -o /usr/local/bin/dsharp
RUN chmod u+x /usr/local/bin/dsharp

# Expose the port that your app will run on
EXPOSE 5000

# default command to execute when container starts
CMD /bin/bash
