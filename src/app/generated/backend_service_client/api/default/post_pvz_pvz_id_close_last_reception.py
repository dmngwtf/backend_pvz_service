from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.reception import Reception
from ...types import Response


def _get_kwargs(
    pvz_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/pvz/{pvz_id}/close_last_reception",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, Reception]]:
    if response.status_code == 200:
        response_200 = Reception.from_dict(response.json())

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
) -> Response[Union[Error, Reception]]:
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
) -> Response[Union[Error, Reception]]:
    """Закрытие последней открытой приемки товаров в рамках ПВЗ

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Reception]]
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
) -> Optional[Union[Error, Reception]]:
    """Закрытие последней открытой приемки товаров в рамках ПВЗ

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Reception]
    """

    return sync_detailed(
        pvz_id=pvz_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pvz_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Error, Reception]]:
    """Закрытие последней открытой приемки товаров в рамках ПВЗ

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Reception]]
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
) -> Optional[Union[Error, Reception]]:
    """Закрытие последней открытой приемки товаров в рамках ПВЗ

    Args:
        pvz_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Reception]
    """

    return (
        await asyncio_detailed(
            pvz_id=pvz_id,
            client=client,
        )
    ).parsed
