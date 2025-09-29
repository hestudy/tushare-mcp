# REST API Spec
```yaml
openapi: 3.0.0
info:
  title: tushare MCP Backend API
  version: 0.1.0
  description: 提供 MCP 指令执行与元数据访问能力的统一后端接口。
servers:
  - url: http://localhost:8000
    description: 本地开发环境
  - url: https://mcp.example.com
    description: 预留生产入口（待部署）
paths:
  /mcp/commands:
    get:
      summary: 列出可用 MCP 指令
      operationId: listCommands
      parameters:
        - name: source
          in: query
          schema:
            type: string
        - name: keyword
          in: query
          schema:
            type: string
      responses:
        "200":
          description: 指令列表
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandListResponse"
  /mcp/commands/{commandId}:
    get:
      summary: 获取 MCP 指令详情
      operationId: getCommandDetail
      parameters:
        - name: commandId
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: 指令详情
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandDetailResponse"
        "404":
          $ref: "#/components/responses/CommandNotFound"
  /mcp/execute:
    post:
      summary: 执行 MCP 指令
      operationId: executeCommand
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ExecuteCommandRequest"
      responses:
        "200":
          description: 执行成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ExecuteCommandResponse"
        "400":
          $ref: "#/components/responses/InvalidParameter"
        "401":
          $ref: "#/components/responses/AuthRequired"
        "429":
          $ref: "#/components/responses/RateLimited"
        "500":
          $ref: "#/components/responses/InternalError"
  /auth/token:
    post:
      summary: 设置或更新 tushare Token
      operationId: setToken
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SetTokenRequest"
      responses:
        "204":
          description: Token 已更新
        "400":
          $ref: "#/components/responses/InvalidParameter"
  /metadata/interfaces/{interfaceName}:
    get:
      summary: 查询 tushare 接口元数据
      operationId: getInterfaceMetadata
      parameters:
        - name: interfaceName
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: 元数据详情
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/InterfaceMetadataResponse"
        "404":
          $ref: "#/components/responses/MetadataNotFound"
components:
  securitySchemes:
    MCPToken:
      type: apiKey
      in: header
      name: X-MCP-Token
  schemas:
    CommandSummary:
      type: object
      properties:
        commandId:
          type: string
        title:
          type: string
        source:
          type: string
        description:
          type: string
    CommandListResponse:
      type: object
      properties:
        commands:
          type: array
          items:
            $ref: "#/components/schemas/CommandSummary"
    CommandDetailResponse:
      type: object
      properties:
        commandId:
          type: string
        description:
          type: string
        parameters:
          type: array
          items:
            $ref: "#/components/schemas/CommandParameter"
        rateLimitHint:
          type: string
        lastUpdatedAt:
          type: string
          format: date-time
    CommandParameter:
      type: object
      properties:
        name:
          type: string
        type:
          type: string
        required:
          type: boolean
        default:
          nullable: true
        description:
          type: string
    ExecuteCommandRequest:
      type: object
      required:
        - commandId
        - params
      properties:
        commandId:
          type: string
        params:
          type: object
          additionalProperties: true
        pagination:
          type: object
          properties:
            limit:
              type: integer
            maxPages:
              type: integer
    ExecuteCommandResponse:
      type: object
      properties:
        requestId:
          type: string
        status:
          type: string
          enum: [SUCCESS, PARTIAL, ERROR]
        data:
          type: object
          additionalProperties: true
        pagination:
          type: object
          properties:
            nextOffset:
              type: integer
            completed:
              type: boolean
        metrics:
          type: object
          properties:
            retries:
              type: integer
            durationMs:
              type: integer
            rateLimitHits:
              type: integer
        error:
          $ref: "#/components/schemas/ErrorPayload"
    SetTokenRequest:
      type: object
      required:
        - token
      properties:
        token:
          type: string
        owner:
          type: string
    InterfaceMetadataResponse:
      type: object
      properties:
        interfaceName:
          type: string
        parameters:
          type: array
          items:
            $ref: "#/components/schemas/CommandParameter"
        responseFields:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              type:
                type: string
              description:
                type: string
        throttleHint:
          type: string
    ErrorPayload:
      type: object
      properties:
        code:
          type: string
        category:
          type: string
          enum: [AUTH, PARAMETER, RATE_LIMIT, SERVICE, UNKNOWN]
        message:
          type: string
        remediation:
          type: string
  responses:
    InvalidParameter:
      description: 参数校验失败
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorPayload"
    AuthRequired:
      description: 未配置或解密 Token 失败
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorPayload"
    RateLimited:
      description: 触发限频
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorPayload"
    InternalError:
      description: 服务异常
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorPayload"
    CommandNotFound:
      description: 指令不存在
    MetadataNotFound:
      description: 元数据缺失
security:
  - MCPToken: []
```
