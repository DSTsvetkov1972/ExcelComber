SELECT
	count()
FROM
	audit._spravka_tk_pogruzka_konteinerov_porozhnie_i_gruzhionye
WHERE /*NOT (`Отправка` LIKE 'Х%' OR `Отправка` LIKE 'X%') AND */
`Исходник` == 'spravka_tk_pogruzka_konteinerov_porozhnie_i_gruzhionye_s_2025-10-10_po_2025-10-11.xlsx' --ORDER BY `Строка в исходнике`


SELECT
	*
FROM
	audit._spravka_tk_pogruzka_konteinerov_porozhnie_i_gruzhionye
WHERE
	lowerUTF8(`Грузоотправитель`) LIKE '%фсб%'