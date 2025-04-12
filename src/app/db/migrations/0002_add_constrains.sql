ALTER TABLE receptions
ADD CONSTRAINT fk_pvz_id
FOREIGN KEY (pvz_id)
REFERENCES pvzs(id)
ON DELETE CASCADE;

ALTER TABLE products
ADD CONSTRAINT fk_reception_id
FOREIGN KEY (reception_id)
REFERENCES receptions(id)
ON DELETE CASCADE;