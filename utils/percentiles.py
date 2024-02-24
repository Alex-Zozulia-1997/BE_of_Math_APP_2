from sqlalchemy import func


def get_user_average(model, user_id, attribute):
    result = (
        model.query.filter_by(user_id=user_id)
        .with_entities(func.avg(getattr(model, attribute)))
        .scalar()
    )
    return result if result is not None else 0


def get_all_users_averages(model, attribute):
    all_users = model.query.with_entities(model.user_id).distinct()
    avgs = []
    for user in all_users:
        avg = get_user_average(model, user.user_id, attribute)
        avgs.append((user.user_id, avg))
    return avgs


def calculate_percentile(user_id, avgs):
    avgs.sort(key=lambda x: x[1])
    user_position = next((i for i, v in enumerate(avgs) if v[0] == user_id), -1)
    percentile = (
        (user_position / (len(avgs) - 1)) * 100
        if user_position != -1 and len(avgs) > 1
        else 0
    )
    return round(percentile, 2)


def get_user_success_rate(model, user_id):
    success_rate = (
        model.query.filter_by(user_id=user_id, game_won=True).count()
        / model.query.filter_by(user_id=user_id).count()
        * 100
    )
    return success_rate


def get_all_users_success_rates(model):
    all_users = model.query.with_entities(model.user_id).distinct()
    s_rates = []
    for user in all_users:
        s_rate = get_user_success_rate(model, user.user_id)
        s_rates.append((user.user_id, s_rate))
    return s_rates


def get_user_total(model, user_id, attribute):
    total = (
        model.query.filter_by(user_id=user_id)
        .with_entities(func.sum(getattr(model, attribute)))
        .scalar()
    )
    return total if total is not None else 0


def get_all_users_totals(model, attribute):
    all_users = model.query.with_entities(model.user_id).distinct()
    totals = []
    for user in all_users:
        total = get_user_total(model, user.user_id, attribute)
        totals.append((user.user_id, total))
    return totals
