# Use an official Miniconda image as the base
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the local code to the container's working directory
COPY ./whisperX /app/whisperX

# Create a new Conda environment with Python 3.10
RUN conda create --name whisperx python=3.10 -y

RUN echo "source activate whisperx" > ~/.bashrc
ENV PATH /opt/conda/envs/whisperx/bin:$PATH

# Activate the Conda environment
SHELL ["conda", "run", "-n", "whisperx", "/bin/bash", "-c"]

# Install PyTorch, torchaudio, and CUDA-specific tools from the PyTorch channel
RUN conda install pytorch==2.0.0 torchaudio==2.0.0 cudatoolkit=11.8 -c pytorch -c nvidia -y

# Install other Python dependencies
RUN pip install --no-cache-dir -r /app/whisperX/requirements.txt

# Install the WhisperX package
RUN pip install /app/whisperX

# Ensure messages and logs are immediately dumped to the stream.
# ENV PYTHONUNBUFFERED=1

EXPOSE 9080

COPY /whisperX/app.py /app/

# Set the default command to start a bash shell
#CMD ["/bin/bash"]
#CMD ["conda", "run", "-n", "whisperx", "python", "/app/whisperX/setup.py", "--help"]
# CMD ["conda", "run", "-n", "whisperx", "python", "/app/whisperX/setup.py", "install"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9080"]