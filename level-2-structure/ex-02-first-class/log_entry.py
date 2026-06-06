class LogEntry:
    def __init__(self, date, time, level, service, message):
        self.date = date
        self.time = time
        self.level = level
        self.service = service
        self.message = message

    def is_error(self):
        return self.level == "ERROR"

    def is_warning(self):
        return self.level == "WARNING"

    def format_short(self):
        return f"[{self.level}] {self.service}: {self.message}"

    def __str__(self):
        return self.format_short()

    def __repr__(self):
        return (
            f"LogEntry(date='{self.date}', "
            f"time='{self.time}', "
            f"level='{self.level}', "
            f"service='{self.service}')"
        )