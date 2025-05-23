from tortoise.contrib.pydantic import pydantic_model_creator
from models.rpa import JobRecords



JobRecordsIn_Pydantic = pydantic_model_creator(
    JobRecords,
    name="JobRecordsIn",
    include=("app_uuid", "app_name", "start_time", "end_time", "result_status", "result_detail"))



JobRecordsOut_Pydantic = pydantic_model_creator(
    JobRecords,
    name="JobRecordsOut",
    include=("id", "app_uuid", "app_name", "start_time", "end_time", "result_status", "result_detail"))
    