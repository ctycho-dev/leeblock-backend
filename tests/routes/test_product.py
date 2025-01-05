import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.main import app  # Adjust import path to your app
from app.dependencies.factory import DependencyFactory

client = TestClient(app)


# Mock DependencyFactory
@pytest.fixture
def mock_factory(mocker):
    factory = MagicMock(spec=DependencyFactory)
    factory.cache.get = AsyncMock(return_value=None)
    factory.cache.set = AsyncMock()
    factory.db = MagicMock()
    return factory


# Test: GET /products
@pytest.mark.asyncio
async def test_get_products(mock_factory, mocker):
    mock_repo = MagicMock()
    mock_repo.get_all_published = AsyncMock(return_value=[{
        "id": 1,
        "name": "Test Product",
        "description": "Description",
        "sequence": 1,
        "published": True
    }])

    # Mock Dependency Injection
    mock_factory.db = mock_repo
    mocker.patch("app.dependencies.injection.get_factory", return_value=mock_factory)

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == "Test Product"


# Test: GET /products/to_display
@pytest.mark.asyncio
async def test_get_products_to_display(mock_factory, mocker):
    mock_repo = MagicMock()
    mock_repo.get_to_display = AsyncMock(return_value=[{
        "id": 1,
        "name": "Display Product",
        "description": "Display Description",
        "sequence": 1,
        "published": True
    }])

    # Mock Dependency Injection
    mock_factory.db = mock_repo
    mocker.patch("app.dependencies.injection.get_factory", return_value=mock_factory)

    response = client.get("/products/to_display")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == "Display Product"


# Test: GET /products/{product_id}
@pytest.mark.asyncio
async def test_get_product_by_id(mock_factory, mocker):
    mock_repo = MagicMock()
    mock_repo.get_by_id = AsyncMock(return_value={
        "id": 1,
        "name": "Specific Product",
        "description": "Specific Description",
        "sequence": 1,
        "published": True
    })

    # Mock Dependency Injection
    mock_factory.db = mock_repo
    mocker.patch("app.dependencies.injection.get_factory", return_value=mock_factory)

    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()['name'] == "Specific Product"


# Test: Cache works
@pytest.mark.asyncio
async def test_cache(mock_factory, mocker):
    mock_factory.cache.get = AsyncMock(return_value='[{"id":1,"name":"Cached Product"}]')
    mocker.patch("app.dependencies.injection.get_factory", return_value=mock_factory)

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == "Cached Product"
