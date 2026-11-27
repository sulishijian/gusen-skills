---
name: wms-bill-query
description: 通过 guthon-develop MCP 的 wms.queryBills 查询 GME 仓储单据。支持只给单号跨类型查找、按类型和日期分页，以及发现当前用户可见的单据类型。
---

# 仓储单据统一查询

使用已授权的 `guthon-develop` MCP 工具 `wms.queryBills`。单据类型由 GME 的 `GD_BILL_TYPE` 和原生 WMS 查看入口实时解析，结果受当前用户和操作机构权限约束。

## 选择模式

| 用户需要 | 调用方式 |
| --- | --- |
| 只知道单号 | 用 `FIND`，传完整 `billCode`。已有明确类型时，可加 `billType` 缩小范围。 |
| 查某类单据的一段日期 | 用 `LIST`，传 `billType`、`startDate`、`endDate`。日期使用 `yyyy-MM-dd`，包含首尾两天。 |
| 不知道类型编码，或想查支持范围 | 用 `CATALOG`。可传 `billType` 作名称关键词，使用目录中的编码查询。 |

例如，单号查询参数如下：

```json
{"mode":"FIND","billCode":"<完整单号>"}
```

列表查询使用返回的类型编码或准确名称。例如：

```json
{"mode":"LIST","billType":"入库单","startDate":"2026-11-01","endDate":"2026-11-30","pageNo":"1","pageSize":"20"}
```

目录查询可按名称缩小范围。例如：

```json
{"mode":"CATALOG","billType":"集装箱","pageNo":"1","pageSize":"20"}
```

## 读取结果

- 从 `items` 读取单号、类型、日期、机构、仓库和业务状态。缺省字段按工具返回处理。相同单号命中多种类型时，列出各个匹配项，由用户选择。出现 `AMBIGUOUS_TYPE` 时读取 `candidates`，确认类型后用其编码重查。
- `DATE_BASIS=BILL_DATE` 表示按业务日期，`SYSTEM_DATE` 表示按该类型登记的建单或系统日期。结果里注明日期口径。
- 使用 `pagination.totalCount` 和 `pagination.hasMore` 判断范围。用户需要后续结果时，保留原筛选条件递增 `pageNo`。每页 1 至 100 条，默认 20 条。
- `PARTIAL` 表示工具只查询了部分类型。用 `coverage.unavailableTypes` 说明本次查不了的类型。若 `coverage.withoutActiveEntry` 大于 0，说明还有登记类型未关联启用的 WMS 查看入口。查无结果仅表示本次权限和覆盖范围内未命中。
- 遇到 `TYPE_NOT_VISIBLE` 或 `QUERY_NOT_AVAILABLE` 时，按返回的类型和状态核对权限、入口和业务日期配置。目录中 `searchByCode=true` 的类型可按单号查找。
