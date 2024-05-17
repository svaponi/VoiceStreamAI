FROM python:3.9 as requirements-stage

# Install poetry
RUN pip install "poetry>=1.2.2"

# Use poetry to generate requirements.txt
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

# define non-root user
ARG USER=app
ARG USERID=1001
ARG GROUP=app
ARG GROUPID=1001
RUN addgroup --gid $GROUPID $GROUP
RUN adduser --uid $USERID --ingroup $GROUP $USER --disabled-password

## Define workdir
ARG WORKDIR=/workdir

# Create workdir
RUN mkdir -p $WORKDIR

# Move to workdir
WORKDIR $WORKDIR

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# install OS deps
RUN apt-get update -y \
    && apt-get install -y libasound-dev libsndfile1-dev ffmpeg

# Install deps
COPY --from=requirements-stage /tmp/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY src/app ./app

# Switch to non-root user
USER $USER

# Make port 8765 available to the world outside this container
EXPOSE 8765

# Define environment variable
ENV NAME VoiceStreamAI
ENV HOST "0.0.0.0"
ENV PORT "8765"

# Set the entrypoint to your application
ENTRYPOINT ["python3", "-m", "app.main"]
