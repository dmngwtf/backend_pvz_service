from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.product import Product
    from ..models.reception import Reception


T = TypeVar("T", bound="GetPvzResponse200ItemReceptionsItem")


@_attrs_define
class GetPvzResponse200ItemReceptionsItem:
    """
    Attributes:
        reception (Union[Unset, Reception]):
        products (Union[Unset, list['Product']]):
    """

    reception: Union[Unset, "Reception"] = UNSET
    products: Union[Unset, list["Product"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reception: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reception, Unset):
            reception = self.reception.to_dict()

        products: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.products, Unset):
            products = []
            for products_item_data in self.products:
                products_item = products_item_data.to_dict()
                products.append(products_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reception is not UNSET:
            field_dict["reception"] = reception
        if products is not UNSET:
            field_dict["products"] = products

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product import Product
        from ..models.reception import Reception

        d = dict(src_dict)
        _reception = d.pop("reception", UNSET)
        reception: Union[Unset, Reception]
        if isinstance(_reception, Unset):
            reception = UNSET
        else:
            reception = Reception.from_dict(_reception)

        products = []
        _products = d.pop("products", UNSET)
        for products_item_data in _products or []:
            products_item = Product.from_dict(products_item_data)

            products.append(products_item)

        get_pvz_response_200_item_receptions_item = cls(
            reception=reception,
            products=products,
        )

        get_pvz_response_200_item_receptions_item.additional_properties = d
        return get_pvz_response_200_item_receptions_item

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
