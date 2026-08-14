# tests/test_api.py
import pytest
from app.config import settings

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Verifies endpoints reject requests without a valid X-API-Key header."""
    response = await client.get("/api/v1/stores")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing X-API-Key header."

@pytest.mark.asyncio
async def test_register_store_ssrf_blocked(client):
    """Verifies that registration of private/loopback IP targets is blocked."""
    headers = {"X-API-Key": settings.API_KEY.get_secret_value()}
    payload = {
        "name": "Malicious Internal Target",
        "url": "http://127.0.0.1:8000/internal",
        "manager_email": "admin@internal.local"
    }
    response = await client.post("/api/v1/stores", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Invalid target URL or internal IP restricted" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_and_list_stores(client):
    """Tests successful store registration and listing."""
    headers = {"X-API-Key": settings.API_KEY.get_secret_value()}
    payload = {
        "name": "Luxury Fashion Hub",
        "url": "https://example.com",
        "manager_email": "manager@example.com"
    }

    # 1. Register Store
    create_res = await client.post("/api/v1/stores", json=payload, headers=headers)
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["name"] == "Luxury Fashion Hub"
    assert data["url"] == "https://example.com/"
    assert "id" in data

    # 2. List Stores
    list_res = await client.get("/api/v1/stores", headers=headers)
    assert list_res.status_code == 200
    stores = list_res.json()
    assert len(stores) >= 1
    assert any(s["name"] == "Luxury Fashion Hub" for s in stores)

@pytest.mark.asyncio
async def test_trigger_manual_inspection(client, monkeypatch):
    """Tests triggering an on-demand inspection with mocked crawler responses."""
    headers = {"X-API-Key": settings.API_KEY.get_secret_value()}
    
    # 1. Register a valid target store
    payload = {
        "name": "Apparel Brand Store",
        "url": "https://example.com",
        "manager_email": "ops@example.com"
    }
    store_res = await client.post("/api/v1/stores", json=payload, headers=headers)
    store_id = store_res.json()["id"]

    # 2. Mock external HTTP inspector service
    mock_audit_result = {
        "is_up": True,
        "status_code": 200,
        "response_time_ms": 142.50,
        "total_links_scanned": 15,
        "broken_links": [
            {
                "url": "https://example.com/collections/sold-out-dress",
                "status_code": 404,
                "source_page": "https://example.com"
            }
        ]
    }

    async def mock_inspect(*args, **kwargs):
        return mock_audit_result

    monkeypatch.setattr(
        "app.api.v1.endpoints.inspector_service.inspect_storefront",
        mock_inspect
    )

    # 3. Trigger manual inspect endpoint
    inspect_res = await client.post(f"/api/v1/stores/{store_id}/inspect", headers=headers)
    assert inspect_res.status_code == 200
    report = inspect_res.json()

    assert report["store_id"] == store_id
    assert report["is_up"] is True
    assert report["status_code"] == 200
    assert report["broken_links_found"] == 1
    assert report["total_links_scanned"] == 15
    assert len(report["broken_links_details"]) == 1
    assert report["broken_links_details"][0]["status_code"] == 404
