import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

bme280_log_file = 'bme280.csv'
bme280_log_file_header = ['ID', 'Timestamp', 'Temperature °C', 'Pressure hPa', 'Humidity % rh']
adxl34x_log_file = 'adxl34x.csv'
adxl34x_log_file_header = ['Timestamp', 'x', 'y', 'z']
rm3100_log_file = 'rm3100.csv'
rm3100_log_file_header = ["Timestamp", "x", "y", "z", "rx", "ry", "rz"]
mcp3422_log_file = 'mcp3422.csv'
mcp3422_log_file_header = ["Timestamp", "Channel 1", "Channel 2", "Puck Face Temperature"]
plot_last_n_rows = 20
interval = 30 * 1000

# Create figure for plotting
fig_num_temp = 1
fig_temp = plt.figure(fig_num_temp)
ax_temp = fig_temp.add_subplot(1, 1, 1)

fig_num_press = 2
fig_press = plt.figure(fig_num_press)
ax_press = fig_press.add_subplot(1, 1, 1)

fig_num_hum = 3
fig_hum = plt.figure(fig_num_hum)
ax_hum = fig_hum.add_subplot(1, 1, 1)

fig_num_acc = 4
fig_acc = plt.figure(fig_num_acc)
ax_acc = fig_acc.add_subplot(1, 1, 1)

fig_num_heading = 5
fig_heading = plt.figure(fig_num_heading)
ax_heading = fig_heading.add_subplot(1, 1, 1)

fig_num_temp_sensors = 6
fig_temp_sensors = plt.figure(fig_num_temp_sensors)
ax_temp_sensors = fig_temp_sensors.add_subplot(1, 1, 1)

# This function is called periodically from FuncAnimation
def animate_bme280(i, fig_num, ax, header):

    bme280_data = pd.read_csv(bme280_log_file, header=0, names=bme280_log_file_header).tail(plot_last_n_rows)

    # Draw x and y lists
    ax.clear()
    ax.plot(
        bme280_data[bme280_log_file_header[1]],
        bme280_data[bme280_log_file_header[header]].astype('float64'))
    plt.figure(fig_num)
    plt.xticks(rotation=45, ha='right')
    plt.title('BME280 - ' + bme280_log_file_header[header] + ' Over Time')
    plt.ylabel(bme280_log_file_header[header])
    plt.tight_layout()

def animate_adxl34x(i, fig_num, ax):

    adxl34x_data = pd.read_csv(adxl34x_log_file, header=0, names=adxl34x_log_file_header).dropna().tail(plot_last_n_rows)

    # Draw x and y lists
    ax.clear()
    ax.plot(
        adxl34x_data[adxl34x_log_file_header[0]],
        adxl34x_data[adxl34x_log_file_header[1]],
        label='x')
    ax.plot(
        adxl34x_data[adxl34x_log_file_header[0]],
        adxl34x_data[adxl34x_log_file_header[2]],
        label='y')
    ax.plot(
        adxl34x_data[adxl34x_log_file_header[0]],
        adxl34x_data[adxl34x_log_file_header[3]],
        label='z')
    ax.legend()
    plt.figure(fig_num)
    plt.xticks(rotation=45, ha='right')
    plt.title('ADXL34x - Accelerometer Over Time')
    plt.ylabel('m/s^2')
    plt.tight_layout()

def animate_rm3100_heading(i, fig_num, ax):

    rm3100_data = pd.read_csv(rm3100_log_file, header=0, names=rm3100_log_file_header).dropna().tail(plot_last_n_rows)

    # Draw x and y lists
    ax.clear()
    ax.plot(
        rm3100_data[rm3100_log_file_header[0]],
        rm3100_data[rm3100_log_file_header[1]],
        label='x')
    ax.plot(
        rm3100_data[rm3100_log_file_header[0]],
        rm3100_data[rm3100_log_file_header[2]],
        label='y')
    ax.plot(
        rm3100_data[rm3100_log_file_header[0]],
        rm3100_data[rm3100_log_file_header[3]],
        label='z')
    ax.legend()
    plt.figure(fig_num)
    plt.xticks(rotation=45, ha='right')
    plt.title('RM3100 - Heading Over Time')
    plt.ylabel('uT')
    plt.tight_layout()

def animate_mcp3422(i, fig_num, ax):

    mcp3422_data = pd.read_csv(mcp3422_log_file, header=0, names=mcp3422_log_file_header).dropna().tail(plot_last_n_rows)

    # Draw x and y lists
    ax.clear()
    ax.plot(
        mcp3422_data[mcp3422_log_file_header[0]],
        mcp3422_data[mcp3422_log_file_header[3]])
    # ax.plot(
    #     mcp3422_data[mcp3422_log_file_header[0]],
    #     mcp3422_data[mcp3422_log_file_header[2]],
    #     label='Channel 2')
    ax.legend()
    plt.figure(fig_num)
    plt.xticks(rotation=45, ha='right')
    plt.title('Puck Face Temperature')
    plt.ylabel('Temp (deg C)')
    plt.tight_layout()

# Set up plot to call animate() function periodically
ani_temp = animation.FuncAnimation(fig_temp, animate_bme280, fargs=(fig_num_temp, ax_temp, 2), interval=interval)
ani_press = animation.FuncAnimation(fig_press, animate_bme280, fargs=(fig_num_press, ax_press, 3), interval=interval)
ani_hum = animation.FuncAnimation(fig_hum, animate_bme280, fargs=(fig_num_hum, ax_hum, 4), interval=interval)
ani_acc = animation.FuncAnimation(fig_acc, animate_adxl34x, fargs=(fig_num_acc, ax_acc), interval=interval)
ani_heading = animation.FuncAnimation(fig_heading, animate_rm3100_heading, fargs=(fig_num_heading, ax_heading), interval=interval)
ani_temp_sensors = animation.FuncAnimation(fig_temp_sensors, animate_mcp3422, fargs=(fig_num_temp_sensors, ax_temp_sensors), interval=interval)

plt.show()
