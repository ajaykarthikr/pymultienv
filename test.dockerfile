# Use the official Python base image with version 3.10.0
FROM python:3.10.0

# Install poetry
RUN pip install --no-cache-dir poetry

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the working directory
COPY poetry.lock pyproject.toml ./

# Install the project dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the entire project directory to the working directory
COPY . .

ENV TEST_DIR=/app/tests

# Run the unit tests
CMD ["poetry", "run", "python", "-m", "unittest", "discover", "tests"]
