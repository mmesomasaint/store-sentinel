# app/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import validate_url_against_ssrf
from app.models.store import StoreModel, AuditLogModel
from app.services.inspector_service import inspector_service
from app.services.alert_service import alert_service

scheduler = AsyncIOScheduler()

async def run_scheduled_store_inspections():
    """Background task executing store crawls and alert routines."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(StoreModel).filter(StoreModel.is_active == True))
        stores = result.scalars().all()

        for store in stores:
            if not validate_url_against_ssrf(store.url):
                continue

            audit_res = await inspector_service.inspect_storefront(store.url)

            # Persist Audit Record
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

            # Trigger alert if store is down or has broken links
            if not audit_res["is_up"] or audit_res["broken_links"]:
                await alert_service.send_downtime_alert(
                    store.manager_email,
                    store.name,
                    audit_res
                )
