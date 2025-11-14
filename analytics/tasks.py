from celery import shared_task
from ingestion.models import TelemetryData
from .models import analytics_and_prediction
from .services import analyze_with_gpt

@shared_task
def analyze_lap_telemetry(telemetry_id):
    telemetry = TelemetryData.objects.get(id=telemetry_id)
    
    # Create or fetch an analysis record
    analysis, _ = analytics_and_prediction.objects.get_or_create(telemetry=telemetry)
    analysis.status = 'processing'
    analysis.save()

    try:
        summary = (
            f"Driver: {telemetry.driver_name}\n"
            f"Lap {telemetry.lap}\n"
            f"Speed: {telemetry.speed} km/h\n"
            f"RPM: {telemetry.rpm}\n"  
            f"Throttle: {telemetry.throttle}%\n"
            f"Brake: {telemetry.brake}%\n"
            f"Gear: {telemetry.gear}\n"  
            f"Tyre: {telemetry.tyre}\n" 
            f"Weather: {telemetry.weather}\n"  
            f"DRS: {telemetry.drs}\n"  
        )

        prompt = (
            "You are a senior telemetry engineer on the pit wall. "
            "Analyze the following telemetry data and provide insights and predictions:\n\n" + summary
        )

        ai_response = analyze_with_gpt(prompt)

        analysis.prompt = prompt
        analysis.ai_response = ai_response
        analysis.status = 'complete'
        analysis.save()
        
        print(f"✅ Analysis complete for {telemetry.driver_name} lap {telemetry.lap}")

    except Exception as e:
        print(f"❌ Analysis error: {e}")
        analysis.status = 'error'
        analysis.ai_response = str(e)
        analysis.save()