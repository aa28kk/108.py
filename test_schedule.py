from shooting_performance_analyzer import ShootingDataManager, ShootingPerformanceAPI, PracticeScheduleGenerator

mgr = ShootingDataManager('test_data.json')
api = ShootingPerformanceAPI(api_key=None)
# clear existing sessions
mgr.sessions = []
# add two sessions
mgr.add_session(series=[{'seven_or_less':0,'eights':1,'nines':8,'tens':1}])
mgr.add_session(series=[{'seven_or_less':0,'eights':0,'nines':4,'tens':6}])

analyses = [api.analyze_session(s) for s in mgr.get_all_sessions()]
print('analyses', analyses)
print('recommendations', api.generate_recommendations(analyses))
print('schedule:')
schedule_text = PracticeScheduleGenerator.generate_schedule(api.generate_recommendations(analyses), days=7, save_path='test_schedule.txt')
print(schedule_text[:400])
