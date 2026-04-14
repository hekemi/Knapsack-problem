# Жадный алгоритм
def greedy_algo(Lst, w):
    # Создаем список с соотношением цена/вес
    grLst = Lst.copy()
    ###grLst = [{"index": item["index"], "multiwp": item["price"]/item["weight"]} for item in Lst]
    
    # Сортировка по цене/весу (убывание)
    grLst.sort(key=lambda x: x["price"]/x["weight"], reverse=True)
    ###grLst.sort(key=lambda x: x["multiwp"], reverse=True)
    rLst = []
    v = cost = 0
    for item in grLst:
        if item["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(item)
            v += item["weight"]
            cost += item["price"]
    return rLst, v, cost
    '''
    for item in grLst:
        if Lst[item["index"]]["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(Lst[item["index"]])
            v += Lst[item["index"]]["weight"]
            cost += Lst[item["index"]]["price"]
    return rLst, v, cost'''

# Метод ветвей и границ
# Класс для создания узлов
class Node:
    def __init__(self, level, price, weight, bound):
        self.level = level #уровень/индекс предмета
        self.price = price #суммарная стоимость предметов в этом узле
        self.weight = weight #суммарный вес предметов в этом узле
        self.bound = bound #максимальный потенциал ветки
    def __lt__(self, other): #сравнение параметров узлов bound 
        return self.bound > other.bound  #наибольший bound

# Функция создания хорошего прогноза
def get_bound(node, n, w, items):
    if node.weight >= w:
        return 0
    profit_bound   = node.value#хороший прогноз
    current_weight = node.weight#текущий вес
    j = node.level + 1

    # Жадно забираем самое ценное
    while j<n and current_weight+items[j]["weight"] <= w:
        current_weight += items[j]["weight"]
        profit_bound   += items[j]["price"]
        j += 1
    
    if j < n: #дополняем прогноз кусочком следующего по цена/вес
        profit_bound += (items[j]["price"]/items[j]["weight"])*(w-current_weight)
    return profit_bound

def branch_boundary_method(Lst, w):
    return 0

queue = [] #создаем список-очередь

# Создаем первый узел (корень)
root = Node(level=-1, value=0, weight=0)
root.bound = get_bound(root, n, w, items)
max_profit = 0
heapq.heappush(queue, root) #добавление в очередь queue узла root с учетом приоритета
while queue:
    current_node = heapq.heappop(queue) #достаем узел с самым большим bound
    # Если профит у узла меньше максимального, скипаем
    if current_node.bound <= max_profit: 
        continue
    next_level = current_node.level + 1
    # Проверка на то, что мы обработали все предметы
    if next_level >= len(items):
        continue

    item = items[next_level]

    # Берем предмет и проверяем, влезет ли он
    if current_node.weight + item["weight"] <= w:
        left_child = Node(
            level=next_level, 
            price=current_node.price + item["price"],
            weight=current_node.weight + item["weight"]
        )

        # Проверяем стала ли текущая стоимость выше рекордной
        if left_child.price > max_profit:
            max_profit = left_child.price