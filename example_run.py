from utils import uniform_distribution, normal_distribution
from stick_n_rope import stick_n_rope


def print_result(title, items, capacity):
    # ...existing code...
    selected, remaining, total_cost = stick_n_rope(items, capacity)
    print(f"\n--- {title} ---")
    print(f"Вместимость рюкзака: {capacity:.3f}")
    print(f"Всего предметов: {len(items)}")
    print(f"Взято предметов: {len(selected)}")
    print(f"Оставшийся объем: {remaining:.3f}")
    print(f"Общая стоимость: {total_cost:.3f}")
    print("Выбранные предметы:")
    for it in selected:
        print(
            f"  index={it['index']}, weight={it['weight']:.3f}, price={it['price']:.3f}"
        )


if __name__ == "__main__":
    n = 20          # Количество предметов
    max_price = 100 # Верхняя граница цены (для utils.items_cost)
    capacity = 3.5  # Вместимость рюкзака

    # Набор с равномерным распределением весов
    items_uniform = uniform_distribution(n, max_price)
    print_result("Равномерное распределение", items_uniform, capacity)

    # Набор с нормальным распределением весов
    items_normal = normal_distribution(n, max_price)
    print_result("Нормальное распределение", items_normal, capacity)