import os
import json
from typing import List
from fastapi import HTTPException, Depends, APIRouter

from app.schemas.product import ProductResponse
from app.schemas.product import ProductResponse
from app.repositories.product_repository import ProductRepository
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.dependencies.injection import get_factory


CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
logger = get_logger()

router = APIRouter(
    prefix='/products',
    tags=['Products']
)


@router.get('/', response_model=List[ProductResponse])
async def get_products(
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Fetch all published products, ordered by sequence.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[ProductResponse]: A list of all published products.

    Raises:
        HTTPException: If no products are found.
    """
    try:
        cache_key = 'products'

        cached_products = await factory.cache.get(cache_key)
        if cached_products:
            return json.loads(cached_products)

        product_repo = ProductRepository(factory.db)
        products = await product_repo.get_all_published()

        product_list = [
            ProductResponse.model_validate(product).model_dump()
            for product in products
        ]

        await factory.cache.set(cache_key, json.dumps(product_list), ex=CACHE_TTL)

        return product_list
    except Exception as exc:
        logger.error('/v1/get_products %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc


@router.get('/to_display')
async def get_products_to_display(
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Fetch all published products, ordered by sequence.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[ProductResponse]: A list of all published products.

    Raises:
        HTTPException: If no products are found.
    """
    try:
        cache_key = 'to_display'

        cached_products = await factory.cache.get(cache_key)
        if cached_products:
            return json.loads(cached_products)

        product_repo = ProductRepository(factory.db)
        products = await product_repo.get_to_display()

        product_list = [
            ProductResponse.model_validate(product).model_dump()
            for product in products
        ]

        await factory.cache.set(cache_key, json.dumps(product_list), ex=CACHE_TTL)

        return product_list
    except Exception as exc:
        logger.error('/v1/get_products %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc


@router.get('/{product_id}')
async def get_product_by_id(
    product_id: int,
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Fetch all published products, ordered by sequence.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[ProductResponse]: A list of all published products.

    Raises:
        HTTPException: If no products are found.
    """
    try:
        cache_key = f'product:{product_id}'

        cached_products = await factory.cache.get(cache_key)
        if cached_products:
            return json.loads(cached_products)

        product_repo = ProductRepository(factory.db)
        product = await product_repo.get_by_id(product_id)

        if not product:
            return None

        product_json = ProductResponse.model_validate(product).model_dump()

        await factory.cache.set(cache_key, json.dumps(product_json), ex=CACHE_TTL)

        return product_json
    except Exception as exc:
        logger.error('/v1/get_products %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc



# @router.get('/v1/get_products/{product_id}', response_model=ProductResponse)
# async def get_product_by_id(
#     product_id: str,
#     db: Session = Depends(get_db),
#     rc: Session = Depends(get_redis_client)
# ):
#     """
#     Fetch a product by its ID.

#     Args:
#         product_id (str): The ID of the product to retrieve.
#         db (Session): The database session dependency.

#     Returns:
#         ProductResponse: Details of the requested product.

#     Raises:
#         HTTPException: If the product is not found.
#     """
#     try:
#         cached_product = rc.get(product_id)
#         if cached_product:
#             return json.loads(cached_product)

#         product = db.query(Products).filter(Products.product_id == product_id).first()

#         if not product:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Product with ID '{product_id}' not found."
#             )

#         product_json = ProductResponse.model_validate(product).model_dump()

#         rc.set(product_id, json.dumps(product_json), ex=3600)
#         return product_json
#     except Exception as exc:
#         logger.error('/v1/get_products/product_id %s', exc)
#         raise HTTPException(
#             status_code=500,
#             detail=exc
#         ) from exc



# @router.get('/v1/get_products_to_display', response_model=list[ProductResponse])
# async def get_products_to_display(
#     db: Session = Depends(get_db),
#     rc: Session = Depends(get_redis_client)
# ):
#     """
#     Fetch all products marked for display on the main page.

#     Args:
#         db (Session): The database session dependency.

#     Returns:
#         List[ProductResponse]: A list of products to display on the main page.

#     Raises:
#         HTTPException: If no products are found for display.
#     """
#     try:
#         cached_products = rc.get('products_to_display')
#         if cached_products:
#             return json.loads(cached_products)
        
#         products = db.query(Products).filter(Products.display_on_main == 1).all()

#         if not products:
#             raise HTTPException(
#                 status_code=404,
#                 detail="No products to display on the main page."
#             )

#         product_list = [ProductResponse.model_validate(product).model_dump() for product in products]
#         rc.set('products_to_display', json.dumps(product_list), ex=3600)
#         return product_list
#     except Exception as exc:
#         logger.error('/v1/get_products_to_display %s', exc)
#         raise HTTPException(
#             status_code=500,
#             detail=exc
#         ) from exc
