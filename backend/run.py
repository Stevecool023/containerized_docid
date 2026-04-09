from app import create_app, db, migrate
from flask.cli import with_appcontext
import click
from sqlalchemy import text

app = create_app()

# Matches migrations: 4e67049fd9a2 (account_types), b8c3a1f5d720 (resource_types)
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


@app.cli.command('seed-db')
def seed_db():
    """Seed reference rows missing after `create-db` + `db stamp` (migrations not applied). Idempotent."""
    from app.models import AccountTypes, ResourceTypes

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

    print('seed-db: finished (account_types + resource_types).')
    print('  Optional: python seed_harvest_sources.py  # harvest_sources / DSpace harvest config')


@app.cli.command('create-db')
def create_db():
    db.create_all()
    print('Database created.')

@app.cli.command('drop-db')
def drop_db():
    db.drop_all()
    print('Database dropped.')

# Migration commands
@app.cli.command('db-init')
def db_init():
    """Initialize migrations."""
    migrate.init()
    print('Migration repository initialized.')

@app.cli.command('db-migrate')
@click.option('--message', '-m', help='Migration message')
def db_migrate(message=None):
    """Create a new migration."""
    migrate.migrate(message=message)
    print('Migration script created.')

@app.cli.command('db-upgrade')
def db_upgrade():
    """Upgrade to the latest migration."""
    migrate.upgrade()
    print('Database upgraded to latest migration.')

@app.cli.command('db-downgrade')
@click.option('--revision', '-r', default='-1', help='Revision to downgrade to')
def db_downgrade(revision):
    """Downgrade the database."""
    migrate.downgrade(revision)
    print(f'Database downgraded to {revision}.')

if __name__ == '__main__':
    # app.run(debug=False, port=5001)
    app.run(debug=True, port=5001)  # Start the server on port 50001
