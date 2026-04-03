-- ============================
-- DATABASE INIT - LAB LEGADO
-- ============================

CREATE TABLE pessoas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14),
    data_nascimento DATE,
    sexo VARCHAR(10),
    tipo_pessoa VARCHAR(3) NOT NULL, -- 'PAC' ou 'MED'
    registro_profissional VARCHAR(30), -- CRM se medico
    especialidade VARCHAR(100),
    telefone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    codigo_registro VARCHAR(50),
    cnpj VARCHAR(18),
    telefone VARCHAR(20),
    plano_nome VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE atendimentos (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    operadora_id INT,
    data_atendimento TIMESTAMP NOT NULL,
    tipo_atendimento VARCHAR(20) DEFAULT 'LAB',
    status VARCHAR(30),
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_paciente
        FOREIGN KEY (paciente_id) REFERENCES pessoas(id),

    CONSTRAINT fk_medico
        FOREIGN KEY (medico_id) REFERENCES pessoas(id),

    CONSTRAINT fk_operadora
        FOREIGN KEY (operadora_id) REFERENCES operadoras(id)
);

CREATE TABLE condicoes (
    id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL,
    atendimento_id INT,
    descricao VARCHAR(255),
    codigo_cid VARCHAR(10),
    data_diagnostico DATE,
    status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cond_paciente
        FOREIGN KEY (paciente_id) REFERENCES pessoas(id),

    CONSTRAINT fk_cond_atendimento
        FOREIGN KEY (atendimento_id) REFERENCES atendimentos(id)
);

CREATE TABLE amostras (
    id SERIAL PRIMARY KEY,
    atendimento_id INT NOT NULL,
    paciente_id INT NOT NULL,
    tipo_amostra VARCHAR(50),
    material VARCHAR(100),
    data_coleta TIMESTAMP,
    status VARCHAR(30),
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_amostra_atendimento
        FOREIGN KEY (atendimento_id) REFERENCES atendimentos(id),

    CONSTRAINT fk_amostra_paciente
        FOREIGN KEY (paciente_id) REFERENCES pessoas(id)
);

CREATE TABLE itens_atendimento (
    id SERIAL PRIMARY KEY,
    atendimento_id INT NOT NULL,
    amostra_id INT,
    descricao VARCHAR(150),
    codigo_interno VARCHAR(50),
    valor_resultado VARCHAR(50),
    unidade VARCHAR(20),
    valor_referencia VARCHAR(50),
    data_resultado TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_item_atendimento
        FOREIGN KEY (atendimento_id) REFERENCES atendimentos(id),

    CONSTRAINT fk_item_amostra
        FOREIGN KEY (amostra_id) REFERENCES amostras(id)
);

-- ============================
-- DADOS FAKE
-- ============================

-- Médicos
INSERT INTO pessoas (nome, cpf, data_nascimento, sexo, tipo_pessoa, registro_profissional, especialidade)
VALUES 
('Dr. Carlos Silva', '111.111.111-11', '1980-05-10', 'M', 'MED', 'CRM12345', 'Clínico Geral');

-- Pacientes
INSERT INTO pessoas (nome, cpf, data_nascimento, sexo, tipo_pessoa)
VALUES 
('Maria Souza', '222.222.222-22', '1995-08-20', 'F', 'PAC'),
('João Pereira', '333.333.333-33', '1988-03-15', 'M', 'PAC');

-- Operadora
INSERT INTO operadoras (nome, codigo_registro, cnpj, telefone, plano_nome)
VALUES
('Unimed Joinville', 'ANS123456', '12.345.678/0001-99', '(47) 3333-0000', 'Plano Premium 200');

-- Atendimento
INSERT INTO atendimentos (paciente_id, medico_id, operadora_id, data_atendimento, status, observacoes)
VALUES
(2, 1, 1, NOW(), 'FINALIZADO', 'Exames de rotina');

-- Condição
INSERT INTO condicoes (paciente_id, atendimento_id, descricao, codigo_cid, data_diagnostico, status)
VALUES
(2, 1, 'Diabetes Mellitus Tipo 2', 'E11', '2023-01-10', 'ativa');

-- Amostra
INSERT INTO amostras (atendimento_id, paciente_id, tipo_amostra, material, data_coleta, status)
VALUES
(1, 2, 'SANGUE', 'Tubo roxo', NOW(), 'analisada');

-- Itens do Atendimento (Exames)
INSERT INTO itens_atendimento (atendimento_id, amostra_id, descricao, codigo_interno, valor_resultado, unidade, valor_referencia, data_resultado)
VALUES
(1, 1, 'Glicose em jejum', 'GLI001', '140', 'mg/dL', '70-99', NOW()),
(1, 1, 'Hemoglobina glicada', 'HBA1C01', '7.5', '%', '< 5.7', NOW());