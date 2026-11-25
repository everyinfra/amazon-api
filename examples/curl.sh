#!/usr/bin/env bash
# Amazon API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Amazon API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "camping tent"
#   bash examples/curl.sh profile "<product url>"                                                             # search 结果里的 url / the url from a search result
#   bash examples/curl.sh reviews "<product url>"                                                             # search 结果里的 url / the url from a search result
#   bash examples/curl.sh bestsellers https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods # 类目畅销榜的完整链接 / the full link of a best sellers page
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|profile|reviews|bestsellers> <value>"}
value=${2:?"value: a keyword, a product url or a best sellers url"}

case "$action" in
  search | bestsellers) params="{\"keyword\":\"$value\"}" ;;
  profile | reviews)    params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, profile, reviews or bestsellers)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"amazon\",\"action\":\"$action\",\"params\":$params}"
echo
