"""Chat Log Detective - forensic log analyzer.

Week 2: Advanced Python & Data Structures | IEEE LGU AI/ML Cohort One
Usage: python main.py [path-to-log]
"""
import os
import sys

from models import ChatLog

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chat.txt")
LINE = "=" * 58


def section(title):
    print(f"\n--- {title} ---")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
    log = ChatLog()
    print(LINE)
    print("            CHAT LOG DETECTIVE - INVESTIGATION REPORT")
    print(LINE)
    if not log.load(path):
        return

    section("Summary")
    print(f"  Lines processed   : {log.total_lines}")
    print(f"  Valid messages    : {len(log.messages)}")
    print(f"  Invalid lines     : {len(log.invalid_lines)}")
    print(f"  SYSTEM errors     : {len(log.system_errors())}")

    section("Messages per user")
    for user, count in sorted(log.message_counts().items(), key=lambda kv: -kv[1]):
        print(f"  {user:<8} {count}")

    section("Active users (humans only)")
    print("  " + ", ".join(sorted(log.active_users())))

    section("Most active user")
    top = log.most_active_user()
    print(f"  {top[0]} with {top[1]} messages" if top else "  No human messages.")

    section("SYSTEM ERROR alerts")
    for message in log.system_errors():
        print(f"  {message}")

    section("Invalid lines (skipped)")
    for line_no, text, reason in log.invalid_lines:
        print(f"  line {line_no:>2}: {text!r}  -> {reason}")

    section("Keyword investigation")
    try:
        keyword = input("  Keyword to search (e.g. database): ")
        results = log.search_keyword(keyword)
        print(f"  {len(results)} message(s) contain '{keyword.strip()}':")
        for message in results:
            print(f"    {message}")

        section("Chatty users filter")
        k = int(input("  Show users who sent more than k messages. k = "))
        chatty = log.users_with_more_than(k)
        print(f"  Users with more than {k} messages: {chatty or 'none'}")
    except ValueError:
        print("  [Error] k must be a whole number. Skipping this filter.")
    except EOFError:
        pass
    print("\nInvestigation complete.")


if __name__ == "__main__":
    main()
