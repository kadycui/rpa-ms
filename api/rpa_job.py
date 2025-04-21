from fastapi import APIRouter, Depends, HTTPException, Query


router = APIRouter()


@router.get("/rpa_job")
async def get_rpa_job(
    job_id: int = Query(..., description="Job ID", example=1),
    status: str = Query(..., description="Job Status", example="running"),
    limit: int = Query(10, description="Limit", example=10),
    offset: int = Query(0, description="Offset", example=0)
):
    """
    Get RPA Job
    """
    # Dummy data for demonstration
    dummy_data = {
        "job_id": job_id,
        "status": status,
        "limit": limit,
        "offset": offset
    }
    
    return dummy_data