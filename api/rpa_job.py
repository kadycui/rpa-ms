from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.rpa import JobRecordsOut_Pydantic, JobRecordsIn_Pydantic
from schemas.response import ResponseBase, ResponseList, ResponseId
from models.rpa import JobRecords
from typing import Optional, List


router = APIRouter()


@router.get("/rpa_job/", response_model=ResponseList[JobRecordsOut_Pydantic], summary="获取RPA任务记录")
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
    total = len(job_objs) if job_objs else 0

    if not job_objs:
        return ResponseList[JobRecordsOut_Pydantic](
            code=404,
            message="未找到符合条件的任务记录",
            data=[],
            total=0
        )

    return ResponseList[JobRecordsOut_Pydantic](
        data=job_objs,
        total=total
    )


@router.post("/rpa_job/", response_model=ResponseId, summary="创建RPA任务记录")
async def create_rpa_job(job: JobRecordsIn_Pydantic):
    job_obj = await JobRecords.create(**job.dict())
    return ResponseId(id=job_obj.id)


@router.put("/rpa_job/{job_id}", response_model=ResponseBase[JobRecordsOut_Pydantic], summary="修改RPA任务记录")
async def update_rpa_job(job_id: int, job: JobRecordsIn_Pydantic):
    # 检查任务是否存在
    job_obj = await JobRecords.get_or_none(id=job_id)
    if not job_obj:
        return ResponseBase[JobRecordsOut_Pydantic](
            code=404,
            message="任务记录不存在",
            data=None
        )
    
    # 更新任务记录
    await job_obj.update_from_dict(job.dict(exclude_unset=True))
    await job_obj.save()
    
    # 返回更新后的任务记录
    updated_job = await JobRecordsOut_Pydantic.from_tortoise_orm(job_obj)
    return ResponseBase[JobRecordsOut_Pydantic](data=updated_job)


@router.delete("/rpa_job/{job_id}", response_model=ResponseBase[None], summary="删除RPA任务记录")
async def delete_rpa_job(job_id: int):
    # 检查任务是否存在
    job_obj = await JobRecords.get_or_none(id=job_id)
    if not job_obj:
        return ResponseBase[None](
            code=404,
            message="任务记录不存在"
        )
    
    # 删除任务记录
    await job_obj.delete()
    
    return ResponseBase[None](message="任务记录已成功删除")