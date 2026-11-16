from app.models.booking import Booking


def test_booking_model_matches_diagram():
    columns = Booking.__table__.columns
    assert set(columns.keys()) == {
        "id", "ticket_no", "user_id", "customer_name", "service_slug",
        "title", "priority", "city", "site_address", "engineer_id",
        "engineer_name", "engineer_phone", "progress", "status", "total",
        "details", "last_contact", "customer_rating", "customer_feedback",
        "started_at", "completed_at", "payment_status", "amount_paid",
        "invoice_no", "created_at", "updated_at", "created_by", "updated_by",
    }
    assert columns.id.primary_key
    assert columns.ticket_no.unique
    assert {fk.target_fullname for fk in columns.user_id.foreign_keys} == {"profiles.id"}
    assert {fk.target_fullname for fk in columns.engineer_id.foreign_keys} == {"engineers.id"}
