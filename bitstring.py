from typing import Union, List


class BitString:
    MAX_SIZE: int = 100  # Максимально возможный размер списка как константа
    size: int  # Максимальный размер строки
    bits: List[int]  # Список бит
    count: int  # Текущее количество элементов

    def __init__(self, size_or_string: Union[int, str]) -> None:
        """Инициализация битовой строки размером или строкой"""
        if isinstance(size_or_string, int):
            if size_or_string <= 0 or size_or_string > self.MAX_SIZE:
                raise ValueError(f"Размер должен быть от 1 до {self.MAX_SIZE}")
            self.size = size_or_string
            self.bits = [0] * size_or_string
            self.count = size_or_string  # Изначально count равен size
        elif isinstance(size_or_string, str):
            if len(size_or_string) > self.MAX_SIZE:
                raise ValueError(f"Длина строки не должна превышать {self.MAX_SIZE}")
            for char in size_or_string:
                if char not in '01':
                    raise ValueError("Строка должна содержать только 0 и 1")
            self.size = len(size_or_string)
            self.bits = [int(char) for char in size_or_string]
            self.count = len(size_or_string)
        else:
            raise ValueError("Аргумент должен быть числом или строкой")

    def __str__(self) -> str:
        """Строковое представление битовой строки"""
        return ''.join(str(bit) for bit in self.bits[:self.count])

    def __getitem__(self, index: int) -> int:
        """Перегрузка оператора индексирования для чтения"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= self.count:
            raise IndexError(f"Индекс должен быть от 0 до {self.count - 1}")
        return self.bits[index]

    def __setitem__(self, index: int, value: int) -> None:
        """Перегрузка оператора индексирования для записи"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= self.count:
            raise IndexError(f"Индекс должен быть от 0 до {self.count - 1}")
        if value not in (0, 1):
            raise ValueError("Значение должно быть 0 или 1")
        self.bits[index] = value

    def get_size(self) -> int:
        """Возвращает установленную максимальную длину"""
        return self.size

    def set_count(self, new_count: int) -> None:
        """Установка нового значения count с проверками"""
        if not isinstance(new_count, int):
            raise TypeError("Count должен быть целым числом")
        if new_count < 0 or new_count > self.size:
            raise ValueError(f"Count должен быть от 0 до {self.size}")
        if new_count > self.count:
            self.bits[self.count:new_count] = [0] * (new_count - self.count)
        self.count = new_count

    def __and__(self, other: 'BitString') -> 'BitString':
        """Операция AND"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        result: BitString = BitString(self.count)
        result.bits = [a & b for a, b in zip(self.bits, other.bits)]
        result.count = self.count
        return result

    def __or__(self, other: 'BitString') -> 'BitString':
        """Операция OR"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        result: BitString = BitString(self.count)
        result.bits = [a | b for a, b in zip(self.bits, other.bits)]
        result.count = self.count
        return result

    def __xor__(self, other: 'BitString') -> 'BitString':
        """Операция XOR"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        result: BitString = BitString(self.count)
        result.bits = [a ^ b for a, b in zip(self.bits, other.bits)]
        result.count = self.count
        return result

    def __invert__(self) -> 'BitString':
        """Операция NOT"""
        result: BitString = BitString(self.size)
        result.bits = [1 - bit for bit in self.bits[:self.count]]
        result.count = self.count
        return result

    def shift_left(self, n: int) -> 'BitString':
        """Сдвиг влево на n позиций"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Сдвиг должен быть неотрицательным целым числом")
        result: BitString = BitString(self.size)
        if n >= self.count:
            result.set_count(self.count)
            return result
        result.bits = self.bits[n:self.count] + [0] * n
        result.set_count(self.count)
        return result

    def shift_right(self, n: int) -> 'BitString':
        """Сдвиг вправо на n позиций"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Сдвиг должен быть неотрицательным целым числом")
        result: BitString = BitString(self.size)
        if n >= self.count:
            result.set_count(self.count)
            return result
        result.bits = [0] * n + self.bits[:self.count - n]
        result.set_count(self.count)
        return result


# Пример использования
if __name__ == "__main__":
    # Создание объектов разными способами
    b1: BitString = BitString(8)  # Через размер
    b2: BitString = BitString("10101010")  # Через строку

    # Установка значений через индексацию
    b1[0] = 1
    b1[2] = 1
    b1[4] = 1
    b1[6] = 1

    print(f"b1:         {b1}")
    print(f"b2:         {b2}")
    print(f"Size b1:    {b1.get_size()}")
    print(f"b1[2]:      {b1[2]}")
    print(f"AND:        {b1 & b2}")
    print(f"OR:         {b1 | b2}")
    print(f"XOR:        {b1 ^ b2}")
    print(f"NOT b1:     {~b1}")
    print(f"Shift L 2:  {b1.shift_left(2)}")
    print(f"Shift R 2:  {b1.shift_right(2)}")

    # Изменение count
    b1.set_count(6)
    print(f"After count=6: {b1}")