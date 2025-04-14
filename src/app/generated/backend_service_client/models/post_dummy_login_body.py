from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_dummy_login_body_role import PostDummyLoginBodyRole

T = TypeVar("T", bound="PostDummyLoginBody")


@_attrs_define
class PostDummyLoginBody:
    """
    Attributes:
        role (PostDummyLoginBodyRole):
    """

    role: PostDummyLoginBodyRole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = PostDummyLoginBodyRole(d.pop("role"))

        post_dummy_login_body = cls(
            role=role,
        )

        post_dummy_login_body.additional_properties = d
        return post_dummy_login_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
