FROM python:3.10-slim-buster AS build

WORKDIR /app

COPY main.py test_main.py ./

RUN python -m pip install dpath

FROM build AS test
RUN python -m pip install pytest
RUN pytest -v

FROM build AS final
CMD [ "python3", "main.py" ]