"""請求判定。使用量が上限を超えたら overage(超過課金)対象とする。"""

from usage import UsageMeter


def is_overage(meter, limit_gb):
    """使用量が上限 limit_gb を超えていれば True。ちょうど上限なら超過ではない。"""
    return meter.total > limit_gb


def overage_amount(meter, limit_gb):
    """超過分(GB)。超過していなければ 0。"""
    if is_overage(meter, limit_gb):
        return meter.total - limit_gb
    return 0.0
