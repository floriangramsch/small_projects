import matplotlib.pyplot as plt

from Nim_Variation import Nim_Variation

interest = []

streichhoelzer_a = 87
streichhoelzer_b = 87
for gen in range(streichhoelzer_a, streichhoelzer_b+1):
    results = []
    generations = 10000

    n = gen

    for i in range(generations):
        nim = Nim_Variation(n, "CPU1", "CPU2", True, True)
        # n, name1, name2, isname1cpu?, isname2cpu?
        while not nim.win:
            if nim.a_turn:
                if nim.cpu_a: nim.cpu_one_or_four()
                else: nim.one_or_four()
            elif nim.b_turn:
                if nim.cpu_b: nim.cpu_one_or_four()
                else: nim.one_or_four()
            result = nim.update()
        results.append(result)

    win_counter = [0, 0]
    rounds_counter = {}
    for i in results:
        if i[0] == "CPU1":
            win_counter[0] += 1
        elif i[0] == "CPU2":
            win_counter[1] += 1
        if i[1] in rounds_counter:
            rounds_counter[i[1]] += 1
        else:
            rounds_counter[i[1]] = 1


    # Data for plotting
    data = [0 for i in range(n+1)]
    for i in rounds_counter.keys():
        data[i] = rounds_counter[i]
    print(data)
    interest.append([gen, len(data) - data.count(0)])

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.canvas.set_window_title(f'Generation {gen}')
    ax1.plot(data, 'o-')

    ax1.set(xlabel='Rounds', ylabel='Count',
        title='Round Duration')
    ax1.grid()

    ax2.plot(win_counter, 'p')
    ax2.set(xlabel='Player', ylabel='Winnings',
            title='Player Wins')

    # fig.savefig(f"{gen}.png")
    plt.show()
    plt.close(fig)

print(interest)