"""Migrate legacy bookings without losing rows or removing legacy columns.

Run from the service directory: python migrations\\001_booking_crud.py
Uses DATABASE_URL from the environment, falling back to the service's .env.
Already migrated or incompatible tables fail without committing changes.
Foreign keys require a separate migration once profiles and engineers exist.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
a

def migrate(connection: Connection, schema: str = "public") -> int:
    """Run inside a caller-owned transaction; return the preserved row count."""
    table = connection.dialect.identifier_preparer.quote_schema(schema) + ".bookings"
    connection.execute(text("SET LOCAL lock_timeout = '5s'"))
    connection.execute(text("SET LOCAL statement_timeout = '30s'"))
    connection.execute(text(f"LOCK TABLE {table} IN ACCESS EXCLUSIVE MODE"))
    connection.execute(text(f"""
        CREATE TEMP TABLE booking_legacy_snapshot ON COMMIT DROP AS
        SELECT id, to_jsonb(b) AS original FROM {table} AS b
    """))
    connection.execute(text(f"""
        ALTER TABLE {table}
            ADD COLUMN ticket_no TEXT,
            ADD COLUMN user_id UUID,
            ADD COLUMN customer_name TEXT,
            ADD COLUMN service_slug TEXT,
            ADD COLUMN title TEXT,
            ADD COLUMN city TEXT,
            ADD COLUMN site_address TEXT,
            ADD COLUMN engineer_id UUID,
            ADD COLUMN engineer_name TEXT,
            ADD COLUMN engineer_phone TEXT,
            ADD COLUMN progress INTEGER DEFAULT 0,
            ADD COLUMN total NUMERIC(12, 2),
            ADD COLUMN details JSONB,
            ADD COLUMN last_contact TEXT,
            ADD COLUMN customer_rating INTEGER,
            ADD COLUMN customer_feedback TEXT,
            ADD COLUMN started_at TIMESTAMPTZ,
            ADD COLUMN completed_at TIMESTAMPTZ,
            ADD COLUMN payment_status TEXT,
            ADD COLUMN amount_paid NUMERIC(12, 2),
            ADD COLUMN invoice_no TEXT,
            ADD COLUMN created_by UUID,
            ADD COLUMN updated_by UUID,
            ALTER COLUMN priority TYPE TEXT,
            ALTER COLUMN status TYPE TEXT,
            ALTER COLUMN customer_id DROP NOT NULL,
            ALTER COLUMN customer_type DROP NOT NULL,
            ALTER COLUMN engineer_level DROP NOT NULL,
            ALTER COLUMN engineer_count DROP NOT NULL,
            ALTER COLUMN start_date DROP NOT NULL,
            ALTER COLUMN end_date DROP NOT NULL,
            ALTER COLUMN duration DROP NOT NULL,
            ALTER COLUMN hours DROP NOT NULL,
            ALTER COLUMN start_time DROP NOT NULL,
            ALTER COLUMN site DROP NOT NULL,
            ALTER COLUMN contacts DROP NOT NULL,
            ALTER COLUMN issue_description DROP NOT NULL,
            ALTER COLUMN subtotal DROP NOT NULL,
            ALTER COLUMN gst DROP NOT NULL,
            ALTER COLUMN total_payable DROP NOT NULL
    """))
    connection.execute(text(f"""
        UPDATE {table} AS b
        SET ticket_no = 'BK-' || upper(replace(b.id::text, '-', '')),
            user_id = b.customer_id,
            customer_name = b.site ->> 'name',
            service_slug = 'field-engineer-support',
            title = b.issue_description,
            site_address = b.site ->> 'address',
            engineer_name = 'Unassigned',
            total = b.total_payable,
            details = s.original
        FROM booking_legacy_snapshot AS s
        WHERE b.id = s.id
    """))
    connection.execute(text(f"""
        ALTER TABLE {table}
            ALTER COLUMN ticket_no SET NOT NULL,
            ADD CONSTRAINT bookings_ticket_no_key UNIQUE (ticket_no)
    """))
    lost_data = connection.execute(text(f"""
        SELECT EXISTS (
            SELECT 1
            FROM booking_legacy_snapshot AS s
            LEFT JOIN {table} AS b ON b.id = s.id
            WHERE b.id IS NULL OR NOT (to_jsonb(b) @> s.original)
        )
    """)).scalar_one()
    before = connection.execute(text(
        "SELECT count(*) FROM booking_legacy_snapshot"
    )).scalar_one()
    after = connection.execute(text(f"SELECT count(*) FROM {table}")).scalar_one()
    if lost_data or before != after:
        raise RuntimeError("Legacy booking data was not preserved")
    return after


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set to run the migration")

    engine = create_engine(database_url, hide_parameters=True)
    try:
        with engine.begin() as connection:
            if connection.dialect.name != "postgresql":
                raise RuntimeError("This migration requires PostgreSQL")
            count = migrate(connection)
        print(f"Migration committed; preserved {count} bookings.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
