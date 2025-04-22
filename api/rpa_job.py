from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.rpa import JobRecordsOut_Pydantic, JobRecordsIn_Pydantic
from models.rpa import JobRecords
from typing import Optional, List


router = APIRouter()


@router.get("/rpa_job/", response_model=List[JobRecordsOut_Pydantic], summary="获取RPA任务记录")
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


class ResponseJobId_Pydantic(JobRecordsOut_Pydantic):
    id: int


@router.post("/rpa_job/", summary="创建RPA任务记录")
async def create_rpa_job(job: JobRecordsIn_Pydantic): # type: ignore
    job_obj = await JobRecords.create(**job.dict())
    return {"id": job_obj.id}