class InfoMessage:
    """Информационное сообщение о тренировке."""
    after_dot = '%.3f'

    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        type_info = f'Тип тренировки: {self.training_type}; '
        duration_info = f'Длительность: {self.after_dot} ч.; ' % self.duration
        distance_info = f'Дистанция: {self.after_dot} км; ' % self.distance
        speed_info = f'Ср. скорость: {self.after_dot} км/ч; ' % self.speed
        calories_info = f'Потрачено ккал: {self.after_dot}.' % self.calories
        message = f'{type_info}{duration_info}{distance_info}' \
                  f'{speed_info}{calories_info}' \
                  f''
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        hour_in_minutes: int = 60
        spent_calories = (coeff_calorie_1
                          * self.get_mean_speed() - coeff_calorie_2)\
                         * self.weight / self.M_IN_KM\
                         * (self.duration * hour_in_minutes)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed = super().get_mean_speed()
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        spent_calories = (coeff_calorie_1 *
                          self.weight + (mean_speed ** 2 // self.height)
                          * coeff_calorie_2 * self.weight) *\
                         (self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self):
        mean_speed: float = self.length_pool * \
                            self.count_pool / \
                            self.M_IN_KM / \
                            self.duration
        return mean_speed

    def get_spent_calories(self):
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories: float = (self.get_mean_speed()
                                 + coeff_calorie_1)\
                                * coeff_calorie_2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    unpacking = training_dict[workout_type](*data)
    return unpacking


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
