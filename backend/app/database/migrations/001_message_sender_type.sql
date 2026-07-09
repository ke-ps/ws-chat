-- Permitir mensajes sin usuario (IA o sistema)
ALTER TABLE messages
MODIFY COLUMN user_id INT NULL;

-- Añadir el origen del mensaje
ALTER TABLE messages
ADD COLUMN sender_type ENUM('USER', 'AI', 'SYSTEM')
NOT NULL
DEFAULT 'USER'
AFTER user_id;