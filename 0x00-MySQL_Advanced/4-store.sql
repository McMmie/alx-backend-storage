-- a SQL script that creates a trigger that decreases the 
-- quantity of an item after adding a new order.

CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = CASE
		WHEN quantity - orders.number >= 0 THEN quantity - orders.number
		ELSE 0
	END
	WHERE name = NEW.item_name;
END
