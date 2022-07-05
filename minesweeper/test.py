def main():
    knowledge=[
        {(2, 1), (2, 2), (2, 0)},
        {(6, 2), (6, 0), (6, 1)},
        {(2, 0), (2, 1)},
    ]
    for i in range(len(knowledge)):
            for j in range(len(knowledge)):
                if knowledge[i] == knowledge[j]:
                    continue
                if knowledge[i].issuperset(knowledge[j]):
                    new_cells = knowledge[i] - knowledge[j]
                    knowledge[i] = new_cells
                    continue
                if knowledge[j].issuperset(knowledge[i]):
                    new_cells = knowledge[j] - knowledge[i]
                    knowledge[j] = new_cells
                    continue
    print(knowledge)
main()