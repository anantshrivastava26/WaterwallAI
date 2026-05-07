from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion.whatsapp_parser import parse


def infer_latest_date(text: str) -> str | None:
    msgs = list(parse(text))
    if not msgs:
        return None
    return msgs[-1].timestamp.date().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Import WhatsApp chat and fetch daily summary")
    parser.add_argument("--chat-file", required=True, help="Path to WhatsApp .txt export")
    parser.add_argument("--date", default=None, help="Summary date in YYYY-MM-DD (defaults to latest parsed day)")
    parser.add_argument("--api-base", default="http://localhost:8000", help="Backend base URL")
    args = parser.parse_args()

    chat_path = Path(args.chat_file)
    if not chat_path.exists():
        raise SystemExit(f"Chat file not found: {chat_path}")

    text = chat_path.read_text(encoding="utf-8-sig")
    target_date = args.date or infer_latest_date(text)

    with httpx.Client(timeout=120) as client:
        with chat_path.open("rb") as fh:
            resp = client.post(
                f"{args.api_base}/ingest/whatsapp",
                files={"file": (chat_path.name, fh, "text/plain")},
            )
        resp.raise_for_status()
        ingest = resp.json()

        print(f"Ingested -> inserted={ingest.get('inserted', 0)} skipped={ingest.get('skipped', 0)}")

        if target_date is None:
            print("No parseable messages found; summary step skipped.")
            return 0

        summary_resp = client.get(f"{args.api_base}/summary/daily", params={"date": target_date})
        summary_resp.raise_for_status()
        summary = summary_resp.json()

    print(f"Summary date: {target_date}")
    print(f"Messages: {summary.get('messages', 0)}")
    print("Summary:")
    print(summary.get("summary", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
