import os
import logging
from dotenv import load_dotenv
import sqlite3
from typing import List, Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)

class ProxyDB:
    def __init__(self, db_path: str = 'database.sqlite'):
        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.debug("Connected to database successfully")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.debug("Database connection closed")

    def insert_proxy(self, proxy_data: Dict[str, str]):
        """Insert or update a proxy record"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO proxies (
                    proxy, ip, port, protocol, response_time,
                    google_pass, anonymity, country, city, isp, status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(proxy) DO UPDATE SET
                    response_time = excluded.response_time,
                    google_pass = excluded.google_pass,
                    anonymity = excluded.anonymity,
                    country = excluded.country,
                    city = excluded.city,
                    isp = excluded.isp,
                    status = excluded.status,
                    updated_at = CURRENT_TIMESTAMP
            ''', (
                proxy_data['proxy'],
                proxy_data.get('ip'),
                proxy_data.get('port'),
                proxy_data.get('protocol'),
                proxy_data.get('response_time'),
                proxy_data.get('google_pass'),
                proxy_data.get('anonymity'),
                proxy_data.get('country'),
                proxy_data.get('city'),
                proxy_data.get('isp'),
                proxy_data.get('status', 'unchecked')
            ))
            self.conn.commit()
            logger.debug(f"Proxy {proxy_data['proxy']} inserted/updated")
        except sqlite3.Error as e:
            logger.error(f"Error inserting proxy: {e}")
            raise

    def get_proxy(self, proxy: str) -> Optional[Dict]:
        """Get a proxy record by proxy string"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM proxies WHERE proxy = ?
            ''', (proxy,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            logger.error(f"Error getting proxy: {e}")
            raise

    def get_proxies_by_protocol(self, protocol: str) -> List[Dict]:
        """Get all proxies of a specific protocol"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM proxies 
                WHERE protocol = ?
            ''', (protocol,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            proxies = []
            for row in rows:
                proxy = dict(zip(columns, row))
                proxies.append(proxy)
            logger.debug(f"First proxy for {protocol}: {proxies[0] if proxies else 'None'}")
            return proxies
        except sqlite3.Error as e:
            logger.error(f"Error getting proxies by protocol: {e}")
            raise

    def mark_proxy_inactive(self, proxy: str):
        """Mark a proxy as inactive"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE proxies 
                SET status = 'inactive' 
                WHERE proxy = ?
            ''', (proxy,))
            self.conn.commit()
            logger.debug(f"Proxy {proxy} marked as inactive")
        except sqlite3.Error as e:
            logger.error(f"Error marking proxy inactive: {e}")
            raise

    def get_active_proxies_by_protocol(self, protocol: str) -> List[Dict]:
        """Get active proxies of a specific protocol"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM proxies 
                WHERE protocol = ? AND status = 'active'
            ''', (protocol,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            proxies = []
            for row in rows:
                proxy = dict(zip(columns, row))
                proxies.append(proxy)
            logger.debug(f"First active proxy for {protocol}: {proxies[0] if proxies else 'None'}")
            return proxies
        except sqlite3.Error as e:
            logger.error(f"Error getting active proxies: {e}")
            raise
