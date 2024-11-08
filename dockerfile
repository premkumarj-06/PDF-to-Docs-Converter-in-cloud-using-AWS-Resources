FROM public.ecr.aws/lambda/python:3.10.2024.03.04.10

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# # Copy requirements.txt
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}

# Install the Python dependencies
RUN pip install -r requirements.txt

COPY ./src/  ${LAMBDA_TASK_ROOT}/src/


ENV PYTHONPATH "${PYTHONPATH}:${LAMBDA_TASK_ROOT}/src"

# Set woring directory
WORKDIR ${LAMBDA_TASK_ROOT}/src

# Set the CMD to your handler
CMD [ "python/doc_transfer_lambda/main.handler" ]