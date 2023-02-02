# import pytest
from monarch_py.implementations.sql.sql_implementation import SQLImplementation


def test_entity():
    data = SQLImplementation()
    entity = data.get_entity("MONDO:0007947")
    assert entity
    assert entity.name == "Marfan syndrome"

