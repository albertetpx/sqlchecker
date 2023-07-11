select nombre, apellido1, apellido2, email from empleado where puesto like "Director General";
select nombre, apellido1, apellido2, puesto from empleado where puesto not like "Representante Ventas";
select nombre_cliente from cliente where pais like "Spain";
select distinct estado from pedido;
select distinct codigo_cliente from pago where YEAR(fecha_pago) = 2008;
select distinct codigo_cliente from pago where left(fecha_pago,4) = 2008;
select codigo_pedido, codigo_cliente, fecha_esperada, fecha_entrega from pedido where estado != "Entregado";
select codigo_pedido, codigo_cliente, fecha_esperada, fecha_entrega from pedido
where adddate(fecha_entrega, interval 2 day) <= fecha_esperada;
select codigo_pedido, codigo_cliente, fecha_esperada, fecha_entrega from pedido
where datediff(fecha_esperada, fecha_entrega) >= 2;
select codigo_producto, cantidad_en_stock from producto where gama like "Ornamentales" and cantidad_en_stock > 100
order by codigo_producto asc;
select c.nombre_cliente, e.nombre, e.apellido1
from cliente c join empleado e
	on c.codigo_empleado_rep_ventas = e.codigo_empleado
order by c.nombre_cliente;
select c.nombre_cliente, e.nombre, e.apellido1, o.ciudad
from cliente c join empleado e
	on c.codigo_empleado_rep_ventas = e.codigo_empleado
join oficina o
	on e.codigo_oficina = o.codigo_oficina
order by c.nombre_cliente;
select distinct c.nombre_cliente
from pago p join cliente c
	on p.codigo_cliente = c.codigo_cliente
order by c.nombre_cliente;
select distinct c.nombre_cliente
from pago p right join cliente c
	on p.codigo_cliente = c.codigo_cliente
where p.codigo_cliente is null
order by c.nombre_cliente;
select distinct c.nombre_cliente, concat_ws(' ',e.nombre, e.apellido1, e.apellido2) as "representante"
from pago p join cliente c
	on p.codigo_cliente = c.codigo_cliente
join empleado e
	on c.codigo_empleado_rep_ventas = e.codigo_empleado
order by c.nombre_cliente;    
select distinct c.nombre_cliente, concat_ws(' ',e.nombre, e.apellido1, e.apellido2) as "representante", o.ciudad as "oficina"
from pago p join cliente c
	on p.codigo_cliente = c.codigo_cliente
join empleado e
	on c.codigo_empleado_rep_ventas = e.codigo_empleado
join oficina o
	on e.codigo_oficina = o.codigo_oficina
order by c.nombre_cliente;
select concat_ws(' ', e.nombre, e.apellido1, e.apellido2) as "nombreEmpleado",
concat_ws(' ',ej.nombre, ej.apellido1, ej.apellido2) as "nombreJefe"
from empleado e join empleado ej
	on e.codigo_jefe = ej.codigo_empleado;
select concat_ws(' ', e.nombre, e.apellido1, e.apellido2) as "nombreEmpleado",
concat_ws(' ',ej.nombre, ej.apellido1, ej.apellido2) as "nombreJefe",
concat_ws(' ',ejj.nombre, ejj.apellido1, ejj.apellido2) as "nombreJefazo"
from empleado e join empleado ej
	on e.codigo_jefe = ej.codigo_empleado
join empleado ejj
	on ej.codigo_jefe = ejj.codigo_empleado;
select distinct c.nombre_cliente
from cliente c join pedido p
	on p.codigo_cliente = c.codigo_cliente
where p.estado like "Pendiente"
order by c.nombre_cliente asc;
select g.gama, count(p.codigo_producto) as "NumeroProductos", round(avg(p.precio_venta),2) as "PrecioMedio"
from gama_producto g join producto p
	on p.gama = g.gama
group by g.gama
order by g.gama asc;
select p.nombre, sum(d.cantidad) as "NumeroUnidades"
from detalle_pedido d join producto p
	on d.codigo_producto = p.codigo_producto
group by p.nombre
order by NumeroUnidades desc, p.nombre asc;
select g.gama, sum(d.cantidad) as "NumeroUnidades" from detalle_pedido d join producto p
	on d.codigo_producto = p.codigo_producto
join gama_producto g
	on p.gama = g.gama
group by g.gama
order by NumeroUnidades desc;