# Отчёт по линейной регрессии

## Используемая модель
Linear Regression

## Целевая переменная
selling_price

## Используемые числовые признаки
- year
- engine
- km_driven
- max_power

## Используемые категориальные признаки
- fuel
- seller_type
- transmission
- owner

## Кодирование категориальных признаков
OneHotEncoder

## Метрика качества модели

### R²
0.6890

## Интерпретация R²

Доля дисперсии target, объясняемая моделью.

## Коэффициенты модели

- num__year: 33628.8721
- num__engine: -35.3377
- num__km_driven: -1.4636
- num__max_power: 12701.5949
- cat__fuel_CNG: 15891.1704
- cat__fuel_Diesel: -22699.7847
- cat__fuel_LPG: 137980.9703
- cat__fuel_Petrol: -131172.3560
- cat__seller_type_Dealer: 187244.6784
- cat__seller_type_Individual: -56407.8918
- cat__seller_type_Trustmark Dealer: -130836.7866
- cat__transmission_Automatic: 222623.0404
- cat__transmission_Manual: -222623.0404
- cat__owner_First Owner: -326174.6441
- cat__owner_Fourth & Above Owner: -320531.2738
- cat__owner_Second Owner: -376192.8033
- cat__owner_Test Drive Car: 1374871.0308
- cat__owner_Third Owner: -351972.3097

## Свободный член

-67493025.1438
