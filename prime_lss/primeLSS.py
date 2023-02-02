# Code generated from https://app.quicktype.io/#l=schema

from dataclasses import dataclass
from typing import Any, Callable, List, Type, TypeVar, cast

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PrimeLSSElement:
    id: int
    original_url: str
    new_url: str
    original_url_status_code: str
    action: int

    @staticmethod
    def from_dict(obj: Any) -> "PrimeLSSElement":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        original_url = from_str(obj.get("OriginalURL"))
        new_url = from_str(obj.get("NewURL"))
        original_url_status_code = from_str(obj.get("OriginalURLStatusCode"))
        action = from_int(obj.get("Action"))
        return PrimeLSSElement(
            id, original_url, new_url, original_url_status_code, action
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["OriginalURL"] = from_str(self.original_url)
        result["NewURL"] = from_str(self.new_url)
        result["OriginalURLStatusCode"] = from_str(self.original_url_status_code)
        result["Action"] = from_int(self.action)
        return result


def prime_lss_from_dict(s: Any) -> List[PrimeLSSElement]:
    return from_list(PrimeLSSElement.from_dict, s)


def prime_lss_to_dict(x: List[PrimeLSSElement]) -> Any:
    return from_list(lambda x: to_class(PrimeLSSElement, x), x)
