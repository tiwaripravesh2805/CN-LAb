import random
import time

def go_back_n_arq(total_frames=10, window_size=4, loss_prob=0.2):
    base = 0
    while base < total_frames:
        end = min(base + window_size, total_frames)
        print(f"Sending frames {list(range(base, end))}")

        # Simulate random frame loss
        lost_frame = None
        for i in range(base, end):
            if random.random() < loss_prob:
                lost_frame = i
                print(f"Frame {i} lost!")
                break

        if lost_frame is not None:
            print(f"Retransmitting frames {list(range(lost_frame, end))}")
            time.sleep(1)
        else:
            base = end
            print(f"ACK {base - 1} received, window slides to {base}\n")
            time.sleep(0.5)

go_back_n_arq()
