from app.tasks import scheduler as scheduler_module


class FakeScheduler:
    def __init__(self) -> None:
        self.running = False
        self.jobs = {}
        self.start_calls = 0
        self.shutdown_calls = 0

    def add_job(self, func, trigger: str, id: str, replace_existing: bool, **kwargs) -> None:
        if id in self.jobs and not replace_existing:
            return
        self.jobs[id] = {
            "func": func,
            "trigger": trigger,
            "kwargs": kwargs,
            "replace_existing": replace_existing,
        }

    def start(self) -> None:
        self.running = True
        self.start_calls += 1

    def shutdown(self, wait: bool = False) -> None:
        self.running = False
        self.shutdown_calls += 1


def test_scheduler_start_is_idempotent(monkeypatch) -> None:
    fake_scheduler = FakeScheduler()
    monkeypatch.setattr(scheduler_module, "scheduler", fake_scheduler)

    scheduler_module.start_scheduler()
    scheduler_module.start_scheduler()

    assert fake_scheduler.start_calls == 1
    assert scheduler_module.PIPELINE_JOB_ID in fake_scheduler.jobs
    assert scheduler_module.POSITION_MONITOR_JOB_ID in fake_scheduler.jobs
    assert scheduler_module.PATENT_SCANNER_JOB_ID in fake_scheduler.jobs
    assert scheduler_module.WEEKLY_DIGEST_JOB_ID in fake_scheduler.jobs


def test_scheduler_stop_shuts_down_when_running(monkeypatch) -> None:
    fake_scheduler = FakeScheduler()
    fake_scheduler.running = True
    monkeypatch.setattr(scheduler_module, "scheduler", fake_scheduler)

    scheduler_module.stop_scheduler()

    assert fake_scheduler.shutdown_calls == 1
