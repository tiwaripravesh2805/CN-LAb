import matplotlib.pyplot as plt
import random

def tcp_congestion_control(rounds=20, loss_prob=0.2):
    cwnd = 1
    ssthresh = 8
    cwnd_values = []

    for r in range(rounds):
        if random.random() < loss_prob:
            print(f"Packet loss at round {r+1}, cwnd={cwnd} → multiplicative decrease")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1
        else:
            if cwnd < ssthresh:
                cwnd *= 2  # Slow Start
            else:
                cwnd += 1  # Congestion Avoidance
        cwnd_values.append(cwnd)

    # Plot cwnd growth
    plt.plot(range(1, rounds + 1), cwnd_values, marker='o')
    plt.title("TCP Congestion Control Simulation")
    plt.xlabel("Transmission Round")
    plt.ylabel("Congestion Window (cwnd)")
    plt.grid(True)
    plt.show()

tcp_congestion_control()
