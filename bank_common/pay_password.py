"""Verify payment password against bank-us."""

from __future__ import annotations

from typing import Any

from bank_common.errors import ErrorCode
from bank_common.response import fail, ok


DEFAULT_US_URL = "http://us:8001"


def _httpx():
    import httpx

    return httpx


def verify_pay_password_sync(
    authorization: str | None,
    pay_password: str | None,
    *,
    us_url: str = DEFAULT_US_URL,
    timeout: float = 5.0,
) -> dict[str, Any]:
    if not pay_password:
        return fail(ErrorCode.PAY_PASSWORD_REQUIRED, "payment password required")
    if not authorization:
        return fail(ErrorCode.UNAUTHORIZED, "missing token")
    httpx = _httpx()
    try:
        with httpx.Client(timeout=timeout) as client:
            r = client.post(
                f"{us_url.rstrip('/')}/api/auth/verify-pay-password",
                headers={"Authorization": authorization},
                json={"pay_password": pay_password},
            )
        data = r.json()
        if data.get("code") != 0:
            return data
        return ok({"verified": True})
    except Exception as exc:  # noqa: BLE001
        return fail(ErrorCode.UPSTREAM_TIMEOUT, f"pay password verify failed: {exc}")


async def verify_pay_password_async(
    authorization: str | None,
    pay_password: str | None,
    *,
    us_url: str = DEFAULT_US_URL,
    timeout: float = 5.0,
) -> dict[str, Any]:
    if not pay_password:
        return fail(ErrorCode.PAY_PASSWORD_REQUIRED, "payment password required")
    if not authorization:
        return fail(ErrorCode.UNAUTHORIZED, "missing token")
    httpx = _httpx()
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(
                f"{us_url.rstrip('/')}/api/auth/verify-pay-password",
                headers={"Authorization": authorization},
                json={"pay_password": pay_password},
            )
        data = r.json()
        if data.get("code") != 0:
            return data
        return ok({"verified": True})
    except Exception as exc:  # noqa: BLE001
        return fail(ErrorCode.UPSTREAM_TIMEOUT, f"pay password verify failed: {exc}")
