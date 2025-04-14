import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.reception_status import ReceptionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Reception")


@_attrs_define
class Reception:
    """
    Attributes:
        date_time (datetime.datetime):
        pvz_id (UUID):
        status (ReceptionStatus):
        id (Union[Unset, UUID]):
    """

    date_time: datetime.datetime
    pvz_id: UUID
    status: ReceptionStatus
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_time = self.date_time.isoformat()

        pvz_id = str(self.pvz_id)

        status = self.status.value

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dateTime": date_time,
                "pvzId": pvz_id,
                "status": status,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date_time = isoparse(d.pop("dateTime"))

        pvz_id = UUID(d.pop("pvzId"))

        status = ReceptionStatus(d.pop("status"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        reception = cls(
            date_time=date_time,
            pvz_id=pvz_id,
            status=status,
            id=id,
        )

        reception.additional_properties = d
        return reception

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
