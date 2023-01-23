import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Dict, List, Tuple

import dpath


class InvalidDataException(Exception):
    """Raise if data provided is invalid."""


def build_dict(
    dict_obj: Dict[str, Any], path: List[str], key: str
) -> Dict[str, Any]:
    dpath.new(dict_obj, path, key)
    return dict_obj


def deep_update(
    source: Dict[str, Any], overrides: Dict[str, Any]
) -> Dict[str, Any]:
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]

    return source


@dataclass
class WelcomeProject:
    data: Dict[str, Any] = field(default_factory=dict)
    allowed_verbs: List[str] = field(
        default_factory=lambda: ["GET", "POST", "PATCH", "DELETE"]
    )

    def run(self, data: List[Tuple[str, str]]) -> Dict[str, Any]:
        if not isinstance(data, list):
            raise TypeError()

        if not data:
            raise ValueError()

        self.handle(data)

        return self.data

    def handle(self, data: List[Tuple[str, str]]) -> None:
        current_dict = {}

        for row in data:
            verb, path = row

            if verb not in self.allowed_verbs:
                raise InvalidDataException(
                    f"Method {verb} not in {self.allowed_verbs}"
                )

            try:
                # We don't need API version and all parameters in curly brackets
                path = re.sub(r"\/api\/v\d\/", "", path)
                path = re.sub(r"\/\{(\w+)\}", "", path)

                # Building dict object from slash-separated path
                dpath.new(current_dict, path, verb)
            except Exception as error:
                raise InvalidDataException(f"Can't parse data: {str(error)}")

        deep_update(self.data, current_dict)


if __name__ == "__main__":
    app = WelcomeProject()

    service1 = [
        ("GET", "/api/v1/cluster/metrics"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
    ]

    service2 = [
        ("GET", "/api/v1/cluster/freenodes/list"),
        ("GET", "/api/v1/cluster/nodes"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
    ]

    result = app.run(service1)
    print("First run: ")
    pprint(app.data)

    result = app.run(service2)
    print("Second run: ")
    pprint(app.data)
