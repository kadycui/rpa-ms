import pymysql
import uuid
import random
from datetime import datetime, timedelta

# 数据库连接配置
DB_CONFIG = {
    "host": "172.19.188.206",
    "user": "root",
    "password": "123456",
    "database": "fd_plateform",
    "port": 3306,
    "charset": "utf8mb4"
}

# 状态枚举
RESULT_STATUSES = ["成功", "失败", "运行中", "超时"]

# 构造模拟数据
def generate_fake_job(i):
    now = datetime.now()
    start_time = now - timedelta(minutes=random.randint(10, 300))
    if random.random() > 0.1:
        end_time = start_time + timedelta(minutes=random.randint(1, 120))
    else:
        end_time = None
    result_status = random.choice(RESULT_STATUSES)
    result_detail = f"{result_status}：任务执行情况描述。"
    return (
        str(uuid.uuid4()),  # app_uuid
        f"测试应用{i}",       # app_name
        start_time.strftime('%Y-%m-%d %H:%M:%S'),  # start_time
        end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else None,  # end_time
        result_status,
        result_detail,
        now.strftime('%Y-%m-%d %H:%M:%S'),  # created_at
        now.strftime('%Y-%m-%d %H:%M:%S'),  # updated_at
    )

# 插入数据
def insert_jobs():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO rpa_job_records (
                    app_uuid, app_name, start_time, end_time,
                    result_status, result_detail, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = [generate_fake_job(i) for i in range(1, 101)]
            cursor.executemany(sql, data)
        connection.commit()
        print("✅ 成功插入 100 条数据到 rpa_job_records 表")
    finally:
        connection.close()

if __name__ == "__main__":
    insert_jobs()
