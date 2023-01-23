import pytest

from main import InvalidDataException, WelcomeProject


def test_welcome_project() -> None:
    # Arrange
    data = [
        ("GET", "/api/v1/cluster/metrics"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
    ]
    app = WelcomeProject()

    # Act
    result = app.run(data)

    # Assert
    assert result == {
        "cluster": {
            "metrics": "GET",
            "plugins": "POST",
        },
    }


def test_welcome_project_if_data_has_wrong_type() -> None:
    # Arrange
    data = "foo"
    app = WelcomeProject()

    # Act
    with pytest.raises(TypeError):
        app.run(data)


def test_welcome_project_if_no_data_provided() -> None:
    # Arrange
    data = []
    app = WelcomeProject()

    # Act
    with pytest.raises(ValueError):
        app.run(data)


def test_welcome_project_sequential_run() -> None:
    # Arrange
    data_1 = [
        ("GET", "/api/v1/cluster/metrics"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
    ]
    data_2 = [
        ("GET", "/api/v1/cluster/freenodes/list"),
        ("GET", "/api/v1/cluster/nodes"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
    ]
    app = WelcomeProject()

    # Act
    result = app.run(data_1)
    result = app.run(data_2)

    # Assert
    assert result == {
        "cluster": {
            "freenodes": {"list": "GET"},
            "metrics": "GET",
            "nodes": "GET",
            "plugins": "POST",
        }
    }


def test_welcome_project_invalid_data() -> None:
    # Arrange
    data = [
        ("GET", {"this is not": "right"}),
    ]
    app = WelcomeProject()

    # Act
    with pytest.raises(InvalidDataException):
        app.run(data)


def test_welcome_project_invalid_verb() -> None:
    # Arrange
    data = [
        ("FOO", "bar"),
    ]
    app = WelcomeProject()

    # Act
    with pytest.raises(InvalidDataException):
        app.run(data)
