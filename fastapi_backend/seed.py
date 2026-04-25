from app.database import SessionLocal
from app.seed_data import seed_database


def main() -> None:
    db = SessionLocal()
    try:
        seed_database(db)
        print("Seed completed successfully.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
