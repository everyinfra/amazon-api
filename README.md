# Amazon API

[English](#english) · [中文](#中文)

## English

This repo reads public Amazon data with Python or curl. You can search products by keyword, read product details and customer reviews, and get a category's best sellers list. You need one EveryInfra API key. You do not need an Amazon account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 4 capabilities cost $1.39 to $2.24 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Amazon API has 10 capabilities, all listed on the platform page: <https://everyinfra.com/en/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### Quick start

```bash
git clone https://github.com/everyinfra/amazon-api.git
cd amazon-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "camping tent" --out products.csv
python main.py product "<product url>" --out product.json
python main.py reviews "<product url>" --out reviews.csv
python main.py bestsellers "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods" --out bestsellers.csv
```

- Take the product link from the `url` field of a `search` result, for example https://www.amazon.com/dp/<ASIN>.
- For `bestsellers`, pass the full link of an Amazon best sellers category page (it contains /zgbs/). Open a category on amazon.com/Best-Sellers to get it.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"amazon","action":"search","params":{"keyword":"camping tent"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `profile`, `reviews`, and `bestsellers` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $2.24 |
| `profile` | $1.39 |
| `reviews` | $1.39 |
| `bestsellers` | $1.39 |

- Billing is per call, about $0.0014 to $0.0022 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>
- Prices for the other 6 Amazon capabilities are on the platform page: <https://everyinfra.com/en/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### Fields

These are the fields that the 4 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `asin` | Amazon Standard Identification Number, the product's unique ID within a store. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `url` | Link to the record on the platform. |
| `brand` | Brand. |
| `price` | Price as a number without a currency symbol; see currency. |
| `list_price` | List (strike-through) price. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `rating_count` | Number of people who rated. null means not disclosed, not 0. |
| `in_stock` | Whether the product is in stock. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `image_url` | Image link. |
| `is_amazon_choice` | Whether the product carries the Amazon's Choice badge. |
| `seller_name` | Seller name. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `images` | Array of image links in the platform's display order; absent when there are no images. |
| `features` | Bullet-point feature list from the product page (search, profile), as written; absent when there is none. |
| `bestseller_ranks` | Best Sellers ranks (search, profile): each item has rank and category, one entry per category; the rank at read time, not a sales figure. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |
| `description` | Summary or description, usually shorter than text. |

All parameters and fields: <https://everyinfra.com/en/amazon-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `asin` | Amazon Standard Identification Number, the product's unique ID within a store. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `url` | Link to the record on the platform. |
| `brand` | Brand. |
| `price` | Price as a number without a currency symbol; see currency. |
| `list_price` | List (strike-through) price. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `rating_count` | Number of people who rated. null means not disclosed, not 0. |
| `in_stock` | Whether the product is in stock. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `image_url` | Image link. |
| `is_amazon_choice` | Whether the product carries the Amazon's Choice badge. |
| `seller_name` | Seller name. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `images` | Array of image links in the platform's display order; absent when there are no images. |
| `features` | Bullet-point feature list from the product page (search, profile), as written; absent when there is none. |
| `bestseller_ranks` | Best Sellers ranks (search, profile): each item has rank and category, one entry per category; the rank at read time, not a sales figure. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/amazon-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `reviews` (reviews)

| Field | Meaning |
|---|---|
| `review_id` | Review ID. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `helpful_count` | How many times the review was marked helpful. |
| `is_verified_purchase` | Whether the review is from a verified purchase. |
| `is_vine` | Whether the review comes from the Vine program (the platform sends the product for testing, and the review is labeled as such). |
| `variant` | Product variant the review refers to. |
| `country` | Country or region: a full name or an ISO code depending on the platform, not normalized. |
| `url` | Link to the record on the platform. |
| `author_name` | Reviewer's public display name (reviews), taken from the reviewer's public profile; may be empty. |
| `author_id` | Reviewer's public Amazon profile ID (reviews); may be empty. |
| `author_avatar_url` | Avatar link from the reviewer's public profile (reviews); may be empty or a default avatar. |
| `product_asin` | Product ASIN. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/amazon-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `bestsellers` (bestsellers)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `rank` | Category rank (BSR). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `review_count` | Number of reviews, for product and business capabilities. null means not disclosed, not 0. |
| `category` | Category name in the platform's own taxonomy, not normalized across platforms. |
| `image_url` | Image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |
| `price` | Price as a number without a currency symbol; see currency. |

All parameters and fields: <https://everyinfra.com/en/amazon-api/bestsellers?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### FAQ

**Do I need an Amazon account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

**Can I connect the Amazon API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>.

**What legal points apply when I use Amazon data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Amazon data can I get?**

The EveryInfra Amazon API has 10 capabilities:

- keyword search
- profile or object details
- reviews
- bestsellers
- sellers
- ranked keywords
- competing products
- keyword search volume
- rank overview
- keyword intersections

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### Tested

Before release, we ran the 4 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "camping tent" --out products.csv` | 2026-11-25 12:09 | 8 | $0.002236 |
| `python main.py product "<product url>" --out product.json` | 2026-11-25 12:10 | 1 | $0.001389 |
| `python main.py reviews "<product url>" --out reviews.csv` | 2026-11-25 12:11 | 10 | $0.001389 |
| `python main.py bestsellers "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods" --out bestsellers.csv` | 2026-11-25 12:11 | 20 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读 Amazon 公开数据：按关键词搜商品，读商品详情和买家评价，看类目畅销榜。只需一把 EveryInfra API Key，不用 Amazon 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 4 个能力每千次 $1.39 到 $2.24，失败和空结果不收费。Amazon 共 10 个能力：<https://everyinfra.com/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/amazon-api.git
cd amazon-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "camping tent" --out products.csv
python main.py product "<商品链接>" --out product.json
python main.py reviews "<商品链接>" --out reviews.csv
python main.py bestsellers "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods" --out bestsellers.csv
```

- 商品链接用 `search` 结果里的 `url`，形如 https://www.amazon.com/dp/<ASIN>。
- `bestsellers` 传 Amazon 类目畅销榜的完整链接（链接里带 /zgbs/），在 amazon.com/Best-Sellers 页面点进类目就能拿到。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"amazon","action":"search","params":{"keyword":"camping tent"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`profile`、`reviews`、`bestsellers` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $2.24 |
| 主页或对象详情 | `profile` | $1.39 |
| 评价 | `reviews` | $1.39 |
| 畅销榜 | `bestsellers` | $1.39 |

- 按调用次数计费，每次约 $0.0014 到 $0.0022；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>
- Amazon 其他 6 个能力的单价见平台页 <https://everyinfra.com/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### 返回字段

下面是这 4 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `asin` | Amazon 标准识别号，站内唯一商品标识。 |
| `title` | 标题。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `brand` | 品牌。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `list_price` | 划线原价。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `rating` | 评分。 |
| `rating_count` | 参与评分的人数。 |
| `in_stock` | 是否有货。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `image_url` | 图片链接。 |
| `is_amazon_choice` | 是否有 Amazon's Choice 标。 |
| `seller_name` | 卖家名称。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `images` | 图片链接数组，按平台展示顺序；没有图片时不出现这个字段。 |
| `features` | 商品页上的卖点要点列表（search / profile），按页面原文；没有时没有这个字段。 |
| `bestseller_ranks` | Best Sellers 排名列表（search / profile）：每项含 rank（名次）和 category（所在类目），同一商品在不同类目的名次分开列；是采集时的名次，不是销量。 |
| `rating_scale` | 上一列 `rating` 的满分。 |
| `description` | 简介或描述，通常比 text 短。 |

完整参数和字段：<https://everyinfra.com/amazon-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `asin` | Amazon 标准识别号，站内唯一商品标识。 |
| `title` | 标题。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `brand` | 品牌。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `list_price` | 划线原价。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `rating` | 评分。 |
| `rating_count` | 参与评分的人数。 |
| `in_stock` | 是否有货。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `image_url` | 图片链接。 |
| `is_amazon_choice` | 是否有 Amazon's Choice 标。 |
| `seller_name` | 卖家名称。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `images` | 图片链接数组，按平台展示顺序；没有图片时不出现这个字段。 |
| `features` | 商品页上的卖点要点列表（search / profile），按页面原文；没有时没有这个字段。 |
| `bestseller_ranks` | Best Sellers 排名列表（search / profile）：每项含 rank（名次）和 category（所在类目），同一商品在不同类目的名次分开列；是采集时的名次，不是销量。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/amazon-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `review_id` | 评价 ID。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `helpful_count` | 评价被标「有帮助」次数。 |
| `is_verified_purchase` | 是否为已验证购买的评价。 |
| `is_vine` | 是否为 Vine 计划评价（平台送测，需标注）。 |
| `variant` | 规格变体。 |
| `country` | 国家或地区。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `author_name` | 评论人公开显示的昵称（reviews），来自评论人公开资料，可能为空。 |
| `author_id` | 评论人的 Amazon 公开资料 ID（reviews），可能为空。 |
| `author_avatar_url` | 评论人公开资料里的头像链接（reviews），可能为空或是默认头像。 |
| `product_asin` | 商品 ASIN。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/amazon-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

#### `bestsellers`（畅销榜）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `rank` | 类目排名（BSR）。 |
| `rating` | 评分。 |
| `review_count` | 评价条数，用于商品/商家类能力。 |
| `category` | 分类名称，取值为原平台的分类体系，未做跨平台归一。 |
| `image_url` | 图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `rating_scale` | 上一列 `rating` 的满分。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |

完整参数和字段：<https://everyinfra.com/amazon-api/bestsellers?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### 常见问题

**调用时要不要提供 Amazon 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

**能把 Amazon 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>。

**用 Amazon 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Amazon 的哪些数据？**

Amazon 有 10 个能力：关键词搜索、主页或对象详情、评价、畅销榜、卖家搜索、关键词排名、竞品商品、关键词搜索量、批量商品排名概览、多个商品的共同关键词。每个能力的参数和返回字段见平台页 <https://everyinfra.com/amazon-api?utm_source=github&utm_medium=example_repo&utm_campaign=amazon-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 4 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "camping tent" --out products.csv` | 2026-11-25 12:09 | 8 | $0.002236 |
| `python main.py product "<商品链接>" --out product.json` | 2026-11-25 12:10 | 1 | $0.001389 |
| `python main.py reviews "<商品链接>" --out reviews.csv` | 2026-11-25 12:11 | 10 | $0.001389 |
| `python main.py bestsellers "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods" --out bestsellers.csv` | 2026-11-25 12:11 | 20 | $0.001389 |

`profile` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "title": "Coleman Sundome Camping Tent with Rainfly, 2/3/4/6 Person Tent Sets Up in 10 Mins, Weatherproof Shelter for Camping, Festivals, Backyard, Sleepovers, & More",
  "brand": "Coleman",
  "price": 81.67,
  "currency": "$",
  "rating": 4.6,
  "rating_count": 23206,
  "category": "Sports & Outdoors > Outdoor Recreation > Camping & Hiking > Tents & Shelters > Tents",
  "rating_scale": 5
}
```

## License

MIT
