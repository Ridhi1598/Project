FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Install Allure
RUN apt-get update && apt-get install -yqq wget && \
   wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.21.0/allure-commandline-2.21.0.zip && \
   unzip allure-commandline-2.21.0.zip -d /opt && \
   ln -s /opt/allure-2.21.0/bin/allure /usr/bin/allure && \
   rm allure-commandline-2.21.0.zip

ENV PATH="/opt/allure-2.2.1/bin:${PATH}"

# Install Java
RUN apt-get update \
   && apt-get install -yqq openjdk-11-jdk

RUN apt-get install -yqq google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Set chrome driver version
ENV CHROMEDRIVER_VERSION 111.0.5563.64
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download the Chrome Driver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Set display port as an environment variable
ENV DISPLAY=:99


# Set working directory
WORKDIR TINAA

# Add requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# Add all files to repo
ADD ./ .

# Unzip oc folder and delete zipped file
RUN unzip oc.zip
RUN chmod 777 oc -R
RUN rm oc.zip

# Add permissions for bin folder
RUN chmod -R 777 /usr/local/bin/

# Add permissions for mnt folder
RUN chmod -R 777 /mnt/test-automation/

# Copy oc binary file to the path
RUN cp oc/oc /usr/local/bin/

# Unzip email folder and delete zipped file
RUN unzip email.zip
RUN rm email.zip

# install exporter library
RUN pip install 'email/Exporter'

CMD ["python", "Test_Runner.py", "bi", "preprod","./features/feature_UIFunctional/bi/TC_70_BI_Service_Dashboard_Login.feature"]