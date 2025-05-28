FROM amazonlinux:2023

# Install Python 3.11 It should match your Lambda Runtime
RUN yum -y update && \
    yum -y install python3.11 python3.11-pip python3.11-devel gcc git zip && \
    yum clean all

# Create symbolic links for Python 3.11
RUN alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    alternatives --set python /usr/bin/python3.11 && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/pip3.11 /usr/bin/pip

# Upgrade pip
RUN python -m pip install --upgrade pip

WORKDIR /var/task

# Copy all necessary files
COPY requirements.txt .
COPY lambda_function.py .
COPY tools/ ./tools/

# Install dependencies (groq and pydantic explicitly, or via requirements.txt)
RUN pip install groq==0.25.0 pydantic -t .

# Remove unnecessary files to reduce package size
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find . -name "*.pyc" -delete
RUN find . -name "*.so" -exec strip {} \; 2>/dev/null || true

# Create deployment package
RUN zip -r9 lambda_package.zip . -x "*.zip" "Dockerfile*" "requirements.txt"
