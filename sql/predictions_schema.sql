
CREATE TABLE model_predictions (
    dia DATE,
    modelo TEXT,
    valor_real NUMERIC,
    valor_previsto NUMERIC,
    PRIMARY KEY (dia, modelo)
);