# Stage 1: Build and download dependencies
FROM python:3.11-slim

# Install system dependencies required for downloading and building
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /home/containeruser

# Create a virtual environment
ENV VIRTUALENV=/home/containeruser/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir torch
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Download the Whisper model
RUN python -c "import whisper; whisper.load_model('tiny')"

# # Stage 2: Setup the final image
# FROM python:3.11-slim

ENV INCOMING_DIR="/home/containeruser/src/incomingFiles" \
    NEXT_DIR="/home/containeruser/src/nextFiles" \
    WHISPER_MODEL_DIR="/root/.cache/whisper"

# # Install system dependencies required for downloading and building
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libsndfile1 \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory in the container
# WORKDIR /home/containeruser

# ENV VIRTUALENV=/home/containeruser/venv
# RUN python3 -m venv $VIRTUALENV
# ENV PATH="$VIRTUALENV/bin:$PATH"

# # Copy only the necessary files from the builder stage
# COPY --from=builder /build/venv /venv
# COPY --from=builder /root/.cache/whisper /root/.cache/whisper

# # Copy the src directory contents into the container at /src
# COPY --chown=containeruser src/ src/
COPY src/ src/

RUN mkdir $NEXT_DIR 
# RUN chown -R containeruser:containeruser $NEXT_DIR
# RUN chmod -R 755 $NEXT_DIR

# Run the application
ENTRYPOINT ["python", "-m", "src.file_access.app"]

# # Stage 1: Build and download dependencies
# FROM python:3.11-slim AS builder

# # Install system dependencies required for downloading and building
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libsndfile1 \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory in the container
# WORKDIR /build

# ENV VIRTUALENV=/build/venv
# RUN python3 -m venv $VIRTUALENV
# ENV PATH="$VIRTUALENV/bin:$PATH"

# # Install Python dependencies
# RUN pip install --no-cache-dir torch
# RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git

# # Download the Whisper model
# RUN python -c "import whisper; whisper.load_model('tiny')"

# # Stage 2: Setup the final image
# FROM python:3.11-slim

# ENV INCOMING_DIR="/home/containeruser/src/incomingFiles" \
#     NEXT_DIR="/home/containeruser/src/nextFiles"

# # Install system dependencies required for downloading and building
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libsndfile1 \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory in the container
# WORKDIR /home/containeruser

# ENV VIRTUALENV=/home/containeruser/venv
# RUN python3 -m venv $VIRTUALENV
# ENV PATH="$VIRTUALENV/bin:$PATH"

# # Copy only the necessary files from the builder stage
# COPY --from=builder /build/venv /venv
# COPY --from=builder /root/.cache/whisper /root/.cache/whisper

# # Copy the src directory contents into the container at /src
# COPY --chown=containeruser src/ src/

# RUN mkdir $NEXT_DIR 
# RUN chown -R containeruser:containeruser $NEXT_DIR
# RUN chmod -R 755 $NEXT_DIR

# # Run the application
# ENTRYPOINT ["python", "-m", "src.file_access.app"]