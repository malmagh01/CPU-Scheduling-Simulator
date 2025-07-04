

'''Project Description:
You are required to produce program codes for preemptive scheduling that 
simulate the following algorithms: Round Robin (RR), Shortest-remaining-time-first- Preemptive, and Priority scheduling.

Program Input: The program should get inputs that describe the incoming process in term of:
- Number of Processers
- Arrival Time for each process
- CPU Burst Time for each process.
- Priority (if any) for each Process; (should be set to zero when non-applicable)
- Time quantum (q) in case of RR algorithm; (should be set to zero for other algorithms)
- The inputs of either arrival time and/or CPU burst time can be

specified in three methods:
a. Manually [Mandatory] 
b. Generated randomly with uniform distribution [Extra marks] 
c. Generated randomly with Gaussian distribution [Extra marks]

*Extra marks only apply when you select one method, either b or c.

Program Output: Upon processing the inputs of the scheduling algorithm and processes, the simulation program should:

draw the Gantt chart,
display the turnaround time for each process,
display the waiting time for each process,
and display the statistical results including the average waiting time and the average turnaround time for the group of input processes. 
Once the program extracts the above statistical results, you are required to evaluate and compare the results of the 
algorithms by selecting any two metrics of your choice. Note: do not forget to set q value for time quantum in case of RR algorithm. '''

# First we must import the necessary libraries

import numpy as np # provides support for arrays, matrices, and high-level mathematical functions
from numpy import random # used to generate random numbers
import copy # to ensure that there are copies of 'process' to avoiod errors and repetition

# Class to store process details 

# Class used to store process information to create objects that represents each process
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0 ):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        #time quantum is decided later

# Method for displaying average waiting time and average turnaround time

def display_results(processes, title):
    print(f"\n{title} Results:")

    num_of_processes = len(processes)

    print("\nProcess Details:")
    print("PID\tWaiting Time\tTurnaround Time\tPriority")
    for p in processes:
        print(f"{p.pid}\t{p.waiting_time}\t\t{p.turnaround_time}\t\t{p.priority}")

    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    average_waiting_time = total_waiting_time / num_of_processes
    average_turnaround_time = total_turnaround_time / num_of_processes

    print(f"Average Waiting Time: {average_waiting_time}")
    print(f"Average Turnaround Time: {average_turnaround_time}")

    return average_waiting_time, average_turnaround_time

# RR
def RR(processes, quantum):
    time = 0  # Current time
    queue = []  # Process queue
    gantt_data = []  # For Gantt chart

    # Sort by arrival time
    processes = sorted(processes, key=lambda x: x.arrival_time)

    completed_processes = []
    remaining_processes = processes[:]

    while remaining_processes or queue:
        # Add newly arrived processes to the queue
        while remaining_processes and remaining_processes[0].arrival_time <= time:
            queue.append(remaining_processes.pop(0))

        if queue:
            current_process = queue.pop(0)
            execution_time = min(quantum, current_process.remaining_time)
            gantt_data.append((current_process.pid, time, time + execution_time))
            time += execution_time
            current_process.remaining_time -= execution_time


            # Check if process is complete
            if current_process.remaining_time == 0:
                current_process.completion_time = time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed_processes.append(current_process)
            else:
                # Check for newly arrived processes after time advancement
                while remaining_processes and remaining_processes[0].arrival_time <= time:
                    queue.append(remaining_processes.pop(0))
                # Re-queue the current process
                queue.append(current_process)
        else:
            # Advance time if no process is ready
            time = remaining_processes[0].arrival_time

    gantt_chart(gantt_data)  # Print Gantt chart
    return completed_processes




# Shortest Remaining Time First algorithm (SRTF - Preemptive)
def srtf(processes):
    current_time = 0
    completed_processes = 0
    num_of_processes = len(processes)
    completed = []
    gantt_data = []  # List to store time data for each process

    while completed_processes < num_of_processes:

        # This part finds all processes that have arrived but still need time
        available_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        if available_processes:
            # Select the process with the shortest remaining time
            shortest = min(available_processes, key=lambda x: x.remaining_time)

            # Execute this process for one time unit
            shortest.remaining_time -= 1
            current_time += 1

            # Log the process in the Gantt chart
            gantt_data.append((shortest.pid, current_time - 1, current_time))

            # If this process is now complete
            if shortest.remaining_time == 0:
                shortest.completion_time = current_time
                shortest.turnaround_time = shortest.completion_time - shortest.arrival_time
                shortest.waiting_time = shortest.turnaround_time - shortest.burst_time
                completed.append(shortest)
                completed_processes += 1
        else:
            # If no process is available, increment the time
            current_time += 1
    gantt_chart(gantt_data)  # Print the Gantt chart
    return completed


# Priority Scheduling Algorithm
def priority_scheduling(processes):
    current_time = 0
    num_processes = len(processes)
    remaining_time = [p.burst_time for p in processes]
    completed_processes = 0
    gantt_data = []  # List to store time data for each process

    while completed_processes < num_processes:

        # Get all processes that have arrived and are not yet complete
        available_processes = [p for i, p in enumerate(processes) if p.arrival_time <= current_time and remaining_time[i] > 0]

        if available_processes:

            # Select the process with the highest priority (lowest priority number)
            highest_priority_process = min(available_processes, key=lambda x: (x.priority, x.arrival_time))
            idx = processes.index(highest_priority_process)

            # Execute the process for one unit of time
            remaining_time[idx] -= 1
            current_time += 1

            # Log the process in the Gantt chart
            gantt_data.append((highest_priority_process.pid, current_time - 1, current_time))

            # If the process is complete, finalize its times
            if remaining_time[idx] == 0:
                 highest_priority_process.completion_time = current_time
                 highest_priority_process.turnaround_time = highest_priority_process.completion_time - highest_priority_process.arrival_time
                 highest_priority_process.waiting_time = highest_priority_process.turnaround_time - highest_priority_process.burst_time
                 completed_processes += 1
        else:
            # If no process is available, increment the time
            current_time += 1

    gantt_chart(gantt_data)  # Print the Gantt chart
    return processes

# Method to compare between each method 

def compare(RR, SRTF , Priority):

  print("\nComparison of Algorithms:")
  print("Algorithm\tAverage Waiting Time\tAverage Turnaround Time")
  print(f"RR\t\t{RR[0]}\t\t\t{RR[1]}")
  print(f"SRTF\t\t{SRTF[0]}\t\t\t{SRTF[1]}")
  print(f"Priority\t{Priority[0]}\t\t\t{Priority[1]}")

  if RR[0] < SRTF[0] and RR[0] < Priority[0]:
    print("Round Robin has the best average waiting time ")
  elif SRTF[0] < RR[0] and SRTF[0] < Priority[0]:
    print("SRTF has the best average waiting time")
  else:
    print("Priority Scheduling has the best average waiting time")

  if RR[1] < SRTF[1] and RR[1] < Priority[1]:
    print("Round Robin has the best average turnaround time")
  elif SRTF[1] < RR[1] and SRTF[1] < Priority[1]:
    print("SRTF has the best average turnaround time")
  else:
    print("Priority Scheduling has the best average turnaround time")

# Print process details

def print_processes(processes):
    print("\nProcess Details:")
    print("PID\tArrival Time\tBurst Time\tPriority")
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t\t{p.burst_time}\t\t{p.priority}")

# Display Gantt chart

def gantt_chart(arr_gantt):

    print("\n\n ----------------------Gantt Chart--------------------------")
    optimized_gantt = []
    previous_process = None
    start_time = None

    for process in arr_gantt:
        pid, start, end = process

        if previous_process == pid:
            continue  # If the current process is the same as the previous one, skip it
        else:
            if previous_process is not None:
                optimized_gantt.append((previous_process, start_time, start))  # Add the previous process's time span
            start_time = start
            previous_process = pid

    # Add the last remaining process to the chart
    if previous_process is not None:
        optimized_gantt.append((previous_process, start_time, arr_gantt[-1][2]))

    # Print the chart with clear separators between processes
    print("\n" + "-" * (len(optimized_gantt) * 16 + 1))
    print("||", end="")
    for i in range(len(optimized_gantt)):
        print(f"\tp{optimized_gantt[i][0]}\t |", end="")

    print("|")
    print("-" * (len(optimized_gantt) * 16 + 1))


    print(0, end="")
    for i in range(len(optimized_gantt)):
        print(f"\t\t{optimized_gantt[i][2]}", end="")
    print()

# Main

def main():
    print("Welcome to the Scheduling Simulator!")
    num_of_processes = int(input("Enter the number of processes: "))

    processes = []

    for i in range(num_of_processes):

        print("------------------------------------------------")
        pid = i + 1
        print(f"\nEnter details for Process {pid}:")

        # Arrival Time Input
        print("Choose how to set the arrival time:")
        print("a) Manually")
        print("b) Randomly by uniform distribution")
        print("c) Randomly by Gaussian distribution")
        arrival_choice = input("Enter choice (a/b/c): ").strip().lower()

        if arrival_choice == 'a':
            arrival_time = int(input(f"Arrival time for Process {pid}: "))
        elif arrival_choice == 'b':
            arrival_time = int(random.uniform(0, 10))
            print("arrival time is " + str(arrival_time))
        elif arrival_choice == 'c':
            arrival_time = abs(int(random.normal(5, 2)))  # Mean=5, StdDev=2
            print("arrival time is " + str(arrival_time))
        else:
            print("Invalid choice! Setting arrival time to 0 by default.")
            arrival_time = 0

        # Burst Time Input
        print("Choose how to set the burst time:")
        print("a) Manually")
        print("b) Randomly by uniform distribution")
        print("c) Randomly by Gaussian distribution")
        burst_choice = input("Enter choice (a/b/c): ").strip().lower()

        if burst_choice == 'a':
            burst_time = int(input(f"Burst time for Process {pid}: "))
        elif burst_choice == 'b':
            burst_time = int(random.uniform(1, 10))
            print("burst time is " + str(burst_time))
        elif burst_choice == 'c':
            burst_time = abs(int(random.normal(6, 1)))  # Mean=6, StdDev=1
            print("burst time is " + str(burst_time))
        else:
            print("Invalid choice! Setting burst time to 1 by default.")
            burst_time = 1

        print("Enter priority of process, or 0 by default: ")
        priority = int(input(f"priority of Process {pid}: "))

        # Append the process to the list inside the loop
        processes.append(Process(pid, arrival_time, burst_time, priority))


    print_processes(processes)

    q_time = int(input("Enter the quantum time for Round Robin algorithm: "))

    # Run RR algorithm
    rr_processes = copy.deepcopy(processes)
    rr_results = RR(rr_processes, q_time)
    rr_avg_waiting_time, rr_avg_turnaround_time = display_results(rr_results, "Round Robin")

    # Run SRTF algorithm
    srtf_processes = copy.deepcopy(processes)
    srtf_results = srtf(srtf_processes)
    srtf_avg_waiting_time, srtf_avg_turnaround_time = display_results(srtf_results, "SRTF")

    # Run Priority Scheduling algorithm
    priority_processes = copy.deepcopy(processes)
    priority_results = priority_scheduling(priority_processes)
    priority_avg_waiting_time, priority_avg_turnaround_time = display_results(priority_results, "Priority Scheduling")

    # compare(rr, srtf, priority)
    compare((rr_avg_waiting_time, rr_avg_turnaround_time),
            (srtf_avg_waiting_time, srtf_avg_turnaround_time),
            (priority_avg_waiting_time, priority_avg_turnaround_time))


if __name__ == "__main__":
    main()