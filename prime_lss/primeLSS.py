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
    action: int
    id: str
    new_url: str
    original_url: str
    original_url_status_code: int
    repo_status: int

    @staticmethod
    def from_dict(obj: Any) -> "PrimeLSSElement":
        assert isinstance(obj, dict)
        action = from_int(obj.get("Action"))
        id = from_str(obj.get("id"))
        new_url = from_str(obj.get("NewURL"))
        original_url = from_str(obj.get("OriginalURL"))
        original_url_status_code = from_int(obj.get("OriginalURLStatusCode"))
        repo_status = from_int(obj.get("RepoStatus"))
        return PrimeLSSElement(
            action, id, new_url, original_url, original_url_status_code, repo_status
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["Action"] = from_int(self.action)
        result["id"] = from_str(self.id)
        result["NewURL"] = from_str(self.new_url)
        result["OriginalURL"] = from_str(self.original_url)
        result["OriginalURLStatusCode"] = from_int(self.original_url_status_code)
        result["RepoStatus"] = from_int(self.repo_status)
        return result


def coordinate_from_dict(s: Any) -> List[PrimeLSSElement]:
    return from_list(PrimeLSSElement.from_dict, s)


def coordinate_to_dict(x: List[PrimeLSSElement]) -> Any:
    return from_list(lambda x: to_class(PrimeLSSElement, x), x)
