import decimal

def cal_Calories_Burned_During_Exercise(activity, weight, duration):
    MET_values = {
        "Running": 9.8,
        "Bicycling": 8.0,
        "Walking": 5.0
    }
    
    if activity in MET_values:
        MET = decimal.Decimal(str(MET_values[activity]))
        weight = decimal.Decimal(str(weight))
        duration = decimal.Decimal(str(duration))
        calories_burned = MET * weight * duration
        
        return calories_burned
    else:
        return "Invalid activity"
