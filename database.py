#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data access layer - Maneja la persistencia de datos
"""

import sqlite3
from typing import List, Tuple, Optional
from pathlib import Path


class ChannelDatabase:
    """Gestiona el acceso a la base de datos de canales"""

    DB_NAME = "channels.db"

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(Path(__file__).parent / self.DB_NAME)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_data()

    def _create_tables(self) -> None:
        """Crea las tablas si no existen"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                instance TEXT NOT NULL UNIQUE,
                page_url TEXT,
                stream_url TEXT NOT NULL,
                category TEXT DEFAULT 'General'
            )
        """)
        self.conn.commit()

    def _seed_data(self) -> None:
        """Inserta datos iniciales si la tabla esta vacia"""
        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM channels")
            count = cursor.fetchone()[0]
            if count == 0:
                self._insert_channels(cursor)
        except sqlite3.OperationalError:
            self._insert_channels(cursor)

        self.conn.commit()

    def _insert_channels(self, cursor) -> None:
        """Inserta los canales reales desde channels_real.py"""
        from channels_real import CHANNELS

        for ch in CHANNELS:
            cursor.execute(
                "INSERT INTO channels (title, instance, page_url, stream_url, category) VALUES (?, ?, ?, ?, ?)",
                (
                    ch["title"],
                    ch["instance"],
                    ch["page_url"],
                    ch["stream_url"],
                    ch.get("category", "General"),
                ),
            )

    def get_all_channels(self) -> List[Tuple]:
        """Obtiene todos los canales ordenados por titulo"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT title, instance, page_url, stream_url FROM channels ORDER BY title"
        )
        channels = cursor.fetchall()
        return channels

    def get_channel_by_instance(self, instance: str) -> Optional[Tuple]:
        """Obtiene un canal especifico por su instancia"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT title, page_url, stream_url FROM channels WHERE instance = ?",
            (instance,),
        )
        channel = cursor.fetchone()
        return channel

    def get_channels_by_category(self, category: str) -> List[Tuple]:
        """Obtiene canales por categoria"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT title, instance, page_url, stream_url FROM channels WHERE category = ? ORDER BY title",
            (category,),
        )
        return cursor.fetchall()

    def get_channel_count(self) -> int:
        """Retorna el numero total de canales"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM channels")
        count = cursor.fetchone()[0]
        return count

    def close(self) -> None:
        """Cierra la conexion a la base de datos"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db = ChannelDatabase()
    print(f"Total de canales: {db.get_channel_count()}")
    db.close()
