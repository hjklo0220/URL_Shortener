## 개요
---

- URL 단축 서비스는 긴 URL을 짧게 단축하여 사용하고, 단축된 URL을 통해 원본 URL로 리디렉션하는 기능을 제공합니다.

- 사용 기술 스택
  - Framework: FastAPI
  - DB: PostgreSQL

- 사용 이유
  - 프로젝트가 확장됨을 고려하여 대규모 데이터에 적합한 PostgreSQL을 선택하였습니다.
  - URL 단축 서비스에서 원본 URL과 단축 키 간의 정확한 매핑이 중요하다고 생각합니다. RDB의 ACID 준수 특성은 이러한 데이터 무결성을 보장하기 때문에 선택하였습니다.

<br>

## API
---

**단축 URL 생성**

- POST `/shorten`
  -  입력받은 긴 URL을 고유한 단축 키로 변환하고 데이터베이스에 저장.

<br>

- 요청 본문 예시: 
    ```json
    {
    "url": "https://www.naver.com/",
    "expires_at": "2024-08-13T13:45:33.311Z"
    }
    ```

- 응답 본문 예시: 
    ```json
    {
    "short_url": "http://localhost:8000/6fOjfrz"
    }
    ```

- 단축 기능
  - uuid를 사용하여 중복을 최소화
  - base62로 인코딩하여 7자로 단축

    ```python
    class Base62Shortener(ShortenerService):
        def __init__(self, length: int = 7):
            self.length = length

        def generate_short_key(self) -> ShortKey:
            # UUID를 생성하고 Base62로 인코딩
            uuid_int = uuid.uuid4().int
            encoded = base62.encodebytes(uuid_int.to_bytes(16, 'big'))

            return ShortKey(value=encoded[:self.length])
    ```
<br>

**원본 URL 리디렉션**

- GET `/<short_key>`
  - 단축된 키를 통해 원본 URL로 리디렉션.

- 리디렉션 기능:
  - 키가 존재하면 301 상태 코드로 원본 URL로 리디렉션
  - 키가 존재하지 않으면 404 상태 코드로 오류 메시지 반환

    ```python
    @router.get("/{short_key}")
    def redirect_to_original_url(
        short_key: str,
        service: URLService = Depends(get_url_service)
    ):
        original_url = service.get_original_url(short_key)
        if original_url is None:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(url=original_url, status_code=301)
    ```

**단축URL 통계**

- GET `stats/<short_key>`
  - 단축된 키를 통해 원본 URL로 리디렉션.

- 응답 예시:

    ```json
    {
    "original_url": "https://www.naver.com/",
    "short_key": "6fOjfrz",
    "created_at": "2024-08-12T13:45:49.274473",
    "expires_at": "2024-08-13T13:45:33.311000",
    "views": 1
    }
    ```
- 조회수 통계 기능
  - short_key를 통해 원본 URL 리디렉션 요청을 하면 조회수 증가

    ```python
    def get_original_url(self, short_key: str) -> Optional[str]:
            url: URL = self.repository.get_by_short_key(ShortKey(value=short_key))
            if url and not url.is_expired():
                url.increment_views()
                self.repository.update(url)
                return str(url.original_url)

            return None
    ```


<br><br>

## 설치 및 실행방법
---

1. docker 및 docker-compose 설치
- [Docker 공식 웹사이트](https://docs.docker.com/get-docker/)에서 운영 체제에 맞는 Docker Desktop을 다운로드하고 설치합니다.

2. git clone

    ```sh
    git clone https://github.com/hjklo0220/URL_Shortener.git
    cd URL_Shortener 
    ```

3. docker-compose 실행 명령어

    ```sh
    docker-compose up --build -d
    ```

4. 브라우저에서 http://localhost:8000/docs 접속