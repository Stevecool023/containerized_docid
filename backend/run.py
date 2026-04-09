import subprocess
import sys

from app import create_app, db, migrate
import click

app = create_app()


@app.cli.command('seed-db')
def seed_db():
    """Seed reference rows missing after `create-db` + `db stamp` (migrations not applied). Idempotent."""
    from seed_reference_data import seed_reference_tables

    seed_reference_tables()
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
    # `python run.py seed-db` does NOT call Click/Flask CLI unless we forward argv.
    # Wrong: python run.py create-db  (old behavior: ignored argv and only ran app.run)
    if len(sys.argv) > 1:
        raise SystemExit(
            subprocess.call(
                [sys.executable, '-m', 'flask', '--app', 'run:app', *sys.argv[1:]]
            )
        )
    app.run(debug=True, port=5001)
