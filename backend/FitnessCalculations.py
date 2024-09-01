import decimal

def cal_Calories_Burned_During_Exercise(activity, weight, duration):
    MET_values = {
        "Running": 9.8,
        "Bicycling": 8.0,
        "Walking": 5.0
    }
    
    if activity in MET_values:
        MET = decimal.Decimal(MET_values[activity])
        weight = decimal.Decimal(weight)
        duration = decimal.Decimal(duration)
        calories_burned = MET * weight * duration
        
        return calories_burned
    else:
        return "Invalid activity"
