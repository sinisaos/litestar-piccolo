import typing as t
from dataclasses import dataclass
from math import ceil

from litestar import Request
from piccolo.table import Table


@dataclass
class Pagination:
    page: t.Optional[int] = None
    page_size: t.Optional[int] = None

    async def get_rows(
        self, table: t.Type[Table], request: Request
    ) -> t.List[t.Dict[str, t.Any]]:
        all_columns: t.Any = table.all_columns()

        if self.page_size is None or self.page is None:
            query = (
                table.select(all_columns, table.get_readable())
                .limit(15)
                .order_by(table._meta.primary_key, ascending=False)
            )
        else:
            if self.page < 1:
                self.page = 1
            offset = self.page_size * (self.page - 1)
            query = (
                table.select(all_columns, table.get_readable())
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
