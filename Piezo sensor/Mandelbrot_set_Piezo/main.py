import queue
import threading

from calculation import calculate
from receive_data import receive_from_arduino
from render import Render


def receive_calculation(q, q2):
    while True:
        receive_thread = threading.Thread(target=receive_from_arduino, args=(q,))
        calculation_thread = threading.Thread(target=calculate, args=(q, q2))

        receive_thread.start()
        calculation_thread.start()

        receive_thread.join()
        calculation_thread.join()


if __name__ == "__main__":
    q = queue.Queue()
    q2 = queue.Queue()
    main_thread = threading.Thread(target=receive_calculation, args=(q, q2,))
    main_thread.start()
    Render().render(q2)
    main_thread.join()
