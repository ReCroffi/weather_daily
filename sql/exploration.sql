-- 1. Existe sazonalidade visível por mês?
SELECT
    EXTRACT(MONTH FROM dia) AS month,
    TRUNC(AVG(temp_max)::numeric, 2) AS avg_temperature_max,
    TRUNC(AVG(temp_min)::numeric, 2) AS avg_temperature_min,
    TRUNC(AVG(precipitacao)::numeric, 2) AS avg_precipitation
FROM weather_daily
GROUP BY month
ORDER BY month;

-- Conclusão: existe sazonalidade visível por mês, com junho e julho mais frios e secos,
-- e dezembro a março mais quente e chuvoso.


-- 2. Precipitação correlaciona com temperatura?
SELECT
    TRUNC(CORR(temp_max, precipitacao)::numeric, 2) AS correlation_temp_max_precipitation,
    TRUNC(CORR(temp_min, precipitacao)::numeric, 2) AS correlation_temp_min_precipitation
FROM weather_daily;

-- Conclusão: existe correlação positiva entre a temperatura mínima e a precipitação, o que
-- parece contraintuitivo, mas pode ser explicado pelo fato de que em dias nublados as nuvens
-- funcionam como um cobertor, segurando parte do calor que sairia pra atmosfera e fazendo
-- com que a temperatura não caia tanto.


-- 3. Qual variável tem maior desvio dia a dia?
SELECT
    TRUNC((STDDEV(temp_max)/AVG(temp_max))::numeric, 2) AS cv_temp_max,
    TRUNC((STDDEV(temp_min)/AVG(temp_min))::numeric, 2) AS cv_temp_min,
    TRUNC((STDDEV(precipitacao)/AVG(precipitacao))::numeric, 2) AS cv_precipitation
FROM weather_daily;

-- Conclusão: a variável com maior desvio relativo dia a dia é a precipitação, pois a região
-- tem épocas de chuva e seca muito bem definidas.
