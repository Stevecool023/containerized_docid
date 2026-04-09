#!/usr/bin/env python3
"""
Seed account_types and resource_types when the DB was created with create-db + db stamp
(migration inserts never ran). Idempotent.

Usage (inside backend container / venv):
  python seed_reference_data.py

Same logic as: flask --app run:app seed-db
"""
from sqlalchemy import text

from app import create_app, db
from app.models import AccountTypes, ResourceTypes

_ACCOUNT_TYPE_SEEDS = [(1, 'Individual'), (2, 'Institutional')]
_DATACITE_RESOURCE_TYPES = (
    'Text',
    'Dataset',
    'Image',
    'Audiovisual',
    'Collection',
    'Software',
    'Other',
)


def seed_reference_tables() -> None:
    for aid, name in _ACCOUNT_TYPE_SEEDS:
        row = AccountTypes.query.filter_by(id=aid).first()
        if row is None:
            db.session.add(AccountTypes(id=aid, account_type_name=name))
            print(f'  + account_types id={aid} {name!r}')
        elif row.account_type_name != name:
            print(f'  ! account_types id={aid}: expected {name!r}, has {row.account_type_name!r}')
    db.session.commit()

    if db.engine.dialect.name == 'postgresql':
        db.session.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('account_types', 'id'), "
                "COALESCE((SELECT MAX(id) FROM account_types), 1))"
            )
        )
        db.session.commit()

    for rt_name in _DATACITE_RESOURCE_TYPES:
        if ResourceTypes.query.filter_by(resource_type=rt_name).first() is None:
            db.session.add(ResourceTypes(resource_type=rt_name))
            print(f'  + resource_types {rt_name!r}')
    db.session.commit()

    if db.engine.dialect.name == 'postgresql':
        db.session.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('resource_types', 'id'), "
                "COALESCE((SELECT MAX(id) FROM resource_types), 1))"
            )
        )
        db.session.commit()

    print('seed_reference_data: finished (account_types + resource_types).')


def main() -> None:
    app = create_app()
    with app.app_context():
        seed_reference_tables()
        print('  Optional: python seed_harvest_sources.py')


if __name__ == '__main__':
    main()
