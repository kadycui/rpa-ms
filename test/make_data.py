import asyncio
import aiomysql
import uuid
import random
from datetime import datetime, timedelta


DB_CONFIG = {
    "host": "172.18.67.16",
    "user": "root",
    "password": "123456",
    "db": "rpadb",  
    "port": 3306,
    "charset": "utf8mb4"
}


RESULT_STATUSES = ["成功", "失败", "运行中", "超时"]


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
        str(uuid.uuid4()),  
        f"测试应用{i}",      
        start_time,        
        end_time,         
        result_status,
        result_detail,
        now,              
        now,              
    )


async def insert_jobs():
    pool = await aiomysql.create_pool(**DB_CONFIG)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = """
                    INSERT INTO rpa_job_records (
                        app_uuid, app_name, start_time, end_time,
                        result_status, result_detail, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = [generate_fake_job(i) for i in range(1, 101)]
                await cursor.executemany(sql, data)
                await conn.commit()
                print("成功插入 100 条数据到 rpa_job_records 表")
    finally:
        pool.close()
        await pool.wait_closed()

async def main():
    await insert_jobs()

if __name__ == "__main__":
    asyncio.run(main())
