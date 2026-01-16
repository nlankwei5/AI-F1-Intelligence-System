import fastf1 
from ingestion.models import TelemetryData
import pandas as pd
import time
from datetime import datetime, timedelta
import json
from kafka import KafkaProducer


fastf1.Cache.enable_cache('fastf1_cache')



def create_kafka_producer(bootstrap_servers='localhost:9092'):
    '''
    Initialize Kafka producer
    '''
    
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def send_telemetry_to_kafka(producer, topic, telemetry_data, key=None):
    '''
    Send telemetry data to Kafka topic
    '''
    producer.send(topic, telemetry_data, key=key)
    producer.flush()
    return True





def simulate_live_race_simple(year, gp, driver='VER', speed_multiplier=1.0,  kafka_bootstrap_servers='localhost:9092',
                            kafka_topic='telemetry_topic'):
    producer = create_kafka_producer(kafka_bootstrap_servers)
    
    session = fastf1.get_session(year, gp, 'R')
    session.load()
    driver_laps = session.laps.pick_driver(driver)
    
    
    race_start_time = datetime.now()
    
    for idx, lap in driver_laps.iterrows():
        lap_number = int(lap['LapNumber'])
        lap_time = lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else 90
        wait_time = lap_time * speed_multiplier 
        print(f"⏳ Lap {lap_number} completing in {wait_time:.1f}s (actual: {lap_time:.1f}s)...")
        
        telemetry = lap.get_telemetry()
        
        if telemetry is None or telemetry.empty:
            print(f" No telemetry for lap {lap_number}")
            continue
        
        # Sample telemetry
        sampled_telemetry = telemetry.iloc[::10]

        lap_compound = str(lap['Compound']) if pd.notna(lap['Compound']) else 'UNKNOWN'
            
        # FIXED: Handle weather data properly
        try:
            if not session.weather_data.empty:
                rainfall_value = session.weather_data['Rainfall'].iloc[0]
                # Convert to float safely
                rainfall = float(rainfall_value) if pd.notna(rainfall_value) else 0.0
            else:
                rainfall = 0.0
        except (KeyError, IndexError, AttributeError) as e:
            print(f"Weather data unavailable: {e}")
            rainfall = 0.0 

        # Build objects
        telemetry_objects = []
        for telem_idx, telem_row in sampled_telemetry.iterrows():
            telemetry_obj = TelemetryData(
                driver_name=lap['Driver'],
                team=lap['Team'],
                circuit_name=session.event['EventName'],
                lap=lap_number,
                speed=float(telem_row['Speed']) if pd.notna(telem_row['Speed']) else 0.0,
                throttle=float(telem_row['Throttle']) if pd.notna(telem_row['Throttle']) else 0.0,
                brake=float(telem_row['Brake']) if pd.notna(telem_row['Brake']) else 0.0,
                gear=int(telem_row['nGear']) if pd.notna(telem_row['nGear']) else 0,
                tyre = lap_compound,
                weather = rainfall,
                rpm=int(telem_row['RPM']) if pd.notna(telem_row['RPM']) else 0,
                drs=bool(telem_row['DRS']) if pd.notna(telem_row['DRS']) else False,
                session_type='R',
                session_id=f"{year}_{gp}_R"
            )
            telemetry_objects.append(telemetry_obj)
        
        
        
        telemetry_dict = [obj.__dict__ for obj in telemetry_objects]

        
        num_points = len(telemetry_dict)
        point_delay = wait_time / num_points if num_points > 0 else 0
        
        print(f" Lap {lap_number} starting - streaming {num_points} points over {wait_time:.1f}s...")
        

        for point_index, single_point in enumerate(telemetry_dict):
            # Create unique key for ordering
            message_key = f"{driver}_lap{lap_number}_point{point_index}"
            
            # Send single point
            send_telemetry_to_kafka(producer, kafka_topic, single_point, key=message_key)
            
            # Wait before next point (simulates live data stream)
            time.sleep(point_delay)
        
        print(f" Lap {lap_number} complete - sent {num_points} telemetry points")
    
    total_time = (datetime.now() - race_start_time).total_seconds()
    print(f"🏁 Race simulation complete! Total time: {total_time/60:.1f} minutes")