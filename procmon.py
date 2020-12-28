import streamlit as st
import pandas as pd
import psutil
import time

st.title("Procmon")


stats = { 
    "🧭 Load avg": psutil.getloadavg(),
    "🔋 Battery": 
}
try:
    stats["🔋 Battery"] = psutil.sensors_battery()
except Exception as e:
    st.warning("Could not get battery data from psutil")
    st.exception(e)

for stat_name, stat in stats.items():
    st.header(stat_name)
    st.write(stat)


st.header("Processes")

def build_dataframe():
    procs = [proc.info for proc in psutil.process_iter(['name', 'pid', 'memory_percent', 'cpu_percent'])]
    df = pd.DataFrame(procs)
    df.set_index('name', inplace=True)
    return df

processes = build_dataframe()
st.write(processes)

st.header("Top 10 memory hogs")
st.bar_chart(processes.sort_values('memory_percent', ascending=False)[0:11]['memory_percent'])

st.header("Top 10 cpu hogs")
st.bar_chart(processes.sort_values('cpu_percent', ascending=False)[0:11]['cpu_percent'])
