import decimal

def cal_Calories_Burned_During_Exercise(activity, weight, duration):
    MET_values = {
        'walking': 3.5,
        'jogging': 7,
        'cycling': 5.5,
        'swimming': 6,
    }

    if activity in MET_values:
        MET = decimal.Decimal(MET_values[activity])
        weight = decimal.Decimal(weight)
        duration = decimal.Decimal(duration)
        calories_burned = MET * weight * duration * decimal.Decimal(0.0175)

        return calories_burned
    else:
        return "Invalid activity"
