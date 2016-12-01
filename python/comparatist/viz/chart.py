import altair


def elapsed(df):
    chart = altair.Chart(df[df["try"] > 0])
    return chart.mark_point().encode(
        x=altair.X(
            'sim',
            axis=altair.Axis(
                title='model [lang] implementation')),
        y='elapsed',
    )
