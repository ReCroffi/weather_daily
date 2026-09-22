CREATE VIEW weather_features AS SELECT
    dia,
    temp_max,
    temp_min,
    precipitacao,
    velocidade_vento,  
    LEAD(temp_max) OVER (ORDER BY dia) AS temp_max_dia_seguinte,
    LEAD(temp_min) OVER (ORDER BY dia) AS temp_min_dia_seguinte,
    LEAD(precipitacao) OVER (ORDER BY dia) AS precipitacao_dia_seguinte,
    LEAD(velocidade_vento) OVER (ORDER BY dia) AS velocidade_vento_dia_seguinte,
    AVG(temp_max) OVER (ORDER BY dia ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel_temp_max
FROM weather_daily; 