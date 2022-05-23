import logging
import datetime
from openpyxl.workbook import Workbook
from openpyxl import load_workbook

from loader import db


class Excel:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.file_name = f'files/{chat_id}.xlsx'

    async def fill_with_messages(self, start_date: datetime = None, end_date: datetime = None):
        try:
            wb = load_workbook(self.file_name)
        except FileNotFoundError as err:
            logging.info(f'{err}. Excel file created for {self.chat_id} at {datetime.datetime.now()}')
            wb = Workbook()
        ws = wb.active
        ws['A1'] = 'Vaqti'
        ws['B1'] = 'Metr kub/soat'
        # messages = await db.
        print(ws['A2'].value)
        wb.save(self.file_name)
