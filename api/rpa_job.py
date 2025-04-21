from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.rpa import JobRecordsOut_Pydantic, JobRecordsIn_Pydantic
from models.rpa import JobRecords
from typing import Optional, List


router = APIRouter()


@router.get("/rpa_job/", response_model=List[JobRecordsOut_Pydantic])
async def get_rpa_jobs(
    app_name: Optional[str] = Query(None),
    result_status: Optional[str] = Query(None),
):
    query = JobRecords.all()
    if app_name:
        query = query.filter(app_name=app_name)
    if result_status:
        query = query.filter(result_status=result_status)
    job_objs = await JobRecordsOut_Pydantic.from_queryset(query)

    if not job_objs:
        raise HTTPException(status_code=404, detail="未找到符合条件的任务记录")

    return job_objs