"""レポートの整形と出力。"""

LABELS = {
    "en": {"title": "Daily Sales Report", "total": "Total"},
    "ja": {"title": "日次売上レポート", "total": "合計"},
}


def render(sales, config):
    locale = config["locale"] or "en"
    labels = LABELS.get(locale, LABELS["en"])
    lines = [labels["title"], "-" * 20]
    total = 0
    for item in sales:
        lines.append(f"{item['name']}: {item['amount']}")
        total += item["amount"]
    lines.append(f"{labels['total']}: {total}")
    return "\n".join(lines)
