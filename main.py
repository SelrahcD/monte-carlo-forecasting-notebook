import pandas as pd
from matplotlib import pyplot as plt
import random

data = pd.read_csv(r'./throughput.csv')

df = pd.DataFrame(data)

print (df)

plt.interactive(False)

# df.plot(x='week', y='throughput')
# df.plot(kind='scatter', x='week', y='throughput')
#
# plt.show()

SIMULATION_ITEMS = 40


def simulate_weeks_for(expected_item_count, past_throughput_per_week):
    weeks = 0
    total = 0
    while total <= expected_item_count:
        total += past_throughput_per_week.sample(1).iloc[0]
        weeks += 1
    return weeks

samples = [simulate_weeks_for(expected_item_count=40, past_throughput_per_week=df['throughput']) for i in range(0, 1000)]

samples = pd.DataFrame(samples, columns=['Weeks'])

now = pd.to_datetime("today")
samples['estimated_completion_date'] = samples['Weeks'].apply(lambda w: now + pd.Timedelta(w, unit='W'))

print(samples)

# GOOD
# plt.rcParams["figure.autolayout"] = True
# plt.hist(samples.estimated_completion_date)
# plt.tick_params(rotation=45)
# plt.show()


distribution = samples.groupby(['estimated_completion_date']).size().reset_index(name='Frequency')

distribution['Cumsum'] = distribution['Frequency'].cumsum()
distribution['Probability'] = 100 * distribution['Cumsum'] / distribution['Frequency'].sum()

# print(distribution)

# plt.rcParams["figure.autolayout"] = True
# plt.bar(data=distribution, x='estimated_completion_date', height='Probability')
# plt.tick_params(rotation=45)
# plt.show()

# print(samples['estimated_completion_date'].quantile(0.95))
print(distribution)
# print(samples.quantile(.95))
                   # .quantile(0.95, axis='estimated_completion_date'))

