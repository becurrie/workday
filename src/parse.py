import hashlib
import copy

from datetime import (
    date,
    datetime,
    timedelta,
)
from subprocess import (
    check_output,
    CalledProcessError,
)

from src.conf.conf import (
    DURATION_MAP,
    HOUR_MAP,
)
from src.conf.config import (
    config,
    data,
)


class RepositoryParser(object):
    """Encapsulate all parsing functionality used when a repository is passed along
    from the application to have it's information refreshed.
    """
    def __init__(self, repository):
        self.repository = repository
        self.hashes = {}
        self.parsed = {}
        self.load()

    def _make_hashes(self, reflog):
        """Generate hashes for reflog entries available.
        """
        for ref in reflog:
            if ref not in self.hashes.values():
                self.hashes[hashlib.md5(ref.encode()).hexdigest()] = ref

    def _make_parsed(self):
        """Generate parsed reflog entries.
        """
        for _hash, ref in self.hashes.items():
            if _hash not in self.parsed:
                # 48c2f7c02a (HEAD -> 4.9, origin/feature/IRISDEV-1788) HEAD@{2021-07-09 18:32:12 -0300}: checkout: moving from feature/IRISDEV-1051 to 4.9
                # commit: "48c2f7c02a"
                # datetime: "2021-07-09 18:32:12 -0300"
                # message: "checkout: moving from feature/IRISDEV-1051 to 4.9"
                commit, timestamp, message, previous, current = (
                    ref.split(" ")[0],
                    ref[ref.find("{") + 1:ref.find("}")],
                    ref[ref.find("checkout: "):],
                    ref[ref.find("from ") + 5:ref.find(" to")],
                    ref[ref.find("to ") + 3:],
                )
                self.parsed[_hash] = {
                    "commit": commit,
                    "timestamp": timestamp,
                    "message": message,
                    "previous": previous,
                    "current": current,
                }

    def reflog(self):
        """Retrieve the raw reflog output for the specified repository.
        """
        return check_output(
            ["git", "reflog", "--date=iso", "--all"],
            cwd=self.repository
        )

    def load(self):
        """Handle loading a repository initially in case it's already been parsed
        before, in which case, a lot of parsing functionality can be skipped.
        """
        if self.repository in data.tracked:
            self.hashes = data.tracked[self.repository]["hashes"]
            self.parsed = data.tracked[self.repository]["parsed"]

    def parse(self):
        """Handle parsing a repository, loading the reflogs output and parsing
        and updating information for the repository in the data file available.
        """
        try:
            reflog = self.reflog()
        except CalledProcessError:
            # Early return, anything better here?
            return

        # Currently only taking "checkout" commands from
        # the reflog to track how long a user is on a given branch,
        # this could be enhanced to track different or more commands.
        reflog = reflog.decode()
        reflog = [ref for ref in reflog.split("\n") if ref and "checkout:" in ref]

        self._make_hashes(reflog)
        self._make_parsed()

        tracked = data.tracked
        tracked[self.repository] = {
            "hashes": self.hashes,
            "parsed": self.parsed,
        }

        data.update(
            tracked=tracked,
        )

    def generate(self):
        """Generate a simple src report for the repository.

        This method is really just meant to generate a list of events that contain
        all of the contextual information required to provide some sort of insight
        into the branches worked on throughout a day.
        """
        self.parse()

        today = date.today()
        yesterday = today - timedelta(days=1)

        today_refs = []
        yesterday_refs = []

        for ref in self.parsed.values():
            ref = copy.deepcopy(ref)
            ref["timestamp"] = datetime.strptime(
                ref["timestamp"],
                "%Y-%m-%d %H:%M:%S %z",
            )

            if ref["timestamp"].date() == today:
                today_refs.append(
                    ref,
                )
            if ref["timestamp"].date() == yesterday:
                yesterday_refs.append(
                    ref,
                )

        yesterday_refs = sorted(
            yesterday_refs,
            key=lambda x: x["timestamp"],
        )
        today_refs = sorted(
            today_refs,
            key=lambda x: x["timestamp"],
        )
        today_refs.insert(0, yesterday_refs[-1])

        events = []

        max_index = len(today_refs)
        cur_index = 0

        for i in range(max_index):
            ref_one = today_refs[cur_index]
            try:
                ref_two = today_refs[cur_index + 1]
            except IndexError:
                ref_two = None

            if not ref_two:
                # No ref two yet means this is the last ref available, we can create
                # a "pseudo" ref to generate an itinerary entry up until now.
                ref_two = {
                    "commit": "pseudo",
                    "timestamp": datetime.now(tz=ref_one["timestamp"].tzinfo),
                    "message": "pseudo",
                    "previous": ref_one["current"],
                    "current": "pseudo",
                }

            cur_index += 1

            if config.hardcoded_start_time:
                hour = HOUR_MAP[config.hardcoded_start_time]
                if (
                    ref_one["timestamp"].hour < hour
                    or ref_one["timestamp"].date() != today
                ):
                    ref_one["timestamp"] = ref_one["timestamp"].replace(
                        day=today.day,
                        hour=hour,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )
            if config.hardcoded_end_time:
                hour = HOUR_MAP[config.hardcoded_end_time]
                if ref_two["timestamp"].hour > hour:
                    ref_two["timestamp"] = ref_two["timestamp"].replace(
                        hour=hour,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )

            event = {
                "start": ref_one["timestamp"],
                "end": ref_two["timestamp"],
                "duration": ref_two["timestamp"] - ref_one["timestamp"],
                "branch": ref_one["current"],
                "issue": ref_one["current"].split("/")[-1] if "/" in ref_one["current"] else ref_one["current"],
            }

            if event["duration"] > timedelta(minutes=DURATION_MAP[config.minimum_event_duration]):
                events.append(
                    event,
                )
        return events
