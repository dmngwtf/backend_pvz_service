import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.pvz_city import PVZCity
from ..types import UNSET, Unset

T = TypeVar("T", bound="PVZ")


@_attrs_define
class PVZ:
    """
    Attributes:
        city (PVZCity):
        id (Union[Unset, UUID]):
        registration_date (Union[Unset, datetime.datetime]):
    """

    city: PVZCity
    id: Union[Unset, UUID] = UNSET
    registration_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        city = self.city.value

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        registration_date: Union[Unset, str] = UNSET
        if not isinstance(self.registration_date, Unset):
            registration_date = self.registration_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "city": city,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if registration_date is not UNSET:
            field_dict["registrationDate"] = registration_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        city = PVZCity(d.pop("city"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _registration_date = d.pop("registrationDate", UNSET)
        registration_date: Union[Unset, datetime.datetime]
        if isinstance(_registration_date, Unset):
            registration_date = UNSET
        else:
            registration_date = isoparse(_registration_date)

        pvz = cls(
            city=city,
            id=id,
            registration_date=registration_date,
        )

        pvz.additional_properties = d
        return pvz

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
