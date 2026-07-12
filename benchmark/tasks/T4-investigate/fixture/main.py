"""日次レポート生成のエントリポイント。"""

import os

from config import load_config
from fetcher import fetch_sales
from report import render


def main():
    config = load_config()
    sales = fetch_sales(config)
    output = render(sales, config)
    os.makedirs(config["output_dir"], exist_ok=True)
    path = os.path.join(config["output_dir"], "daily.txt")
    with open(path, "w") as f:
        f.write(output)
    print(f"レポートを出力しました: {path}")


if __name__ == "__main__":
    main()
