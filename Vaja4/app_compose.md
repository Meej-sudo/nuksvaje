# Docker Compose Aplikacije

Naša aplikacija ima trenutno samo en container, to je naš python app. Docker compose ima sledečo strukturo.
```yaml
version: "3.9"

services:
 api:
    build:
      context: .
    container_name: fastapi_api
    ports:
      - "8000:8000"
 ```
  
