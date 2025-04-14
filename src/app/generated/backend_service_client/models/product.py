import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.product_type import ProductType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Product")


@_attrs_define
class Product:
    """
    Attributes:
        type_ (ProductType):
        reception_id (UUID):
        id (Union[Unset, UUID]):
        date_time (Union[Unset, datetime.datetime]):
    """

    type_: ProductType
    reception_id: UUID
    id: Union[Unset, UUID] = UNSET
    date_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        reception_id = str(self.reception_id)

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        date_time: Union[Unset, str] = UNSET
        if not isinstance(self.date_time, Unset):
            date_time = self.date_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "receptionId": reception_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if date_time is not UNSET:
            field_dict["dateTime"] = date_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ProductType(d.pop("type"))

        reception_id = UUID(d.pop("receptionId"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _date_time = d.pop("dateTime", UNSET)
        date_time: Union[Unset, datetime.datetime]
        if isinstance(_date_time, Unset):
            date_time = UNSET
        else:
            date_time = isoparse(_date_time)

        product = cls(
            type_=type_,
            reception_id=reception_id,
            id=id,
            date_time=date_time,
        )

        product.additional_properties = d
        return product

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
