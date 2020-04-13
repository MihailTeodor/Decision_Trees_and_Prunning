import matplotlib.pyplot as plt
from dataManager import*
from id3Tree import*
from id3Tree import _manage_prune



def elaborate(dataset, initial_error_rate, initial_examples_nr, number_of_iterations, light):
    k = initial_error_rate
    while k < 100:
        pre_med_nodes = []
        post_med_nodes = []
        pre_med_precision = []
        post_med_precision = []
        pre_med_depth = []
        post_med_depth = []
        data_length = []
        for i in range(0, number_of_iterations):
            iteration = True
            n = initial_examples_nr
            pre_nodes = []
            post_nodes = []
            pre_precision = []
            post_precision = []
            pre_depth = []
            post_depth = []
            data_length = []
            while iteration:
                grow_set, validation_set, test_set, attributes, iteration = manage_data(dataset, n, iteration, k)
                tree = ID3(grow_set, "boh")
                pre_cut_tree_nodes_num, pre_cut_tree_max_depth = get_tree_info(tree)
                pre_cut_precision = (test(tree, test_set) * 100)
                pre_cut_val_precision = test(tree, validation_set)
                if light:
                    tree, post_cut_val_precision, nr_pruned = manage_prune(tree, validation_set, grow_set)
                else:
                    tree, post_cut_val_precision, nr_pruned = _manage_prune(tree, validation_set, grow_set)
                post_cut_precision = test(tree, test_set) * 100
                post_cut_tree_nodes_num, post_cut_tree_max_depth = get_tree_info(tree)

                pre_nodes.append(pre_cut_tree_nodes_num)
                post_nodes.append(post_cut_tree_nodes_num)
                pre_precision.append(pre_cut_precision)
                post_precision.append(post_cut_precision)
                pre_depth.append(pre_cut_tree_max_depth)
                post_depth.append(post_cut_tree_max_depth)

                print("Pre-Prune precision on validation_set: " + str(
                    pre_cut_val_precision) + " and Post-Prune precision on same validation_set: " + str(
                    post_cut_val_precision))
                print("Pre-Prune precision on test_set: " + str(
                    pre_cut_precision) + " and Post-Prune precision on same test_set: " + str(post_cut_precision))
                print(str(nr_pruned) + " nodes were pruned")
                print("Pre-prune nodes num: " + str(pre_cut_tree_nodes_num) + " with depth: " + str(
                    pre_cut_tree_max_depth))
                print("Post-Prune nodes num: " + str(post_cut_tree_nodes_num) + " with depth: " + str(
                    post_cut_tree_max_depth))
                print(str(i) + "," + str(n))
                print(" ")
                data_length.append(n)
                n += 150

            if len(pre_med_nodes) == 0:
                for j in range(0, len(pre_nodes)):
                    pre_med_nodes.append(0)
                    pre_med_precision.append(0)
                    pre_med_depth.append(0)
                    post_med_nodes.append(0)
                    post_med_precision.append(0)
                    post_med_depth.append(0)

            for j in range(0, len(pre_nodes)):
                pre_med_nodes[j] += pre_nodes[j]
                pre_med_precision[j] += pre_precision[j]
                pre_med_depth[j] += pre_depth[j]
                post_med_nodes[j] += post_nodes[j]
                post_med_precision[j] += post_precision[j]
                post_med_depth[j] += post_depth[j]

        for m in range(0, len(pre_med_nodes)):
            pre_med_nodes[m] /= number_of_iterations
            pre_med_precision[m] /= number_of_iterations
            pre_med_depth[m] /= number_of_iterations
            post_med_nodes[m] /= number_of_iterations
            post_med_precision[m] /= number_of_iterations
            post_med_depth[m] /= number_of_iterations

        plt.plot(data_length, pre_med_nodes, label='pre-prunning')
        plt.plot(data_length, post_med_nodes, label='post-prunning')
        plt.title("Numero nodi prima e dopo (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Numero nodi")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        plt.plot(data_length, pre_med_precision, label='pre-prunning')
        plt.plot(data_length, post_med_precision, label='post-prunning')
        plt.title("Precisione sul test set (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Precisione")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        plt.plot(data_length, pre_med_depth, label='pre-prunning')
        plt.plot(data_length, post_med_depth, label='post-prunning')
        plt.title("Profondità alberi prima e dopo prunning (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Profondità")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        k += 25

def compare(dataset, initial_error_rate, initial_examples_nr, number_of_iterations):
    k = initial_error_rate
    while k < 100:
        pre_med_nodes = []
        post_med_nodes = []
        pre_med_precision = []
        post_med_precision = []
        pre_med_depth = []
        post_med_depth = []
        data_length = []

        post_or_med_nodes = []
        post_or_med_precision = []
        post_or_med_depth = []
        for i in range(0, number_of_iterations):
            iteration = True
            n = initial_examples_nr
            pre_nodes = []
            post_nodes = []
            pre_precision = []
            post_precision = []
            pre_depth = []
            post_depth = []
            data_length = []
            post_or_nodes = []
            post_or_precision = []
            post_or_depth = []
            while iteration:
                grow_set, validation_set, test_set, attributes, iteration = manage_data(dataset, n, iteration, k)
                tree = ID3(grow_set, "boh")
                pre_cut_tree_nodes_num, pre_cut_tree_max_depth = get_tree_info(tree)
                pre_cut_precision = (test(tree, test_set) * 100)
                pre_cut_val_precision = test(tree, validation_set)
                tree_backup = copy.deepcopy(tree)
                light_tree, post_cut_val_precision, nr_light_pruned = manage_prune(tree_backup, validation_set, grow_set)
                tree, post_cut_or_val_precision, nr_pruned = _manage_prune(tree, validation_set, grow_set)
                post_cut_light_tree_precision = test(light_tree, test_set) * 100
                post_cut_tree_precision = test(tree, test_set) * 100
                post_cut_tree_nodes_num, post_cut_tree_max_depth = get_tree_info(tree)
                post_cut_light_tree_nodes, post_cut_light_tree_max_depth = get_tree_info(light_tree)

                pre_nodes.append(pre_cut_tree_nodes_num)
                post_nodes.append(post_cut_light_tree_nodes)
                pre_precision.append(pre_cut_precision)
                post_precision.append(post_cut_light_tree_precision)
                pre_depth.append(pre_cut_tree_max_depth)
                post_depth.append(post_cut_light_tree_max_depth)

                post_or_nodes.append(post_cut_tree_nodes_num)
                post_or_precision.append(post_cut_tree_precision)
                post_or_depth.append(post_cut_tree_max_depth)

                print("Pre-Prune precision on validation_set: " + str(
                    pre_cut_val_precision) + " and Post-Prune precision on same validation_set (heavy-prunning): " + str(
                    post_cut_or_val_precision) + " and Post-Prune precision on validation_set (light-prunning): " + str(post_cut_val_precision))
                print("Pre-Prune precision on test_set: " + str(
                    pre_cut_precision) + " and Post-Prune precision on same test_set (heavy prunning) : " + str(post_cut_tree_precision) + " and (light prunning: " + str(post_cut_light_tree_precision))
                print("Pre-prune nodes num: " + str(pre_cut_tree_nodes_num) + " with depth: " + str(
                    pre_cut_tree_max_depth))
                print("Post-Prune (light prunning) nodes num: " + str(post_cut_light_tree_nodes) + " with depth: " + str(
                    post_cut_light_tree_max_depth))

                print("Post-Prune (heavy prunning) nodes num: " + str(post_cut_tree_nodes_num) + " with depth: " + str(
                    post_cut_tree_max_depth))
                print(str(i) + "," + str(n))
                print(" ")

                data_length.append(n)
                n += 100

            if len(pre_med_nodes) == 0:
                for j in range(0, len(pre_nodes)):
                    pre_med_nodes.append(0)
                    pre_med_precision.append(0)
                    pre_med_depth.append(0)

                    post_med_nodes.append(0)
                    post_med_precision.append(0)
                    post_med_depth.append(0)

                    post_or_med_nodes.append(0)
                    post_or_med_precision.append(0)
                    post_or_med_depth.append(0)

            for j in range(0, len(pre_nodes)):
                pre_med_nodes[j] += pre_nodes[j]
                pre_med_precision[j] += pre_precision[j]
                pre_med_depth[j] += pre_depth[j]

                post_med_nodes[j] += post_nodes[j]
                post_med_precision[j] += post_precision[j]
                post_med_depth[j] += post_depth[j]

                post_or_med_nodes[j] += post_or_nodes[j]
                post_or_med_precision[j] += post_or_precision[j]
                post_or_med_depth[j] += post_or_depth[j]

        for m in range(0, len(pre_med_nodes)):
            pre_med_nodes[m] /= number_of_iterations
            pre_med_precision[m] /= number_of_iterations
            pre_med_depth[m] /= number_of_iterations

            post_med_nodes[m] /= number_of_iterations
            post_med_precision[m] /= number_of_iterations
            post_med_depth[m] /= number_of_iterations

            post_or_med_nodes[m] /= number_of_iterations
            post_or_med_precision[m] /= number_of_iterations
            post_or_med_depth[m] /= number_of_iterations

        plt.plot(data_length, pre_med_nodes, label='pre-prunning')
        plt.plot(data_length, post_or_med_nodes, label='heavy-prunning')
        plt.plot(data_length, post_med_nodes, label='light-prunning')
        plt.title("Numero nodi dopo prunning (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Numero nodi")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        plt.plot(data_length, pre_med_precision, label='pre-prunning')
        plt.plot(data_length, post_or_med_precision, label='heavy-prunning')
        plt.plot(data_length, post_med_precision, label='light-prunning')
        plt.title("Precisione sul test set (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Precisione")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        plt.plot(data_length, pre_med_depth, label='pre-prunning')
        plt.plot(data_length, post_or_med_depth, label='heavy-prunning')
        plt.plot(data_length, post_med_depth, label='light-prunning')
        plt.title("Profondità alberi dopo prunning (rumore del " + str(k) + "%)")
        plt.xlabel("Numero esempi totali")
        plt.ylabel("Profondità")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        k += 25

def main(dataset):
    '''
    elaborate() function generates a decision tree based on file dataset and then pruns it plotting the results (True = light prunning; False = heavy prunning)
    compare() function compares the two implementations of prunning (light and heavy)
    parameters are (in order): dataset, initial_error_rate, initial_examples_nr, number_of_iterations, light
    '''
    #elaborate(dataset, 5, 50, 10, False)
    compare(dataset, 5, 50, 10)


main("tic-tac-toe")
