from pydantic import BaseModel, HttpUrl

class ShortKey(BaseModel):
    value: str

    def __str__(self):
        return self.value

    # 지정 파라미터 아닌 위치 파라미터 사용
    class Config:
        frozen = True


class OriginalURL(BaseModel):
    value: HttpUrl

    def __str__(self):
        return str(self.value)

    class Config:
        frozen = True
