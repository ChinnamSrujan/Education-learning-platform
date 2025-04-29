import app

# Test if generate_daily_timetable is defined
print("Checking if generate_daily_timetable is defined...")
if hasattr(app, 'generate_daily_timetable'):
    print("✅ generate_daily_timetable is defined")
else:
    print("❌ generate_daily_timetable is NOT defined")

# Test if display_timetable is defined
print("Checking if display_timetable is defined...")
if hasattr(app, 'display_timetable'):
    print("✅ display_timetable is defined")
else:
    print("❌ display_timetable is NOT defined")

# Test if hours_per_week is defined
print("Checking if hours_per_week is defined...")
if hasattr(app, 'hours_per_week'):
    print("✅ hours_per_week is defined")
else:
    print("❌ hours_per_week is NOT defined")
