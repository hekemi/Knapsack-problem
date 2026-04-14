def stick_n_rope(Lst, w):  # Основная функция: принимает список предметов и вместимость рюкзака.
    cLst = Lst.copy()  # Делаем копию входного списка, чтобы не менять исходные данные.
    
    cooked_list = []  # Здесь будет список пар (предмет, отношение цена/вес).

    for item in cLst:  # Проходим по каждому предмету из копии списка.
        ratio = float("inf") if item["weight"] == 0 else item["price"] / item["weight"]  # Считаем отношение цена/вес (для нулевого веса — бесконечность).
        cooked_list.append((item, ratio))  # Добавляем кортеж (сам предмет, его отношение цена/вес).
    
    cooked_list.sort(key=lambda x: x[1], reverse=True)  # Сортируем по убыванию отношения цена/вес (для верхней оценки).
    
    items = [pair[0] for pair in cooked_list]  # Получаем отсортированный список только предметов.
    n = len(items)  # Запоминаем количество предметов.

    def upper_bound(level, current_weight, current_price):  # Вспомогательная функция верхней границы (optimistic bound).
        if current_weight > w:  # Если уже превысили вместимость,
            return 0  # то такая ветка не может дать полезного решения.

        bound = current_price  # Начинаем верхнюю оценку с уже набранной стоимости.
        total_weight = current_weight  # И с уже набранного веса.
        i = level  # Начинаем добор с текущего уровня дерева решений.

        while i < n and total_weight + items[i]["weight"] <= w:  # Пока можем брать предметы целиком,
            total_weight += items[i]["weight"]  # добавляем их вес,
            bound += items[i]["price"]  # и добавляем их стоимость к оценке,
            i += 1  # переходим к следующему предмету.

        if i < n:  # Если еще остался предмет, который не помещается целиком,
            remain = w - total_weight  # считаем оставшийся объем.
            wi = items[i]["weight"]  # Берем вес текущего предмета.
            pi = items[i]["price"]  # Берем цену текущего предмета.
            if wi == 0:  # Если его вес нулевой,
                bound += pi  # добавляем цену целиком (без увеличения веса).
            else:  # Иначе
                bound += pi * (remain / wi)  # добавляем дробную часть (как в fractional knapsack) для оптимистичной оценки.

        return bound  # Возвращаем верхнюю границу для ветки.

    best_price = 0  # Лучшая найденная стоимость.
    best_weight = 0  # Вес у лучшего найденного набора.
    best_taken = []  # Индексы взятых предметов у лучшего решения.

    stack = [(0, 0, 0, [])]  # Стек DFS: (уровень, текущий вес, текущая стоимость, взятые индексы).

    while stack:  # Пока есть непроверенные состояния,
        level, curr_w, curr_p, taken = stack.pop()  # достаем очередное состояние.

        if level == n:  # Если дошли до конца списка предметов,
            if curr_p > best_price:  # и нашли решение лучше текущего лучшего,
                best_price = curr_p  # обновляем лучшую стоимость,
                best_weight = curr_w  # обновляем вес лучшего решения,
                best_taken = taken  # обновляем набор взятых предметов.
            continue  # Переходим к следующему состоянию из стека.

        if upper_bound(level, curr_w, curr_p) <= best_price:  # Если даже оптимистичная оценка не лучше текущего лучшего,
            continue  # отсекаем ветку (branch and bound pruning).

        item = items[level]  # Берем предмет текущего уровня.
        iw = item["weight"]  # Его вес.
        ip = item["price"]  # Его стоимость.

        stack.append((level + 1, curr_w, curr_p, taken))  # Ветка "не брать текущий предмет".

        if curr_w + iw <= w:  # Если предмет помещается,
            stack.append((level + 1, curr_w + iw, curr_p + ip, taken + [level]))  # добавляем ветку "взять предмет".

    rLts = [items[i] for i in best_taken]  # Собираем итоговый список выбранных предметов.
    v = w - best_weight  # Считаем оставшийся объем рюкзака.
    cost = best_price  # Итоговая стоимость выбранных предметов.

    return rLts, v, cost  # Возвращаем: выбранные предметы, оставшийся объем, общую стоимость.