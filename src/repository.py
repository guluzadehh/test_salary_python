from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

from helpers import create_group_key
from schemas import InputSchema


load_dotenv()


class SalaryRepository:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(
            os.getenv("CONNECTION_STRING"), server_api=ServerApi("1")
        )
        self.db = self.client["sampleDB"]

    async def group_total_salaries_by(self, options: InputSchema):
        group_key = create_group_key(options.group_type)

        pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": options.dt_from,
                        "$lte": options.dt_upto,
                    }
                },
            },
            {
                "$group": {
                    "_id": group_key,
                    "totalSalary": {"$sum": "$value"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "dt": {
                        "$dateFromParts": {
                            "year": "$_id.year",
                            "month": "$_id.month",
                            "day": {"$ifNull": ["$_id.day", 1]},
                            "hour": {"$ifNull": ["$_id.hour", 0]},
                        }
                    },
                    "totalSalary": {"$ifNull": ["$totalSalary", 0]},
                }
            },
            {"$sort": {"dt": 1}},
        ]

        return await self.db["sample_collection"].aggregate(pipeline).to_list(None)
