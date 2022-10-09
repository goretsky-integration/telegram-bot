import contextlib
import datetime
import pathlib

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel, parse_obj_as


class WriteOff(BaseModel):
    to_be_write_off_at: datetime.datetime
    written_off_at: datetime.datetime | None
    ingredient_name: str


class UnitWriteOffs(BaseModel):
    unit_id: int
    unit_name: str
    data: list[WriteOff]


def get_write_offs_by_period(*args, **kwargs):
    data = [
        {
            'unit_id': 389,
            'unit_name': 'Москва 4-1',
            'data': [
                {
                    'to_be_write_off_at': '2022-10-03T00:00:00',
                    'written_off_at': None,
                    'ingredient_name': 'Тесто 35'
                }
            ]
        }
    ]
    return parse_obj_as(list[UnitWriteOffs], data)


def generate_write_offs_excel_report(file_path: str | pathlib.Path, units_write_offs: list[UnitWriteOffs]) -> None:
    workbook = openpyxl.Workbook(write_only=True)
    with contextlib.closing(workbook):
        for unit_write_offs in units_write_offs:
            worksheet: Worksheet = workbook.create_sheet(unit_write_offs.unit_name)
            if not unit_write_offs.data:
                worksheet.append(('Нету данных',))
            worksheet.append(('Ингредиент', 'Списание', 'Списано в'))
            for write_off in unit_write_offs.data:
                worksheet.append((write_off.ingredient_name, write_off.to_be_write_off_at, write_off.written_off_at))
        workbook.save(file_path)
