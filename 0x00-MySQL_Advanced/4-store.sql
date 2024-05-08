-- Create the trigger
DROP TRIGGER IF EXISTS decrease_quantity_trigger;
CREATE TRIGGER decrease_quantity_trigger
AFTER INSERT ON orders
FOR EACH ROW
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
