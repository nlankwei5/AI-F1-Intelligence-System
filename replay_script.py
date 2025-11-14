import fastf1 
from ingestion.models import TelemetryData
import pandas as pd
import time
from datetime import datetime, timedelta
from analytics.tasks import analyze_lap_telemetry


fastf1.Cache.enable_cache('fastf1_cache')

def simulate_live_race_simple(year, gp, driver='VER', speed_multiplier=1.0):
    session = fastf1.get_session(year, gp, 'R')
    session.load()
    driver_laps = session.laps.pick_driver(driver)
    
    
    race_start_time = datetime.now()
    
    for idx, lap in driver_laps.iterrows():
        lap_number = int(lap['LapNumber'])
        lap_time = lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else 90
        wait_time = lap_time * speed_multiplier 
        print(f"⏳ Lap {lap_number} completing in {wait_time:.1f}s (actual: {lap_time:.1f}s)...")
        time.sleep(wait_time)
        telemetry = lap.get_telemetry()
        
        if telemetry is None or telemetry.empty:
            print(f"⚠️  No telemetry for lap {lap_number}")
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
            print(f"⚠️  Weather data unavailable: {e}")
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
        
        # Save to DB
        if telemetry_objects:
            TelemetryData.objects.bulk_create(telemetry_objects, batch_size=500)

            saved_telemetry = TelemetryData.objects.filter(
                session_id=f"{year}_{gp}_R",
                driver_name=str(lap['Driver']),
                lap=lap_number
            ).first()
            
            if saved_telemetry:
                # Call the analysis task synchronously (waits for completion)
                analyze_lap_telemetry(saved_telemetry.id)
            
            elapsed_time = (datetime.now() - race_start_time).total_seconds()
            print(f"✅ Lap {lap_number} complete! ({len(telemetry_objects)} points) | Race time: {elapsed_time:.1f}s\n")
    
    total_time = (datetime.now() - race_start_time).total_seconds()
    print(f"🏁 Race simulation complete! Total time: {total_time/60:.1f} minutes")