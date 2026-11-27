---
name: wms-bill-query
description: 通过当前连接的 guthon-develop MCP 查询仓储单据，支持按完整单号跨类型查找、按类型和日期分页，以及查询当前项目可见的单据类型。
---

# 仓储单据统一查询

## 确认 MCP 和项目

- 从当前已连接的 `guthon-develop` MCP 工具列表中查找 `wms.queryBills`，按该连接实际公布的参数和返回结构调用。查询范围由该连接指向的项目、登录用户和操作机构决定。
- 用户指定项目时，通过连接名称、地址或 MCP 提供的项目信息核对目标。存在多个候选连接且无法确认目标时，先请用户指定连接。当前连接唯一且用户未指定项目时，使用该连接。
- 当前连接未公布 `wms.queryBills` 时，说明该项目的 MCP 暂未提供统一查询，请用户切换到具备该工具的目标连接或联系项目管理员启用。项目切换以用户选择为准。
- 单据类型从当前连接的目录实时获取。换项目或连接后重新查目录，避免沿用其他项目的类型编码。

## 选择模式

以下示例适用于当前连接公布的 `wms.queryBills` 支持 `FIND`、`LIST` 和 `CATALOG` 的情况。参数或模式有差异时，以实际工具定义为准。

| 用户需要 | 调用方式 |
| --- | --- |
| 只知道单号 | 用 `FIND`，传完整 `billCode`。已有明确类型时，可加 `billType` 缩小范围。 |
| 查某类单据的一段日期 | 用 `LIST`，传 `billType`、`startDate`、`endDate`。日期使用 `yyyy-MM-dd`，包含首尾两天。 |
| 不知道类型编码，或想查支持范围 | 用 `CATALOG`。可传 `billType` 作名称关键词，使用目录中的编码查询。 |

单号查询示例

```json
{"mode":"FIND","billCode":"<完整单号>"}
```

列表查询示例。类型用当前项目目录返回的编码或准确名称。

```json
{"mode":"LIST","billType":"<当前项目的类型编码>","startDate":"2026-11-01","endDate":"2026-11-30","pageNo":"1","pageSize":"20"}
```

目录查询示例

```json
{"mode":"CATALOG","billType":"集装箱","pageNo":"1","pageSize":"20"}
```

## 读取结果

- 从工具返回的 `items` 读取单号、类型、日期、机构、仓库和业务状态。相同单号命中多种类型时，列出匹配项，由用户选择。返回 `AMBIGUOUS_TYPE` 时，读取 `candidates`，确认类型后用其编码重查。
- 返回 `DATE_BASIS=BILL_DATE` 时注明按业务日期，返回 `SYSTEM_DATE` 时注明按建单或系统日期。
- 工具返回 `pagination` 时，用 `totalCount` 和 `hasMore` 判断范围。用户需要下一页时，保留原筛选条件并递增 `pageNo`。分页上限和默认值以当前工具定义为准。
- 返回 `PARTIAL` 时，根据 `coverage.unavailableTypes` 说明未覆盖的类型。若 `coverage.withoutActiveEntry` 大于 0，说明存在未关联启用查看入口的登记类型。查无结果仅表示本次连接、权限和覆盖范围内未命中。
- 返回 `TYPE_NOT_VISIBLE` 或 `QUERY_NOT_AVAILABLE` 时，按返回的类型和状态说明受限原因。目录返回 `searchByCode=true` 时，表示该类型可按单号查找。
