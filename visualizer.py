import sys, time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                             QCheckBox, QTextEdit, QMessageBox, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backpack Solver Project")
        self.resize(1000, 800)
        
        # Словарь для хранения результатов расчётов
        self.results_storage = {}

        self.setStyleSheet("""
            QMainWindow { 
                background-color: #090D18; 
            }

            QLabel { 
                color: #7DF9FF; 
                font-size: 14pt; 
                font-weight: bold; 
            }

            QLineEdit, QComboBox { 
                background-color: #10182B; 
                color: #EAF6FF; 
                border: 1px solid #00E5FF; 
                padding: 6px; 
                border-radius: 6px; 
                font-size: 13pt;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #FCEE0A;
            }

            QComboBox::drop-down {
                border: none;
                width: 24px;
            }

            QComboBox QAbstractItemView {
                background-color: #121A2F;
                color: #BDEBFF;
                selection-background-color: #00E5FF;
                selection-color: #081018;
                border: 1px solid #FCEE0A;
                outline: 0;
            }

            QCheckBox { 
                color: #EAF6FF; 
                font-size: 13pt; 
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #00E5FF;
                border-radius: 4px;
                background-color: #0E1424;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #FCEE0A;
            }
            QCheckBox::indicator:checked {
                background-color: #FCEE0A;
                border: 2px solid #00FFD1;
            }

            QTextEdit { 
                background-color: #0A1020; 
                color: #FCEE0A; 
                font-family: 'Consolas', 'JetBrains Mono', monospace;
                font-size: 12.5pt; 
                border: 2px solid #00E5FF; 
                border-radius: 8px; 
                padding: 10px;
                selection-background-color: #FCEE0A;
                selection-color: #000000;
            }

            QPushButton { 
                background-color: #00E5FF; 
                color: #081018; 
                font-size: 13pt; 
                font-weight: bold; 
                border: 1px solid #FCEE0A;
                border-radius: 6px; 
                padding: 10px 22px; 
            }
            QPushButton:hover {
                background-color: #FCEE0A;
                color: #000000;
                border: 1px solid #00E5FF;
            }
            QPushButton:pressed {
                background-color: #FFD400;
                color: #000000;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Блок управления
        top_wrapper = QHBoxLayout()
        grid = QGridLayout() #сетка/невидимая таблица
        grid.setSpacing(20)

        grid.addWidget(QLabel("Кол-во (N):"), 0, 0)
        self.edit_n = QLineEdit()
        grid.addWidget(self.edit_n, 0, 1)
        grid.addWidget(QLabel("Макс. цена (X):"), 0, 2)
        self.edit_max_price = QLineEdit()
        grid.addWidget(self.edit_max_price, 0, 3)

        grid.addWidget(QLabel("Алгоритмы:"), 1, 0)
        self.check_bb = QCheckBox("Ветвей и границ")
        self.check_greedy = QCheckBox("Жадный")
        grid.addWidget(self.check_bb, 1, 1)
        grid.addWidget(self.check_greedy, 1, 2)

        grid.addWidget(QLabel("Данные:"), 2, 0)
        self.check_uniform = QCheckBox("Равномерное")
        self.check_normal = QCheckBox("Нормальное")
        grid.addWidget(self.check_uniform, 2, 1)
        grid.addWidget(self.check_normal, 2, 2)

        top_wrapper.addLayout(grid)
        top_wrapper.addStretch()
        main_layout.addLayout(top_wrapper)

        # Кнопка и Фильтр
        action_layout = QHBoxLayout()
        self.btn_solve = QPushButton("Запустить расчёт")
        self.btn_solve.clicked.connect(self.solve_task)
        
        self.combo_filter = QComboBox()
        self.combo_filter.setFixedWidth(400)
        self.combo_filter.addItem("Сначала запустите расчёт...")
        self.combo_filter.currentIndexChanged.connect(self.update_display)
        
        action_layout.addWidget(self.btn_solve)
        action_layout.addSpacing(20)
        action_layout.addWidget(QLabel("Просмотр результатов:"))
        action_layout.addWidget(self.combo_filter)
        action_layout.addStretch()
        main_layout.addLayout(action_layout)

        # --- Вывод ---
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output)

    def solve_task(self):
        try:
            from utils import uniform_distribution, normal_distribution
            from solver import greedy_algo
            from stick_n_rope import stick_n_rope as branch_boundary_method

            n = int(self.edit_n.text())
            x = int(self.edit_max_price.text())
            w = 1
            
            self.results_storage = {} 
            self.combo_filter.clear()
            self.combo_filter.addItem("Показать всё")

            dists = []
            if self.check_uniform.isChecked(): dists.append(("Равномерное", uniform_distribution))
            if self.check_normal.isChecked(): dists.append(("Нормальное", normal_distribution))

            algos = []
            if self.check_bb.isChecked(): algos.append(("Ветвей и границ", branch_boundary_method))
            if self.check_greedy.isChecked(): algos.append(("Жадный", greedy_algo))

            if not dists or not algos:
                QMessageBox.warning(self, "Внимание", "Выберите данные и алгоритм!")
                return

            for d_name, d_func in dists:
                items = d_func(n, x)
                
                # ШАГ 1: Находим точное решение для этого набора данных
                # Оно нужно как эталон для расчета погрешности
                exact_items, exact_w, exact_p = branch_boundary_method(items, w)
                
                for a_name, a_func in algos:
                    start = time.perf_counter()
                    res_items, final_w, final_p = a_func(items, w)
                    dt = time.perf_counter() - start
                    
                    # Считаем погрешность
                    # Если текущий алгоритм и есть Ветви и Границы, погрешность = 0
                    if a_name == "Ветвей и границ":
                        error_str = "0.000% (Точное решение)"
                    else:
                        # exact_p — результат ветвей и границ (ЭТАЛОН)
                        # final_p — результат жадного алгоритма

                        if exact_p > 0:
                            # Погрешность = (Разница / Эталон) * 100
                            relative_error = ((exact_p - final_p) / exact_p) * 100
                            error_str = f"{relative_error:.4f}%"
                        else:
                            error_str = "0.000%"

                    key = f"{a_name} ({d_name})"
                    self.combo_filter.addItem(key)
                    
                    # Формируем текст
                    text = f"РЕЗУЛЬТАТ: {key}\n"
                    text += f"Выполнено за: {dt:.6f} сек.\n"
                    text += f"Относительная погрешность: {error_str}\n"
                    text += "-" * 45 + "\n"
                    for i in res_items:
                        text += f"ID: {i['index']:03} | Вес: {i['weight']:.9f} | Цена: {i['price']:.5f}\n"
                    text += "-" * 45 + "\n"
                    text += f"ИТОГОВЫЙ ВЕС:  {final_w:.15f}\n"
                    text += f"ИТОГОВАЯ ЦЕНА: {final_p:.9f}\n"
                    
                    self.results_storage[key] = text

            self.update_display()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def update_display(self): #фильтрация
        choice = self.combo_filter.currentText()
        if choice == "Показать всё":
            all_text = "\n\n".join(self.results_storage.values())
            self.result_output.setText(all_text)
        elif choice in self.results_storage:
            self.result_output.setText(self.results_storage[choice])