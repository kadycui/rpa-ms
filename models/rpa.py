from tortoise import fields
from tortoise.models import Model
from enum import Enum


class ResultStatusEnum(str, Enum):
    success = "成功"
    failed = "失败"
    pending = "运行中"
    timeout = "超时"


class JobRecords(Model):
    id = fields.IntField(pk=True, description="自增主键")
    app_uuid = fields.CharField(max_length=36, description="应用唯一标识 (UUID)", index=True)
    app_name = fields.CharField(max_length=255, description="应用名称")
    start_date = fields.DatetimeField(auto_now_add=True, description="开始时间", index=True)
    end_date = fields.DatetimeField(null=True, description="结束时间")
    result_status = fields.CharEnumField(
        enum_type=ResultStatusEnum,
        default=ResultStatusEnum.pending,
        description="执行状态"
    )
    result_detail = fields.TextField(null=True, description="执行结果详情")
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="最后更新时间")

    class Meta:
        table = "rpa_job_records"
        table_description = "RPA任务记录表"
