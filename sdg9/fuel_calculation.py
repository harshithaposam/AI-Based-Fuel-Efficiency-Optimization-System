# el/sdg9/fuel_calculation.py
import pandas as pd

def calculate_fuel_consumption(route_length, mileage_impact):
    base_mileage = 15  # Assume a base mileage of 15 km per liter
    adjusted_mileage = base_mileage * (1 + mileage_impact / 100)
    return route_length / adjusted_mileage

def get_mileage_impact(weather, traffic, elevation, dataset):
    match = dataset[(dataset['Temperature'] == weather['Temperature']) &
                    (dataset['Rain'] == weather['Rain']) &
                    (dataset['Traffic'] == traffic) &
                    (dataset['Elevation'] == elevation)]
    if not match.empty:
        return float(match.iloc[0]['Combined Four-Wheelers Impact'].strip('%'))
    return 0

def calculate_fuel_consumption(route_length, mileage_impact):
    base_mileage = 15  # Assume a base mileage of 15 km per liter
    adjusted_mileage = base_mileage * (1 + mileage_impact / 100)
    return route_length / adjusted_mileage

def get_mileage_impact(weather, traffic, elevation, dataset):
    match = dataset[(dataset['Temperature'] == weather['Temperature']) &
                    (dataset['Rain'] == weather['Rain']) &
                    (dataset['Traffic'] == traffic) &
                    (dataset['Elevation'] == elevation)]
    if not match.empty:
        return float(match.iloc[0]['Combined Four-Wheelers Impact'].strip('%'))
    return 0