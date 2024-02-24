from utils.percentiles import (
    get_user_average,
    get_all_users_averages,
    calculate_percentile,
    get_user_success_rate,
    get_all_users_success_rates,
    get_user_total,
    get_all_users_totals,
)


def calculate_percentiles(model, user_id):
    percentiles = []
    for attribute in ["actions", "number_of_digits"]:
        avgs = get_all_users_averages(model, attribute)
        percentile = calculate_percentile(user_id, avgs)
        percentiles.append({attribute: percentile})

    totals = get_all_users_totals(model, "game_time")
    game_time_percentile = calculate_percentile(user_id, totals)
    percentiles.append({"game_time": game_time_percentile})

    s_rates = get_all_users_success_rates(model)
    success_percentile = calculate_percentile(user_id, s_rates)
    percentiles.append({"success_rate": success_percentile})

    dict_of_per = {}
    for d in percentiles:
        dict_of_per.update(d)
    return dict_of_per
