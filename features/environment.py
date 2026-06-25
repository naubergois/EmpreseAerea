"""Configuração do ambiente BDD."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from database import init_db, SessionLocal
from main import app
from seed import seed_data


def before_all(context):
    os.environ['DATABASE_URL'] = 'sqlite:///./test_bdd.db'
    if os.path.exists('test_bdd.db'):
        os.remove('test_bdd.db')
    init_db()
    seed_data()
    context.client = TestClient(app)
    context.world = {}


def before_scenario(context, scenario):
    context.world = {}
    event_bus_clear()


def after_all(context):
    if os.path.exists('test_bdd.db'):
        os.remove('test_bdd.db')


def event_bus_clear():
    from event_bus import event_bus
    event_bus.clear()
