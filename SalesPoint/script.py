import os
import django
import sys
import xml.etree.ElementTree as ET

django_project_path = 'C:/Users/Matias/OneDrive/Escritorio/Data_Structure/SalesPoint/SalesPoint'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SalesPoint.settings')
sys.path.append(django_project_path)
django.setup()
from SalesPoint.core.erp.models import SaleDetails

try:
    id = input("Ingrese el id de la compra que desea facturar: ")
    sales = SaleDetails.objects.filter(sale_id=int(id))
    # Obtener la venta relacionada con los productos
    sale = sales.first().sale

    print(f"Id Venta: {sale.pk}")
    print(f"Fecha: {sale.date_sale}")
    print(f"Cédula Cliente: {sale.client.dni}")
    print(f"Razón Social: {sale.client.names} {sale.client.surnames}")
    print(f"Fecha Nacimiento: {sale.client.birth}")
    print(f"Contacto: {sale.client.phone}")
    print(f"Correo: {sale.client.mail}")
    print(f"Fecha de venta: {sale.date_sale}")
    print(f"Subtotal: {sale.subtotal}")
    print(f"Iva: {sale.iva}")
    print(f"Total: {sale.total}")
    print("===========================================================================")
    # Iterar sobre los productos
    for sale_detail in sales:
        print(f"Producto: {sale_detail.product.name} | Cantidad: {sale_detail.amount} | Precio: {sale_detail.price} | Subtotal: {sale_detail.subtotal}")
    
    try:
        # Crear el elemento raíz del XML
        root = ET.Element("Venta")

        # Crear elementos y asignarles los valores correspondientes
        ET.SubElement(root, "IdVenta").text = str(sale.pk)
        ET.SubElement(root, "Fecha").text = str(sale.date_sale)
        ET.SubElement(root, "CedulaCliente").text = str(sale.client.dni)
        ET.SubElement(root, "RazonSocial").text = f"{sale.client.names} {sale.client.surnames}"
        ET.SubElement(root, "FechaNacimiento").text = str(sale.client.birth)
        ET.SubElement(root, "Contacto").text = str(sale.client.phone)
        ET.SubElement(root, "Correo").text = str(sale.client.mail)
        ET.SubElement(root, "Subtotal").text = str(sale.subtotal)
        ET.SubElement(root, "IVA").text = str(sale.iva)
        ET.SubElement(root, "Total").text = str(sale.total)

        # Crear el elemento de productos y agregar los elementos de cada producto
        productos = ET.SubElement(root, "Productos")
        for sale_detail in sales:
            producto = ET.SubElement(productos, "Producto")
            ET.SubElement(producto, "Nombre").text = sale_detail.product.name
            ET.SubElement(producto, "Cantidad").text = str(sale_detail.amount)
            ET.SubElement(producto, "Precio").text = str(sale_detail.price)
            ET.SubElement(producto, "Subtotal").text = str(sale_detail.subtotal)

        # Crear el árbol XML
        tree = ET.ElementTree(root)

        # Guardar el XML en un archivo
        tree.write("venta.xml", encoding="utf-8", xml_declaration=True)
        print("Archivo XML generado correctamente.")
    except Exception as e:
        print(f"No se pudo generar el XML por el error: {e}")
except Exception as e:
    print("No es un ID de compra válido")