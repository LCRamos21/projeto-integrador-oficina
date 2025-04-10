-- Script SQL para criação das tabelas do banco de dados do Sistema de Gerenciamento de Ordens de Serviço
-- Compatível com SQLite

-- Tabela para armazenar os usuários do sistema
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária autoincrementável
    username TEXT NOT NULL UNIQUE,         -- Nome de usuário (obrigatório e único)
    password TEXT NOT NULL                 -- Senha do usuário (obrigatória)
);

-- Tabela para armazenar as ordens de serviço
CREATE TABLE IF NOT EXISTS ordens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária autoincrementável
    cliente TEXT NOT NULL,                 -- Nome do cliente (obrigatório)
    modelo TEXT NOT NULL,                  -- Modelo do equipamento (obrigatório)
    problema TEXT NOT NULL,                -- Descrição do problema (obrigatório)
    data_entrada TEXT NOT NULL,            -- Data de entrada (obrigatória, formato YYYY-MM-DD)
    status TEXT NOT NULL,                  -- Status atual da ordem (obrigatório)
    valor REAL,                            -- Valor do serviço (pode ser nulo)
    user_id INTEGER NOT NULL,              -- Chave estrangeira para relacionar com o usuário que criou a ordem (obrigatório)

    -- Definição da chave estrangeira
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE RESTRICT -- Impede deletar um usuário se ele tiver ordens associadas
        ON UPDATE CASCADE  -- Se o ID do usuário mudar (raro), atualiza aqui também
);

-- (Opcional) Criação de Índices para otimizar buscas frequentes (Exemplo)
-- CREATE INDEX IF NOT EXISTS idx_ordens_status ON ordens (status);
-- CREATE INDEX IF NOT EXISTS idx_ordens_cliente ON ordens (cliente);

