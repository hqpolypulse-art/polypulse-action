import os
import sys
from datetime import datetime

def generate_report():
    today = datetime.now().strftime("%Y-%m-%d")
    report = (
        f"⚡ **PolyPulse Daily Community Sentiment & Pulse Report** | [{today}]\n\n"
        f"📊 **Market & Community Mood Summary:**\n"
        f"- Sentiment Index: Dynamic Community Tracking Active\n"
        f"- Key Signals: High Engagement on Global Market Trends\n"
        f"- Automated Pulse Check: Live on Reddit Canvas\n\n"
        f"👉 Cast your live vote and see real-time community sentiment in the pinned interactive post above!\n\n"
        f"---\n"
        f"*Generated automatically by PolyPulse Autonomous Social Agent.*"
    )
    return report

def main():
    print("🚀 Initializing PolyPulse Autonomous Agent...")
    report_content = generate_report()
    print("Generated Report:\n", report_content)

    # حفظ التقرير في ملف ليتم توثيقه واستخدامه عبر سير العمل
    os.makedirs("output", exist_ok=True)
    with open("output/daily_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)

    print("✅ Report generated and saved successfully!")

if __name__ == "__main__":
    main()
