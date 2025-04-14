from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_pvz_response_200_item_receptions_item import GetPvzResponse200ItemReceptionsItem
    from ..models.pvz import PVZ


T = TypeVar("T", bound="GetPvzResponse200Item")


@_attrs_define
class GetPvzResponse200Item:
    """
    Attributes:
        pvz (Union[Unset, PVZ]):
        receptions (Union[Unset, list['GetPvzResponse200ItemReceptionsItem']]):
    """

    pvz: Union[Unset, "PVZ"] = UNSET
    receptions: Union[Unset, list["GetPvzResponse200ItemReceptionsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pvz: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pvz, Unset):
            pvz = self.pvz.to_dict()

        receptions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.receptions, Unset):
            receptions = []
            for receptions_item_data in self.receptions:
                receptions_item = receptions_item_data.to_dict()
                receptions.append(receptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pvz is not UNSET:
            field_dict["pvz"] = pvz
        if receptions is not UNSET:
            field_dict["receptions"] = receptions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_pvz_response_200_item_receptions_item import GetPvzResponse200ItemReceptionsItem
        from ..models.pvz import PVZ

        d = dict(src_dict)
        _pvz = d.pop("pvz", UNSET)
        pvz: Union[Unset, PVZ]
        if isinstance(_pvz, Unset):
            pvz = UNSET
        else:
            pvz = PVZ.from_dict(_pvz)

        receptions = []
        _receptions = d.pop("receptions", UNSET)
        for receptions_item_data in _receptions or []:
            receptions_item = GetPvzResponse200ItemReceptionsItem.from_dict(receptions_item_data)

            receptions.append(receptions_item)

        get_pvz_response_200_item = cls(
            pvz=pvz,
            receptions=receptions,
        )

        get_pvz_response_200_item.additional_properties = d
        return get_pvz_response_200_item

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
