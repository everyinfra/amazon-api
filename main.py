"""Amazon API 示例（Amazon API in Python）。

  python main.py search "camping tent" --out products.csv                                                                    # 按关键词搜商品 / search products
  python main.py product "<商品链接>" --out product.json                                                                     # 商品详情 / product detail
  python main.py reviews "<商品链接>" --out reviews.csv                                                                      # 商品评价 / reviews
  python main.py bestsellers "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods" --out bestsellers.csv # 类目畅销榜 / best sellers
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜商品 / search products by keyword")
    s.add_argument("keyword")
    s.add_argument("--domain", help="国家站点，默认 amazon.com / marketplace domain, default amazon.com")
    pr = sub.add_parser("product", help="商品详情 / one product")
    pr.add_argument("url")
    r = sub.add_parser("reviews", help="商品评价 / reviews of one product")
    r.add_argument("url")
    b = sub.add_parser("bestsellers", help="类目畅销榜 / best sellers of one category")
    b.add_argument("keyword")
    for x in (s, pr, r, b):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"domain": a.domain} if a.domain else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "product":
        rows, charged = fetch("profile", {"url": a.url})
    elif a.cmd == "reviews":
        rows, charged = fetch("reviews", {"url": a.url})
    else:
        rows, charged = fetch("bestsellers", {"keyword": a.keyword})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
