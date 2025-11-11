from celery import shared_task
import random
from replay_script import simulate_live_race_simple


@shared_task
def run_replay_script():
    years = range(2018, 2025)
    gp_identifiers = ['Bahrain', 'Monaco', 'Silverstone', 'Monza', 'Abu Dhabi', 'Miami']
    random_year = random.choice(years)
    random_gp = random.choice(gp_identifiers)
    simulate_live_race_simple(random_year, random_gp)




