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
        locations = self.database.get_locations()
        if not locations:
            print("No locations found in the database. Add locations first.")
            return
        start_dt = datetime(2025, 1, 15, 0, 0)
        end_dt = datetime(2025, 1, 16, 0, 0)   # exclusive
        interval = timedelta(minutes=15)

        for location_id, name, area_type in locations:
            speed_limit = self._get_speed_limit(area_type)
            current_time = start_dt
            
            print(f"Simulating for locatio9n: {name} ({area_type}), limit{speed_limit} km/h")

            while current_time < end_dt:
                volume, avg_speed_kmh, pct_speeding = self._generate_reading(
                    current_time.hour,
                    area_type,
                    speed_limit
                )

                ts_str = current_time.isoformat(timespec="minutes")

                self.database.insert_traffic_record(
                    location_id=location_id,
                    ts=ts_str,
                    volume=volume,
                    avg_speed_kmh=avg_speed_kmh,
                    speed_limit_kmh=speed_limit,
                    pct_speeding=pct_speeding
                )

                current_time += interval

    def _get_speed_limit(self, area_type):
        if area_type.lower() == "school zone":
            return 40
        elif area_type.lower() == "residential":
            return 50
        else:
            return 60  # default for arterial/other
    def _generate_reading(self, hour, area_type, speed_limit):
          if 7 <= hour <= 9:          # AM peak
            base_volume = random.randint(25, 50)
          elif 16 <= hour <= 18:      # PM peak
            base_volume = random.randint(30, 55)
          elif 10 <= hour <= 15:      # daytime
            base_volume = random.randint(15, 35)
          elif 19 <= hour <= 21:      # evening
            base_volume = random.randint(5, 20)
          else:                       # night
            base_volume = random.randint(0, 8)  
          volume = base_volume
        
            # Speed behavior by area type
          if area_type.lower() == "school zone":
                mean_over = random.uniform(-5, 8)
          elif area_type.lower() == "residential":
                mean_over = random.uniform(0, 15)
          else:  # arterial / other
                mean_over = random.uniform(5, 20)

          avg_speed_kmh = speed_limit + mean_over

              # Estimate percent speeding from how far over the mean is
          if mean_over <= 0:
            pct_speeding = random.uniform(0, 10)
          else:
            pct_speeding = min(100.0, mean_over * random.uniform(3, 6))

          return volume, avg_speed_kmh, pct_speeding
def main():
        database = TrafficDatabase("traffic_simulation.db")
        database.connect()
        database.create_tables()

        existing_locations = database.get_locations()
        if not existing_locations:
            print("No locations found. Inserting default locations...")
            database.insert_location("School Zone 1", "Birchwood Ave", "School Zone")
            database.insert_location("Residential Collector", "Maplecrest Cres", "Residential")
            database.insert_location("Major Arterial", "Rutherford Rd", "Arterial")
        else:
            print("Locations already exist, skipping insert.")

        simulator = TrafficSimulator(database)
        simulator.run()               

        database.close()              

if __name__ == "__main__":
    main()


