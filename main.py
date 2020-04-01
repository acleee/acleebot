from application import start_bot
from multiprocessing import Process
from config import CHATANGO_ROOMS


if __name__ == '__main__':
    processes = []
    for room in CHATANGO_ROOMS:
        p = Process(target=start_bot, args=(room,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
