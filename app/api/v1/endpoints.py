# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import verify_api_key, validate_url_against_ssrf
from app.models.store import StoreModel, AuditLogModel
from app.schemas.store import StoreCreate, StoreResponse, AuditReportResponse
from app.services.inspector_service import inspector_service

router = APIRouter()

@router.post("", response_model=StoreResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def register_store(payload: StoreCreate, db: AsyncSession = Depends(get_db)):
    url_str = str(payload.url)
    if not validate_url_against_ssrf(url_str):
        raise HTTPException(status_code=400, detail="Invalid target URL or internal IP restricted.")

    store = StoreModel(
        name=payload.name,
        url=url_str,
        manager_email=payload.manager_email
    )
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store

@router.get("", response_model=List[StoreResponse], dependencies=[Depends(verify_api_key)])
async def list_monitored_stores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreModel))
    return result.scalars().all()

@router.post("/{store_id}/inspect", response_model=AuditReportResponse, dependencies=[Depends(verify_api_key)])
async def trigger_manual_inspection(store_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreModel).filter(StoreModel.id == store_id))
    store = result.scalars().first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found.")

    audit_res = await inspector_service.inspect_storefront(store.url)
    
    audit = AuditLogModel(
        store_id=store.id,
        status_code=audit_res["status_code"],
        response_time_ms=audit_res["response_time_ms"],
        is_up=audit_res["is_up"],
        total_links_scanned=audit_res["total_links_scanned"],
        broken_links_found=len(audit_res["broken_links"]),
        broken_links_details=audit_res["broken_links"]
    )
    db.add(audit)
    await db.commit()
    await db.refresh(audit)
    return audit
