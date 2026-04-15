import heapq

# Жадный алгоритм
def greedy_algo(Lst, w):
    # Создаем список с соотношением цена/вес
    grLst = Lst.copy()
    
    # Сортировка по цене/весу (убывание)
    grLst.sort(key=lambda x: x["price"]/x["weight"], reverse=True)
    rLst = [] #результирующий список
    v = cost = 0 #вместимость и суммарная стоимость
    for item in grLst:
        if item["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(item)
            v += item["weight"]
            cost += item["price"]
    return rLst, v, cost

# Метод ветвей и границ
