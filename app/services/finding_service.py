from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.finding import Finding


def reconcile_finding(db: Session, server_id: int, check_id: int, severity: str, passed: bool) -> None:
    open_finding = (
        db.query(Finding)
        .filter(
            Finding.server_id == server_id,
            Finding.check_id == check_id,
            Finding.status == "open",
        )
        .first()
    )

    now = datetime.now(timezone.utc)

    if not passed:
        if open_finding:
            # Same problem seen again — update, do not create a duplicate.
            open_finding.last_seen_at = now
        else:
            new_finding = Finding(
                server_id=server_id,
                check_id=check_id,
                severity=severity,
                status="open",
                first_detected_at=now,
                last_seen_at=now,
            )
            db.add(new_finding)
    else:
        if open_finding:
            open_finding.status = "resolved"
            open_finding.resolved_at = now
        # If there's no open finding and the check passed, there's nothing to do.