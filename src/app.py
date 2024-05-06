from datetime import datetime
from typing import List
from helpers import increment_date
from schemas import InputSchema, OutputSchema
from repository import SalaryRepository


class App:
    async def run(self, request: InputSchema) -> OutputSchema:
        repository = SalaryRepository()
        data = iter(await repository.group_total_salaries_by(request))

        dataset: List[int] = []
        labels: List[str] = []

        dt_from: datetime = request.dt_from
        dt_upto: datetime = request.dt_upto
        cur = next(data)

        while dt_from <= dt_upto:
            if cur is not None and dt_from == cur["dt"]:
                dataset.append(cur["totalSalary"])
                labels.append(cur["dt"].isoformat())
                try:
                    cur = next(data)
                except:
                    cur = None
            else:
                dataset.append(0)
                labels.append(dt_from.isoformat())

            dt_from = increment_date(dt_from, request.group_type)

        return OutputSchema.model_validate({"dataset": dataset, "labels": labels})
