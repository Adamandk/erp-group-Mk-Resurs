def authenticate_user(db: Session, email: str, password: str):
    sql = text("""
        SELECT 
            i.identity_id,
            i.party_id,
            i.password_hash,
            COALESCE(pra.role_code, 'employee') AS role_code,
            p.display_name,
            m.my_company_id
        FROM identities i
        JOIN parties p 
            ON p.party_id = i.party_id
        LEFT JOIN party_role_assignments pra 
            ON pra.party_id = i.party_id 
           AND pra.is_active = true
        LEFT JOIN my_company_affiliation m
            ON m.party_id = i.party_id
           AND (m.end_date IS NULL OR m.end_date > now())
        WHERE i.provider = 'email' 
          AND i.provider_user_id = :email
        LIMIT 1
    """)

    row = db.execute(sql, {"email": email}).fetchone()
    if not row:
        return None

    (
        identity_id,
        party_id,
        password_hash,
        role_code,
        display_name,
        my_company_id,
    ) = row

    if not verify_password(db, password, password_hash):
        return None

    return {
        "identity_id": identity_id,
        "party_id": party_id,
        "role_code": role_code or "employee",
        "display_name": display_name or "",
        "my_company_id": my_company_id,
    }