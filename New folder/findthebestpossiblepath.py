# a sample graph
graph = {'USD': ['BTC', 'LTC', 'PPC', 'EUR', 'RUR', 'NVC'],
         'BTC': ['RUR', 'USD', 'EUR', 'LTC', 'NMC', 'NVC', 'TRC', 'PPC', 'FTC', 'XPM'],
         'RUR': ['BTC', 'LTC', 'USD', 'EUR'],
         'EUR': ['BTC', 'LTC', 'USD', 'RUR'],
         'LTC': ['BTC', 'USD', 'RUR', 'EUR'],
         'NMC': ['BTC', 'USD'],
         'NVC': ['BTC', 'USD'],
         'TRC': ['BTC'],
         'PPC': ['BTC', 'USD'],
         'FTC': ['BTC'],
         'XPM': ['BTC']}


class MyQUEUE:  # just an implementation of a queue

    def __init__(self):
        self.holder = []

    def enqueue(self, val):
        self.holder.append(val)

    def dequeue(self):
        val = None
        try:
            val = self.holder[0]
            if len(self.holder) == 1:
                self.holder = []
            else:
                self.holder = self.holder[1:]
        except:
            pass

        return val

    def IsEmpty(self):
        result = False
        if len(self.holder) == 0:
            result = True
        return result


path_queue = MyQUEUE()  # now we make a queue


def BFS(graph, start, end, q):
    temp_path = [start]

    q.enqueue(temp_path)

    while q.IsEmpty() == False:
        tmp_path = q.dequeue()
        last_node = tmp_path[len(tmp_path) - 1]
        # print tmp_path
        if last_node == end:
            print "VALID_PATH : ", tmp_path
        for link_node in graph[last_node]:
            if link_node not in tmp_path:
                #new_path = []
                new_path = tmp_path + [link_node]
                q.enqueue(new_path)


BFS(graph, "USD", "NVC", path_queue)
