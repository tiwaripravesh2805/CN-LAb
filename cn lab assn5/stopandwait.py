import random
import time

def stop_and_wait_arq(total_frames=5, loss_prob=0.3, timeout=2):
    current_frame = 0

    while current_frame < total_frames:
        print(f"Sending Frame {current_frame}")
        time.sleep(0.5)

        # Simulate random frame loss
        frame_lost = random.random() < loss_prob

        if not frame_lost:
            # ACK received successfully
            print(f"ACK {current_frame} received\n")
            current_frame += 1
            continue
        else:
            print(f"Frame {current_frame} lost")

        # Timeout and retransmission
        start_time = time.time()
        ack_received = False

        while not ack_received:
            if time.time() - start_time > timeout:
                print(f"Timeout! Retransmitting Frame {current_frame}")
                time.sleep(0.5)
                frame_lost = random.random() < loss_prob
                if not frame_lost:
                    print(f"ACK {current_frame} received\n")
                    current_frame += 1
                    ack_received = True
                else:
                    print(f"Frame {current_frame} lost again")
                    start_time = time.time()

    print("All frames transmitted and acknowledged successfully")
    
stop_and_wait_arq(total_frames=6, loss_prob=0.3, timeout=2)

