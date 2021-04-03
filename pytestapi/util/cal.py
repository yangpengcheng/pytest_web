def cal_offset(page: int, per_page: int):
    return (page - 1) * per_page if page > 0 and per_page >0 else 0

