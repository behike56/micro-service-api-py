# open api schema

試し書き用。

## oasの構造

第1情報源: [https://swagger.io/docs/specification/v3_0/about/](What is OpenAPI?)

``` yaml
openapi: 3.0.0
info:
  title: Sample API
  description: Optional multiline or single-line description in [CommonMark](http://commonmark.org/help/) or HTML.
  version: 0.1.9

servers:
  - url: http://api.example.com/v1
    description: Optional server description, e.g. Main (production) server
  - url: http://staging-api.example.com
    description: Optional server description, e.g. Internal staging server for testing

paths:
  /users:
    get:
      summary: Returns a list of users.
      description: Optional extended description in CommonMark or HTML.
      responses:
        "200": # status code
          description: A JSON array of user names
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
```

### Metadata

OpenAPIのバージョン。

``` yaml
openapi: 3.0.0
```

APIのタイトルやバージョンといった一般情報。

``` yaml
info:
  title: Sample API
  description: Optional multiline or single-line description in [CommonMark](http://commonmark.org/help/) or HTML.
  version: 0.1.9
```

### Servers

APIを利用できるURLのリスト。

Server URL format.

`scheme://host[:port][/path]`

テンプレート

``` yaml
servers:
  - url: https://{customerId}.saas-app.com:{port}/v2
    variables:
      customerId:
        default: demo
        description: Customer ID assigned by the service provider
      port:
        enum:
          - '443'
          - '8443'
        default: '443'
```

### Paths

APIが提供するエンドポイントを表す。

``` yaml
paths:
  /users:
    get:
      summary: Returns a list of users.
      description: Optional extended description in CommonMark or HTML.
      responses:
        "200": # status code
          description: A JSON array of user names
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
```

### components

スキーマ、パラメータ、セキュリティスキーム、リクエストボディ、レスポンスなど。
API仕様全体で再利用可能な要素の定義群。
スキーマとはリクエストオブジェクトとレスポンスオブジェクトに置いて期待される属性と、型の定義のこと。
