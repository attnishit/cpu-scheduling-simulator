# when imported as module.
from src.utils.tmp import processes
import src.utils.table as table
import src.utils.graph as graph


def run(processes):
    # expects array of processes as arguments -> run the scheduling -> returns a dictionary/object of the result.

    print('running srtf...')

    gantt = []  # (,())

    # initialize
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    total_return_time = 0

    n = len(processes)

    response = []
    for i in range(n):
        response.append(False)

    def findWaitingTime(processes, n):

        rt = [0] * n

        # Copy the burst time into rt[]
        for i in range(n):
            rt[i] = processes[i].burst_time
        complete = 0
        t = 0
        minm = 999999999
        short = 0
        check = False

        # Process until all processes gets
        # completed
        while (complete != n):
            # Find process with minimum remaining
            # time among the processes that
            # arrives till the current time`
            for j in range(n):
                if ((processes[j].arrival_time <= t) and
                        (rt[j] < minm) and rt[j] > 0):
                    minm = rt[j]
                    short = j
                    check = True
            if (check == False):
                t += 1
                continue
            else:
                if(response[short] == False):
                    response[short] = True
                    processes[short].response_time = t - \
                        processes[short].arrival_time

            # Reduce remaining time by one
            rt[short] -= 1

            # Update minimum
            minm = rt[short]
            if (minm == 0):
                minm = 999999999

            # If a process gets completely
            # executed
            if (rt[short] == 0):

                # Increment complete
                complete += 1
                check = False

                # Find finish time of current
                # process
                fint = t + 1

                # Calculate waiting time
                processes[short].waiting_time = (
                    fint - processes[short].arrival_time - processes[short].burst_time)

                if (processes[short].waiting_time < 0):
                    processes[short].waiting_time = 0

            # Increment time
            t += 1

    def findTurnAroundTime(processes, n):
        processes[0].waiting_time = 0
        for i in range(n):
            processes[i].turnaround_time = processes[i].burst_time + \
                processes[i].waiting_time

    # sort by arrival_time
    proc = sorted(processes, key=lambda proc: proc.arrival_time)

    # setting initial values

    findWaitingTime(proc, n)

    findTurnAroundTime(proc, n)

    for i in range(0, n):
        proc[i].return_time = proc[i].arrival_time + proc[i].turnaround_time

    # calculate for next processes
    for i in range(1, len(proc)):

        # update total
        total_response_time += proc[i].response_time
        total_waiting_time += proc[i].waiting_time
        total_turnaround_time += proc[i].turnaround_time
        total_return_time += proc[i].burst_time

    return {
        'name': 'SRTF',
        'avg_waiting_time': total_waiting_time/len(proc),
        'avg_response_time': total_response_time/len(proc),
        'avg_turnaround_time': total_turnaround_time/len(proc),
        'processes': proc,
        'gantt': gantt
    }


# If this file is executed directly -> run temporary test-cases
def main():
    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    print("Avg Turnaround Time: {}".format(result['avg_turnaround_time']))
    print("Avg Response Time: {}".format(result['avg_response_time']))
    table.plot(result['processes'])
    graph.plot_gantt(result['gantt'])


if __name__ == '__main__':
    main()
