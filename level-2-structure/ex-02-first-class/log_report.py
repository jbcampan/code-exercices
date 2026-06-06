class LogReport:
    def __init__(self, entries):
        self.entries = entries

    def errors(self):
        return [entry for entry in self.entries if entry.is_error()]

    def warnings(self):
        return [entry for entry in self.entries if entry.is_warning()]

    def count_by_service(self):
        counts = {}

        for entry in self.entries:
            service = entry.service

            if service not in counts:
                counts[service] = 0

            counts[service] += 1

        return counts

    def summary(self):
        return {
            "total_logs": len(self.entries),
            "errors": len(self.errors()),
            "warnings": len(self.warnings()),
            "by_service": self.count_by_service(),
        }

    def to_dict(self):
        return self.summary()