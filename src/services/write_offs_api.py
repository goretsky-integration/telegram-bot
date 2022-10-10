import collections
import contextlib
import datetime
import pathlib
from typing import Iterable

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel, parse_obj_as

from utils import logger


class WriteOff(BaseModel):
    to_be_write_off_at: datetime.datetime
    written_off_at: datetime.datetime | None
    ingredient_name: str
    unit_id: int


def group_write_offs_by_unit(write_offs: Iterable[WriteOff]) -> dict[int, list[WriteOff]]:
    unit_id_to_write_offs = collections.defaultdict(list)
    for write_off in write_offs:
        write_offs_by_unit_id = unit_id_to_write_offs[write_off.unit_id]
        write_offs_by_unit_id.append(write_off)
    return unit_id_to_write_offs


def get_write_offs_by_period(*args, **kwargs) -> list[WriteOff]:
    data = [
        {
            "id": 389,
            "unit_id": 389,
            "ingredient_name": "Тесто 35",
            "to_be_write_off_at": "2022-11-10T14:00:09",
            "written_off_at": "2022-10-10T15:00:09"
        },
        {
            "id": 389,
            "unit_id": 389,
            "ingredient_name": "Тесто 35",
            "to_be_write_off_at": "2022-11-10T12:00:09",
            "written_off_at": "2022-10-10T15:00:02"
        },
        {
            "id": 389,
            "unit_id": 342,
            "ingredient_name": "Тесто 35",
            "to_be_write_off_at": "2022-11-10T14:00:09",
            "written_off_at": "2022-10-10T15:00:09"
        },
    ]
    return parse_obj_as(list[WriteOff], data)


def generate_write_offs_excel_report(file_path: str | pathlib.Path,
                                     unit_id_to_name: dict[int, str],
                                     write_offs_grouped_by_unit_id: dict[int, list[WriteOff]]) -> None:
    workbook = openpyxl.Workbook(write_only=True)

    with contextlib.closing(workbook):
        for unit_id, write_offs in write_offs_grouped_by_unit_id.items():
            unit_name = unit_id_to_name.get(unit_id, str(unit_id))

            worksheet: Worksheet = workbook.create_sheet(unit_name)
            for column in ('A', 'B', 'C'):
                worksheet.column_dimensions[column].width = 20
            worksheet.append(('Ингредиент', 'Списание', 'Списано в'))

            write_offs = sorted(write_offs, key=lambda write_off: write_off.to_be_write_off_at)
            for write_off in write_offs:
                row = (write_off.ingredient_name, write_off.to_be_write_off_at, write_off.written_off_at)
                worksheet.append(row)

        workbook.save(file_path)
        logger.debug('Excel report saved')
