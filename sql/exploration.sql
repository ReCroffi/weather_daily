-- existe sazonalidade visivel por mes? t
SELECT
    EXTRACT(MONTH FROM dia) AS month,
    TRUNC(AVG(temp_max)::numeric, 2) AS avg_temperature_max,
    TRUNC(AVG(temp_min)::numeric, 2) AS avg_temperature_min,
    TRUNC(AVG(precipitacao)::numeric, 2) AS avg_precipitation
FROM weather_daily
GROUP BY month
ORDER BY month; 

-- podemos ver que existe sazonalidade visivel por mes, com junho e julho mais frios e secos e dezembro a março mais quente e chuvoso.

-- Precipitação correlaciona com temperatura?
SELECT
    TRUNC(CORR(temp_max, precipitacao)::numeric, 2) AS correlation_temp_max_precipitation,
    TRUNC(CORR(temp_min, precipitacao)::numeric, 2) AS correlation_temp_min_precipitation
FROM weather_daily;

-- existe correlação positiva entre a temperatura minima e precipitação, o que parece ser contra intuitivo, mas pode ser explicado pelo fato de que em dias mais quentes, a evaporação é maior, formando uma camada de nuvens que funcionam como um cobertor. 

--Qual variável tem maior desvio dia a dia?
SELECT
    TRUNC(STDDEV(temp_max)::numeric, 2)/TRUNC(AVG(temp_max)::numeric, 2) AS stddev_temp_max,
    TRUNC(STDDEV(temp_min)::numeric, 2)/TRUNC(AVG(temp_min)::numeric, 2) AS stddev_temp_min,
    TRUNC(STDDEV(precipitacao)::numeric, 2)/TRUNC(AVG(precipitacao)::numeric, 2) AS stddev_precipitation
FROM weather_daily; 

-- podemos ver que a variável com maior desvio dia a dia é a precipitação pois a região tem epócas de chuvas e secas muito bem definidas.
