import sqlite3
from pathlib import Path 

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

        cursor.execute("""
            INSERT INTO locations (name, road_name, area_type)
            VALUES (?, ?, ?)
        """, (name, road_name, area_type))

        self.conn.commit()

        print(f"Inserted location: {name} on {road_name} ({area_type})")
            


class TrafficSimulator:  # Handles simulation logic
    def __init__(self, database):
        self.database = database

    def run(self):
        print("The traffic simulator is now ready.\nSimulation will go here later.")

def main():
    database = TrafficDatabase("traffic_simulation.db")
    database.connect()
    database.create_tables()

    simulator = TrafficSimulator(database)
    simulator.run()               # FIX: you wrote "simualtor"

    database.close()              # FIX: you forgot parentheses

if __name__ == "__main__":
    main()


