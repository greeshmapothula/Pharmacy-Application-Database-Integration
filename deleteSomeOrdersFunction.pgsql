CREATE OR REPLACE FUNCTION deleteSomeOrdersFunction(maxOrderDeletions INT)

RETURNS INT AS $$ -- INTEGER

DECLARE
	total_deleted INT := 0;
	supplier_data RECORD;
	deleted_count INT;

BEGIN
	IF maxOrderDeletions <= 0 THEN
    	RETURN -1;
	END IF;

	FOR supplier_data IN
    	WITH SupplierStats AS (
        	SELECT
            	s.supplierid,
            	s.suppliername,

            	-- Count of future orders for this supplier
            	COUNT(*) FILTER (WHERE o.orderdate > '2024-01-05') AS future_orders,

            	-- Count of cancelled past orders for this supplier
            	COUNT(*) FILTER (WHERE o.orderdate <= '2024-01-05' AND o.status = 'cnld') AS cancelled_past_orders

        	FROM
            	Supplier s
        	JOIN
            	OrderSupply o ON s.supplierid = o.supplierid
        	GROUP BY
            	s.supplierid, s.suppliername
    	)
    	
        SELECT *
    	FROM SupplierStats
    	WHERE cancelled_past_orders > 0
    	ORDER BY cancelled_past_orders DESC, supplierName ASC

	LOOP
    	IF (total_deleted + supplier_data.future_orders) <= maxOrderDeletions THEN

            IF supplier_data.future_orders > 0 THEN
       	 
        	    DELETE FROM OrderSupply
        	    WHERE
            	    supplierid = supplier_data.supplierid AND orderdate > '2024-01-05';

        	    -- Get the number of rows affected by the DELETE operation
        	
                GET DIAGNOSTICS deleted_count = ROW_COUNT;

        	    total_deleted := total_deleted + deleted_count;
            END IF;

    	ELSE
        	RETURN total_deleted;
    	
        END IF;
	
    END LOOP;

	RETURN total_deleted;

END;
$$ LANGUAGE plpgsql;
