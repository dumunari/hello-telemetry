# Use the official Tomcat image from the Docker Hub
FROM tomcat:11.0

# Donwload Java Agent
ADD --chmod=644 https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar /opt/opentelemetry-javaagent.jar

# Copy your web application WAR file to the Tomcat webapps directory
COPY MyWebApp.war /usr/local/tomcat/webapps/

# Start Tomcat
CMD ["catalina.sh", "run"]