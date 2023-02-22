import typing as t
from dataclasses import dataclass
from math import ceil

from piccolo.table import Table
from starlite import Request


@dataclass
class Pagination:
    page: t.Optional[int] = None
    page_size: t.Optional[int] = None

    async def get_rows(self, table: t.Type[Table], request: Request):
        if self.page_size is None or self.page is None:
            query = (
                table.select(table.all_columns(), table.get_readable())
                .limit(2)
                .order_by(table._meta.primary_key, ascending=False)
            )
        else:
            if self.page < 1:
                self.page = 1
            offset = self.page_size * (self.page - 1)
            query = (
                table.select(table.all_columns(), table.get_readable())
                .offset(offset)
                .limit(self.page_size)
                .order_by(table._meta.primary_key, ascending=False)
            )
        return await query.run()

    async def total_pages(self, table: t.Type[Table]) -> int:
        count = await table.count()
        if self.page_size is None:
            self.page_size = 1
        return max(ceil(count / self.page_size), 1)
