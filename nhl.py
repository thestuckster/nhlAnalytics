import pandas
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.plotting import ColumnDataSource


def main():

    nhl_df = pandas.read_csv("NHL2017.csv")

    print(nhl_df.query("Age > 40").to_string())

    build_position_chart(nhl_df)
    build_average_points_per_age_bracket_chart(nhl_df)
    build_average_points_per_age(nhl_df)

def build_position_chart(df):

    centers = df.query('Pos == "C"')
    left_wing = df.query('Pos == "LW"')
    right_wing = df.query('Pos == "RW"')
    defense_men = df.query('Pos == "D"')
    others = df.query('Pos != "C" & Pos != "LW" & Pos != "RW" & Pos != "D"')

    x_range = ['D', 'C', 'LW', 'RW', 'Multiple']
    p = figure(x_range=x_range, title="NHL Positions 2017")
    p.vbar(x=['C'], top=[len(centers.index)], width=.7, color='#003f5c')
    p.vbar(x=['LW'], top=[len(left_wing.index)], width=.7, color='#58508d')
    p.vbar(x=['RW'], top=[len(right_wing.index)], width=.7, color='#bc5090')
    p.vbar(x=['D'], top=[len(defense_men.index)], width=.7, color='#ff6361')
    p.vbar(x=['Multiple'], top=[len(others.index)], width=.7, color='#ffa600')
    output_file("nhl2017.html")
    show(p)


def build_average_points_per_age_bracket_chart(df):

    points = 'PTS'

    lower = df.query('Age <= 25')
    middle = df.query('Age >= 26 & Age <= 35')
    older = df.query('Age >= 36')

    lower_average = lower[points].sum() / len(lower.index)
    middle_average = middle[points].sum() / len(middle.index)
    older_average = older[points].sum() / len(older.index)

    x_range = ['Age <= 25', 'Age >= 26 & Age <= 35', 'Age >= 36']
    p = figure(x_range=x_range, y_range=(0, older_average + 3), title="Average points per age bracket, 2017")
    p.vbar(x=['Age <= 25'], top=lower_average, width=.8, color='#003f5c')
    p.vbar(x=['Age >= 26 & Age <= 35'], top=middle_average, width=.8, color='#bc5090')
    p.vbar(x=['Age >= 36'], top=older_average, width=.8, color='#ffa600')

    output_file("averagePointsPerBracket2017.html")
    show(p)


def build_average_points_per_age(df):

    df.fillna(0)
    max = df['Age'].max()
    min = df['Age'].min()

    print("Max: %s. Min: %s" % (max, min))

    age = []
    avg = []
    for x in range(min, max+1):
        age_df = df.query("Age == " + str(x))

        sum = age_df['PTS'].sum()
        if sum > 0:
            age.append(x)
            avg.append(sum / len(age_df.index))


    source = ColumnDataSource(data=dict(age=age, avg=avg))

    output_file("averagePointsPerAge2017.html")
    p = figure(title="Average Points Per Age, 2017")
    # p.line(age, avg, line_width=5)
    p.line(x='age', y='avg', line_width=4, source=source, color="#003f5c")
    p.circle(x='age', y='avg', line_width=5, source=source, color="#bc5090")

    show(p)


if __name__ == "__main__":
    main()
else:
    print("This is not a library!")
