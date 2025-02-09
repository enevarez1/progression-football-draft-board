import openpyxl as x

from src.report.model import Evaluation, Exercise, Player, UserValues

def retrieve_custom_values():
    wb = x.load_workbook('custom_values.xlsx')
    sheet = wb.active
    # Map to a model
    custom_values = UserValues()
    custom_values.overall_weight = sheet['B2'].value
    custom_values.ras_weight = sheet['B3'].value
    custom_values.report_weight = sheet['B4'].value
    custom_values.all_pro = sheet['B5'].value
    custom_values.sky_high = sheet['B6'].value
    custom_values.great_upside = sheet['B7'].value
    custom_values.great_pfl = sheet['B8'].value
    custom_values.starting = sheet['B9'].value
    custom_values.long_term = sheet['B10'].value
    custom_values.consistent = sheet['B11'].value
    custom_values.solid = sheet['B12'].value
    custom_values.mistakes = sheet['B13'].value
    custom_values.film = sheet['B14'].value
    custom_values.strategy = sheet['B15'].value
    custom_values.energetic = sheet['B16'].value
    custom_values.professional = sheet['B17'].value
    custom_values.aggressive = sheet['B18'].value
    custom_values.adaptive = sheet['B19'].value

    return custom_values



