from mesa.batchrunner import BatchRunner
from plane import PlaneModel
from statistics import mean
import matplotlib.pyplot as plt
import collections
import numpy as np
import seaborn as sns
import pandas as pd
import math

bins = np.linspace(150, 1100, 100)

method_types = [
    'Random',
    'Front-to-back',
    # 'Front-to-back (4 groups)',
    'Back-to-front',
    # 'Back-to-front (4 groups)',
    'Window-Middle-Aisle',
    # 'Steffen Perfect',
    # 'Steffen Modified'
]
colors = ["blue", "red", "purple", "yellow",
          "green", "cyan", "gold", "magenta"]
plot_design = []

for i in method_types:
    fixed_params = {"method": i}
    batch_run = BatchRunner(PlaneModel, None, fixed_params, iterations=1000,
                            model_reporters={"method_time": lambda m: m.schedule.time}, display_progress=False, max_steps=1500)
    batch_run.run_all()
    all_times = (batch_run.get_model_vars_dataframe()['method_time'])
    c_times = collections.Counter(all_times)
    common = sorted(c_times.elements())
    plot_design.append(common)
    average_time = mean(batch_run.get_model_vars_dataframe()['method_time'])
    variance_time = np.var(batch_run.get_model_vars_dataframe()['method_time'])
    sd = 1.5*(math.sqrt(variance_time))
    print("{} - Mean: {}, Variance: {}".format(i, average_time, variance_time))
    df = pd.DataFrame(batch_run.get_model_vars_dataframe()['method_time'])
    # try:
    #     df_worstcase = df[df['method_time'] >= average_time + sd]
    #     average_time_worsecase = mean(df_worstcase['method_time'])
    # except:
    #     # df_sorted = df.sort_values(by='method_time',ascending=False)
    n = int(len(df['method_time']) * 0.05 )
    df_worstcase = df.nlargest(n,'method_time')
    average_time_worsecase = mean(df_worstcase['method_time'])
    print("{} (Worse Case) - Mean: {}".format(i, average_time_worsecase))

    
    


df = pd.read_csv(
    'https://raw.githubusercontent.com/selva86/datasets/master/diamonds.csv')
kwargs = dict(hist_kws={'alpha': .4}, kde_kws={'linewidth': 2})

for j in range(len(plot_design)):
    a = np.asarray(plot_design[j])
    #x1 = df.loc[df.cut == "Good", "depth"]
    #plt.hist(a, bins, alpha=0.3, color=colors[j])
    sns.distplot(a, color=colors[j],
                 label=plot_design[j], **kwargs, hist=False)


plt.legend(['Random',
            'Front to back',
            # 'Front to back (4 groups)',
            'Back to front',
            # 'Back to front (4 groups)',
            'Window-Middle-Aisle',
            # 'Steffen Perfect',
            # 'Steffen Modified'
            ]
           )
plt.xlabel('Time')
plt.ylabel('Density')
plt.show()

plt.clf()
plt.close()

new_params1 = [{"method": method_types[0], "shuffle_enable": True, 'common_bags': 0},
               {"method": method_types[0],
                   "shuffle_enable": False, 'common_bags': 1},
               {"method": method_types[0],
                   "shuffle_enable": False, 'common_bags': 2},
               {"method": method_types[0],
                   "shuffle_enable": False, 'common_bags': 3},
               {"method": method_types[0], "shuffle_enable": False, 'common_bags': 4}]

new_params2 = [{"method": method_types[4], "shuffle_enable": True, 'common_bags': 0},
               {"method": method_types[4],
                   "shuffle_enable": False, 'common_bags': 1},
               {"method": method_types[4],
                   "shuffle_enable": False, 'common_bags': 2},
               {"method": method_types[4],
                   "shuffle_enable": False, 'common_bags': 3},
               {"method": method_types[4], "shuffle_enable": False, 'common_bags': 4}]

bins = np.linspace(100, 500, 100)

fig, axes = plt.subplots(1, 5, figsize=(15, 3), dpi=100, sharey=True)

# RANDOM
for j in range(len(new_params1)):
    batch_run = BatchRunner(PlaneModel, None, new_params1[j], iterations=50,
                            model_reporters={"method_time": lambda m: m.schedule.time}, display_progress=False,
                            max_steps=1500)
    batch_run.run_all()
    all_times = (batch_run.get_model_vars_dataframe()['method_time'])
    c_times = collections.Counter(all_times)
    common = sorted(c_times.elements())
    a = np.asarray(common)
    average_time = mean(batch_run.get_model_vars_dataframe()['method_time'])
    if j == 0:
        label_name = "SHUFFLE ONLY" + " " + \
            "avg. time:" + " " + str(average_time)
    else:
        label_name = "BAG SIZE:" + " " + \
            str(j) + " " + "avg. time:" + " "+str(average_time)
    sns.distplot(a, color=colors[j], ax=axes[j],
                 label="Density", axlabel=label_name, hist=False)


plt.show()
plt.clf()
plt.close()

fig, axes = plt.subplots(1, 5, figsize=(15, 3), dpi=100, sharey=True)
# BACK TO FRONT (4 GROUPS)
for j in range(len(new_params2)):
    batch_run = BatchRunner(PlaneModel, None, new_params2[j], iterations=50,
                            model_reporters={"method_time": lambda m: m.schedule.time}, display_progress=False,
                            max_steps=1500)
    batch_run.run_all()
    all_times = (batch_run.get_model_vars_dataframe()['method_time'])
    c_times = collections.Counter(all_times)
    common = sorted(c_times.elements())
    a = np.asarray(common)
    average_time = mean(batch_run.get_model_vars_dataframe()['method_time'])
    if j == 0:
        label_name = "SHUFFLE ONLY" + " " + \
            "avg. time:" + " " + str(average_time)
    else:
        label_name = "BAG SIZE:" + " " + \
            str(j) + " " + "avg. time:" + " " + str(average_time)
    sns.distplot(a, color=colors[j], ax=axes[j],
                 label="Density", axlabel=label_name, hist=False)
plt.show()
