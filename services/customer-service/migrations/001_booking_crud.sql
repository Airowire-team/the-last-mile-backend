-- One-time migration from the legacy booking schema. Run the entire file.
-- Legacy columns are retained; their original values are also copied to details.
-- profiles and engineers do not exist on this database, so their foreign keys
-- must be added separately when those tables and identity mappings are available.
BEGIN;
SET LOCAL lock_timeout = '5s';
SET LOCAL statement_timeout = '30s';
LOCK TABLE public.bookings IN ACCESS EXCLUSIVE MODE;

CREATE TEMP TABLE booking_legacy_snapshot ON COMMIT DROP AS
SELECT id, to_jsonb(b) AS original FROM public.bookings AS b;

ALTER TABLE public.bookings
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
    ALTER COLUMN total_payable DROP NOT NULL;

UPDATE public.bookings AS b
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
WHERE b.id = s.id;

ALTER TABLE public.bookings
    ALTER COLUMN ticket_no SET NOT NULL,
    ADD CONSTRAINT bookings_ticket_no_key UNIQUE (ticket_no);

-- Abort rather than commit if any original field or row was lost.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM booking_legacy_snapshot AS s
        LEFT JOIN public.bookings AS b ON b.id = s.id
        WHERE b.id IS NULL OR NOT (to_jsonb(b) @> s.original)
    ) OR (SELECT count(*) FROM public.bookings)
        <> (SELECT count(*) FROM booking_legacy_snapshot)
    THEN
        RAISE EXCEPTION 'Legacy booking data was not preserved';
    END IF;
END $$;
COMMIT;
