from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


class Cache:
    def __init__(self, app, cache_url='sqlite:////tmp/test.db'):
        app.config['SQLALCHEMY_DATABASE_URI'] = cache_url
        self.db = SQLAlchemy(app)
        self.record_class = self._create_record_class()
        self.db.create_all()  # why create if already wxists

    def _create_record_class(self):
        class Record(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            key = self.db.Column(self.db.Text(), unique=True, nullable=False)
            val = self.db.Column(self.db.Text(), nullable=False)

            def __repr__(self):
                return f"({self.id}, {self.key}, {self.val})"
        return Record

    def _get_all(self, key: str):
        with Session(self.db.engine) as session:
            query = "SELECT val FROM Record WHERE key = :key"
            return session.execute(query, {"key": key}).all()

    def has(self, key: str):
        return len(self._get_all(key)) > 0

    def get(self, key: str, default=None):
        records = self._get_all(key)
        if len(records) == 0:
            return default
        return records[0].val

    def set(self, key, val):
        with Session(self.db.engine) as session:
            session.execute("""
            INSERT INTO Record (key, val)
                VALUES
                    (:key, :val)
                ON CONFLICT (key) DO UPDATE
                SET
                    key = :key,
                    val = :val
            """, {"key": key, "val": val})
            session.commit()
