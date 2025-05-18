import pytest

from .functions import get_eng_slug

def test_get_eng_slug():

    result = get_eng_slug("Горохов Алексей Анатольевич")


    assert isinstance(result, str)
    assert result == "aleksey-Anatolyevich-GOROKHOV"
