"""Message and ChatLog classes for the Chat Log Detective.

Week 2: Advanced Python & Data Structures | IEEE LGU AI/ML Cohort One
"""
import re

# [HH:MM] sender: message
LINE_PATTERN = re.compile(r"^\[(\d{2}):(\d{2})\]\s+([A-Za-z][A-Za-z0-9_]*):\s*(.+)$")


class Message:
    """One parsed log entry."""

    def __init__(self, timestamp, sender, content):
        self.timestamp = timestamp
        self.sender = sender
        self.content = content
        self.is_system_error = (sender == "SYSTEM"
                                and content.upper().startswith("ERROR"))

    @property
    def hour(self):
        return self.timestamp.split(":")[0]

    @classmethod
    def from_line(cls, line):
        """Parse one raw line. Raises ValueError if the format is wrong."""
        match = LINE_PATTERN.match(line.strip())
        if match is None:
            raise ValueError("does not match '[HH:MM] user: message'")
        hours, minutes, sender, content = match.groups()
        if int(hours) > 23 or int(minutes) > 59:
            raise ValueError(f"invalid time {hours}:{minutes}")
        return cls(f"{hours}:{minutes}", sender, content.strip())

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content}"


class ChatLog:
    """A collection of messages plus the forensic analysis algorithms."""

    def __init__(self):
        self.messages = []
        self.invalid_lines = []   # list of (line_number, raw_text, reason)
        self.total_lines = 0

    def load(self, path):
        """Parse the log file line by line, recovering from bad lines."""
        file = None
        try:
            file = open(path, encoding="utf-8")
            for line_no, raw in enumerate(file, start=1):
                if not raw.strip():
                    continue
                self.total_lines += 1
                try:
                    self.messages.append(Message.from_line(raw))
                except ValueError as error:
                    self.invalid_lines.append((line_no, raw.strip(), str(error)))
        except FileNotFoundError:
            print(f"[Error] Log file not found: {path}")
            return False
        finally:
            if file is not None:
                file.close()
        return True

    def message_counts(self):
        """{username: count} for every sender (SYSTEM included)."""
        counts = {}
        for message in self.messages:
            counts[message.sender] = counts.get(message.sender, 0) + 1
        return counts

    def active_users(self):
        """Set of unique human users (SYSTEM excluded)."""
        return {m.sender for m in self.messages if m.sender != "SYSTEM"}

    def most_active_user(self):
        """Human user with the most messages as (name, count), or None."""
        human_counts = {u: c for u, c in self.message_counts().items() if u != "SYSTEM"}
        if not human_counts:
            return None
        user = max(human_counts, key=human_counts.get)
        return user, human_counts[user]

    def users_with_more_than(self, k):
        """Dictionary comprehension: humans who sent more than k messages."""
        return {u: c for u, c in self.message_counts().items()
                if u != "SYSTEM" and c > k}

    def search_keyword(self, keyword):
        """All messages containing the keyword (case-insensitive)."""
        needle = keyword.strip().lower()
        return [m for m in self.messages if needle and needle in m.content.lower()]

    def system_errors(self):
        return [m for m in self.messages if m.is_system_error]

    def activity_by_hour(self):
        """Nested dictionary: {user: {hour: message_count}}."""
        activity = {}
        for message in self.messages:
            if message.sender == "SYSTEM":
                continue
            per_hour = activity.setdefault(message.sender, {})
            per_hour[message.hour] = per_hour.get(message.hour, 0) + 1
        return activity
