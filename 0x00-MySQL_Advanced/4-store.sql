-- SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

-- Quantity in the table items can be negative.

DROP TRIGGER IF EXISTS decrease_item_quantity;

CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDAT items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
