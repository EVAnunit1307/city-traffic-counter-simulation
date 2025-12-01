import sqlite3
from pathlib import Path 
import random
from datetime import datetime, timedelta

class TrafficDatabase:  # Connection to database 
    def __init__(self, db_path): 
        self.db_path = Path(db_path)
        self.conn = None

    def connect(self):
        print(f"Connecting to database at: {self.db_path.resolve()}")
        self.conn = sqlite3.connect(self.db_path)
        print("Connection opened.")

    def close(self):  # Close file if opened
        if self.conn is not None:            
            self.conn.close()
            self.conn = None                 
            print("The connection is now closed.")
        else:
            print("No connection to close.")  
    
    def create_tables(self):
        cursor = self.conn.cursor()  # Create a SQL cursor

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                road_name TEXT NOT NULL,
                area_type TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS traffic_counts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_id INTEGER NOT NULL,
                ts TEXT NOT NULL,
                volume INTEGER NOT NULL,
                avg_speed_kmh REAL NOT NULL,
                speed_limit_kmh INTEGER NOT NULL,
                pct_speeding REAL NOT NULL,
                FOREIGN KEY (location_id) REFERENCES locations(id)
            );
        """)

        self.conn.commit()  # Save changes 
        print("tables created")

    def insert_location(self, name, road_name, area_type):
        cursor = self.conn.cursor()  
    def get_locations(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, area_type FROM locations;")
        return cursor.fetchall()
    def insert_traffic_record(self, location_id, ts, volume, avg_speed_kmh,
                          speed_limit_kmh, pct_speeding):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO traffic_counts (
                location_id, ts, volume, avg_speed_kmh,
                speed_limit_kmh, pct_speeding
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (location_id, ts, volume, avg_speed_kmh, speed_limit_kmh, pct_speeding))
        self.conn.commit()


class TrafficSimulator:  # Handles simulation logic
    def __init__(self, database):
        self.database = database

    def run(self):
        print("Starting traffic simulation for one day...")
        self.simulate_day()
        print("Traffic simulation complete.")
    def simulate_day(self):
        if not locations:
            print("No locations found in the database. Add locations first.")
            return
def main():
    database = TrafficDatabase("traffic_simulation.db")
    database.connect()
    database.create_tables()

    simulator = TrafficSimulator(database)
    simulator.run()               

    database.close()              

if __name__ == "__main__":
    main()


