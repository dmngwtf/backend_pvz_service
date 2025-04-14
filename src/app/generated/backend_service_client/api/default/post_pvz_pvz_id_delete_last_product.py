from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    pvz_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/pvz/{pvz_id}/delete_last_product",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pvz_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Error]]:
    """Удаление последнего добавленного товара из текущей приемки (LIFO, только для сотрудников ПВЗ)

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        pvz_id=pvz_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pvz_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, Error]]:
    """Удаление последнего добавленного товара из текущей приемки (LIFO, только для сотрудников ПВЗ)

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        pvz_id=pvz_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pvz_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, Error]]:
    """Удаление последнего добавленного товара из текущей приемки (LIFO, только для сотрудников ПВЗ)

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        pvz_id=pvz_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pvz_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, Error]]:
    """Удаление последнего добавленного товара из текущей приемки (LIFO, только для сотрудников ПВЗ)

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            pvz_id=pvz_id,
            client=client,
        )
    ).parsed
