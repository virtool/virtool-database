import json
import arrow
import pytest
import subprocess


@pytest.mark.parametrize("version", [None, "v1.0.1", "v0.8.3"])
def test_version(version, tmpdir):
    """
    Test that the version field is correctly set in the viruses.json file.

    """
    json_file = tmpdir.join("viruses.json")

    command = ["python", "scripts/build.py", "-f", str(json_file), "src"]

    if version:
        command += ["-V", version]

    subprocess.call(command)

    built_json = json.load(json_file)

    assert built_json["version"] == version


def test_created_at(tmpdir):
    """
    Test that the version field is correctly set in the viruses.json file.

    """
    json_file = tmpdir.join("viruses.json")

    subprocess.call(["python", "scripts/build.py", "-f", str(json_file), "src"])

    built_json = json.load(json_file)

    created_at = arrow.get(built_json["created_at"])

    assert (arrow.utcnow() - created_at).seconds == 0
